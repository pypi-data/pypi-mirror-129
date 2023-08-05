"""Build class definition"""

import logging
import os
from datetime import datetime, timedelta
from itertools import islice
from time import sleep
from typing import Dict, List, Tuple

import requests

from yojenkins.monitor import BuildMonitor
from yojenkins.utility import utility
from yojenkins.utility.utility import fail_out, print2
from yojenkins.yo_jenkins.jenkins_item_classes import JenkinsItemClasses
from yojenkins.yo_jenkins.status import BuildStatus

# Getting the logger reference
logger = logging.getLogger()


class Build():
    """Buld class"""

    def __init__(self, rest, auth) -> None:
        """Object constructor method, called at object creation

        Args:
            rest: Rest object
            auth: Auth object

        Returns:
            None
        """
        self.rest = rest
        self.auth = auth
        self.build_monitor = BuildMonitor(rest, auth, self)

        self.build_logs_extension = ".log"

    def info(self,
             build_url: str = '',
             job_name: str = '',
             job_url: str = '',
             build_number: int = None,
             latest: bool = False) -> Dict:
        """TODO Docstring

        Args:
            TODO

        Returns:
            TODO
        """
        if build_url:
            # Making a direct request using the passed url
            request_url = f"{build_url.strip('/')}/api/json"
            build_info = self.rest.request(request_url, 'get', is_endpoint=False)[0]
            if not build_info:
                fail_out('Failed to get build info')
        else:
            if not job_name and not job_url:
                fail_out('No job name, job url, and build url provided')

            if job_name and not job_url:
                job_url = utility.name_to_url(self.rest.get_server_url(), job_name)

            job_info, _, success = self.rest.request(f'{job_url.strip("/")}/api/json', 'get', is_endpoint=False)
            if not success:
                fail_out(f'Failed getting build info, because failed to request job info: {job_url}')

            # Check if found item type/class is a build
            if job_info['_class'] not in JenkinsItemClasses.JOB.value['class_type']:
                fail_out(f'Failed to match job type/class. The found item is "{job_info["_class"]}"')

            job_last_build_number = job_info['lastBuild']['number'] if 'lastBuild' in job_info else 0

            # If build number is not passed, get the latest build number for job
            if not build_number and latest:
                # Build number not passed and latest flag is not set
                logger.debug(
                    f'No build number passed BUT --latest flag set. Using latest build number for this job: {job_last_build_number}'
                )
                build_number = job_last_build_number
            elif not build_number and not latest:
                fail_out('Failed to specify build. No build number passed and --latest flag not set')
            else:
                # Build number is passed
                if build_number > job_last_build_number:
                    fail_out('Failed to specify build. Build number exceeds last build number for this job')

            logger.debug(f'Getting build info for job "{job_info["fullName"]}, build {build_number} ...')
            build_info, _, success = self.rest.request(f'{job_url.strip("/")}/{build_number}/api/json',
                                                       'get',
                                                       is_endpoint=False)
            if not success:
                fail_out('Failed to request build info')

        # Check if found item type/class is a build
        if build_info['_class'] not in JenkinsItemClasses.BUILD.value['class_type']:
            fail_out(f'Build found, but failed to match build type/class. This item is "{build_info["_class"]}"')

        # Add additional derived information
        if 'timestamp' in build_info:
            build_info['startDatetime'] = datetime.fromtimestamp(build_info['timestamp'] /
                                                                 1000.0).strftime("%A, %B %d, %Y %I:%M:%S")
            build_info['estimatedDurationFormatted'] = str(timedelta(
                seconds=build_info["estimatedDuration"] /
                1000.0))[:-3] if build_info["estimatedDuration"] > 0 else None

            # Check if results are in
            if 'result' in build_info:
                if build_info['result']:
                    build_info['resultText'] = build_info['result']
                    build_info['durationFormatted'] = str(timedelta(seconds=build_info['duration'] / 1000.0))[:-3]
                    build_info['endDatetime'] = datetime.fromtimestamp(
                        (build_info['timestamp'] + build_info['duration']) / 1000.0).strftime("%A, %B %d, %Y %I:%M:%S")
                    build_info['elapsedFormatted'] = build_info['durationFormatted']
                else:
                    build_info['resultText'] = BuildStatus.RUNNING.value
                    build_info['durationFormatted'] = None
                    build_info['endDatetime'] = None
                    build_info['elapsedFormatted'] = str(
                        timedelta(seconds=((datetime.utcnow().timestamp()) - build_info['timestamp'] / 1000)))[:-3]

            else:
                build_info['resultText'] = BuildStatus.UNKNOWN.value
        else:
            build_info['startDatetime'] = None
            build_info['estimatedDurationFormatted'] = None
            build_info['resultText'] = BuildStatus.NOT_RUN.value
            build_info['durationFormatted'] = None
            build_info['endDatetime'] = None
            build_info['elapsedFormatted'] = None

        if 'url' in build_info:
            build_info['fullName'] = utility.url_to_name(build_info['url'])
            build_info['jobUrl'] = utility.build_url_to_other_url(build_info['url'], target_url='job')
            build_info['jobFullName'] = utility.url_to_name(build_info['jobUrl'])
            build_info['jobName'] = utility.fullname_to_name(build_info['jobFullName'])
            build_info['folderUrl'] = utility.build_url_to_other_url(build_info['url'], target_url='folder')
            build_info['folderFullName'] = utility.url_to_name(build_info['folderUrl'])
            build_info['folderName'] = utility.fullname_to_name(build_info['folderFullName'])
            build_info['serverURL'] = utility.item_url_to_server_url(build_info['url'])
            build_info['serverDomain'] = utility.item_url_to_server_url(build_info['url'], False)

            build_info[
                'folderFullName'] = 'Base Folder' if not build_info['folderFullName'] else build_info['folderFullName']

        if 'builtOn' not in build_info:
            build_info['builtOn'] = 'N/A'
        else:
            build_info['builtOn'] = 'N/A' if not build_info['builtOn'] else build_info['builtOn']

        return build_info

    def status_text(self,
                    build_url: str = '',
                    job_name: str = '',
                    job_url: str = '',
                    build_number: int = None,
                    latest: bool = False) -> str:
        """TODO Docstring

        Args:
            TODO

        Returns:
            TODO
        """
        # Get the build info
        build_info = self.info(build_url=build_url,
                               job_name=job_name,
                               job_url=job_url,
                               build_number=build_number,
                               latest=latest)

        # If nothing is returned, check if job is queued on server
        if not build_info:
            logger.debug('The specified build was not found in job')
            logger.debug('Looking for build in the server build queue ...')
            if build_url:
                job_url = utility.build_url_to_other_url(build_url)
            elif job_name:
                pass
            elif job_url:
                pass
            else:
                fail_out('Failed to find build status text. Specify build url, job name, or job url')
            logger.debug(f'Job name: {job_name}')

            # Requesting all queue and searching queue (NOTE: Could use Server object)
            logger.debug(f'Requesting all build queue items ...')
            queue_all = self.rest.request('queue/api/json', 'get')[0]
            logger.debug(f"Number of queued items found: {len(queue_all['items'])}")
            queue_matches = utility.queue_find(queue_all, job_name=job_name, job_url=job_url)
            if not queue_matches:
                fail_out('Failed to find running or queued builds')
            queue_info = queue_matches[0]

            if not queue_info:
                logger.debug('Build for job NOT found in queue')
                return BuildStatus.NOT_FOUND.value
            else:
                logger.debug(f'Build for job found in queue. Queue number {queue_info["id"]}')
                return BuildStatus.QUEUED.value

        # FIXME: resultText is returned in build info. Maybe move queue check to build_info??

        # Check if in process (build is there but results not posted)
        if 'result' not in build_info:
            logger.debug('Build was found running/building, however no results are posted')
            return BuildStatus.RUNNING.value
        else:
            # FIXME: Get "No status found" when "yojenkins build status --url" on build that is "RUNNING" (result: Null)
            logger.debug('Build found, but has concluded or stopped with result')
            return build_info['result']

    def abort(self,
              build_url: str = '',
              job_name: str = '',
              job_url: str = '',
              build_number: int = None,
              latest: bool = False) -> int:
        """TODO Docstring

        Args:
            TODO

        Returns:
            TODO
        """
        if build_url:
            logger.debug(f'Build URL passed: {build_url}')
            url = build_url
        else:
            logger.debug('NO build URL passed. Getting build information ...')
            # Get build info request
            build_info = self.info(build_url, job_name, job_url, build_number, latest)
            url = build_info['url']

        # Making a direct request using the passed url
        logger.debug(f'Aborting build: {url} ...')
        request_url = f"{url.strip('/')}/stop"
        if not self.rest.request(request_url, 'post', is_endpoint=False)[2]:
            fail_out('Failed to abort build. Build may not exist or is queued')

        logger.debug('Successfully aborted build')

        return utility.build_url_to_build_number(build_url=url)

    def delete(self,
               build_url: str = '',
               job_name: str = '',
               job_url: str = '',
               build_number: int = None,
               latest: bool = False) -> int:
        """TODO Docstring

        Args:
            TODO

        Returns:
            TODO
        """
        # TODO: Pass a list of build numbers
        if build_url:
            logger.debug(f'Build URL passed: {build_url}')
            url = build_url
        else:
            logger.debug('NO build URL passed. Getting build information ...')
            # Get build info request
            build_info = self.info(build_url, job_name, job_url, build_number, latest)
            url = build_info['url']

        # Making a direct request using the passed url
        logger.debug(f'Deleting build: {url} ...')
        request_url = f"{url.strip('/')}/doDelete"
        if not self.rest.request(request_url, 'post', is_endpoint=False)[2]:
            fail_out('Failed to delete build. Build may not exist or is queued')

        return utility.build_url_to_build_number(build_url=url)

    def stage_list(self,
                   build_url: str = '',
                   job_name: str = '',
                   job_url: str = '',
                   build_number: int = None,
                   latest: bool = False) -> Tuple[list, list]:
        """TODO Docstring

        Args:
            TODO

        Returns:
            TODO
        """
        # FIXME: yojenkins build stages --url https://localhost:8080/job/Non-PAR/job/Non-Prod-Jobs/job/Something/job/test_job/46/
        #        yields 404 in running build. Maybe issue with formatting of the url to name?

        # TODO: Pass a list of build numbers
        if not build_url:
            logger.debug('NO build URL passed. Getting build information ...')
            # Get build info request
            build_info = self.info(build_url, job_name, job_url, build_number, latest)
            build_url = build_info['url']

        # Making a direct request using the passed url
        logger.debug(f'Getting build stages for: {build_url} ...')
        request_url = f"{build_url.strip('/')}/wfapi/describe"
        return_content, _, return_success = self.rest.request(request_url, 'get', is_endpoint=False)
        if not return_success or not return_content:
            fail_out('Failed to get build stages. This may not be a staged build')

        # Getting the stage items
        # FIXME: When --url <job> and no build number is passed, it will just get the job describe, not build info
        if 'stages' in return_content:
            build_stage_list = return_content['stages']
        else:
            fail_out('Failed to find "stages" key in build info. This may not be a staged build')

        # Add additional derived information for each step
        for stage_info in build_stage_list:
            stage_info['startDatetime'] = datetime.fromtimestamp(stage_info["startTimeMillis"] /
                                                                 1000.0).strftime("%A, %B %d, %Y %I:%M:%S")
            stage_info['durationFormatted'] = str(timedelta(seconds=stage_info["durationMillis"] / 1000.0))[:-3]
            stage_info['pauseDurationFormatted'] = str(timedelta(seconds=stage_info["pauseDurationMillis"] / 1000.0))
            stage_info['url'] = stage_info['_links']['self']['href']

        # Getting only the names of the stages
        build_stage_name_list = [stage['name'] for stage in build_stage_list]

        return build_stage_list, build_stage_name_list

    def artifact_list(self,
                      build_url: str = '',
                      job_name: str = '',
                      job_url: str = '',
                      build_number: int = None) -> List[dict]:
        """TODO Docstring

        Args:
            TODO

        Returns:
            TODO
        """
        # Test on build with artifacts
        return self.info(build_url=build_url, job_name=job_name, job_url=job_url,
                         build_number=build_number).get('artifacts')

    def artifact_download(self):
        """TODO Docstring

        Args:
            TODO

        Returns:
            TODO
        """
        # TODO: Test on build with artifacts
        pass

    def logs(self,
             build_url: str = '',
             job_name: str = '',
             job_url: str = '',
             build_number: int = None,
             latest: bool = False,
             tail: float = None,
             download_dir: str = '',
             follow: bool = False) -> bool:
        """TODO Docstring

        Args:
            TODO

        Returns:
            TODO
        """
        if build_url:
            logger.debug(f'Build URL passed: {build_url}')
            url = build_url
        else:
            logger.debug('NO build URL passed. Getting build information through job ...')
            # Get build info request
            build_info = self.info(job_name=job_name, job_url=job_url, build_number=build_number, latest=latest)
            url = build_info['url']

        # FIXME: Check if this is an actual build

        request_url = f"{url.strip('/')}/consoleText"

        if download_dir:
            # Download to local file
            auth = requests.auth.HTTPBasicAuth(self.rest.username, self.rest.api_token)
            filename = f'build-logs_{datetime.now().strftime("%m-%d-%Y_%I-%M-%S")}{self.build_logs_extension}'
            logger.debug(f'Downloading console text logs to local file "{filename}" ...')
            try:
                with requests.get(request_url, auth=auth, stream=True, timeout=10) as open_request:
                    open_request.raise_for_status()
                    with open(os.path.join(download_dir, filename), 'wb') as open_file:
                        for chunk in open_request.iter_content(chunk_size=8192):
                            if chunk:
                                open_file.write(chunk)
                logger.debug('Successfully download build logs to file')
            except Exception as error:
                fail_out(f'Failed to download or save logs for build. Exception: {error}')
        else:
            # Stream the logs to console
            if not follow:
                logger.debug('Fetching logs from server ...')
                return_content, _, return_success = self.rest.request(request_url,
                                                                      'get',
                                                                      is_endpoint=False,
                                                                      json_content=False)
                if not return_success or not return_content:
                    fail_out('Failed to get console logs. Build may not exist or is queued')

                # If tail/last part of the log was specified
                if tail:
                    logger.debug(f'--tail option specified with value of: {tail}')
                    tail = abs(tail)
                    logs_list = list(map(lambda num: num.strip(), return_content.splitlines()))
                    number_of_lines = round(len(logs_list) * tail) if tail < 1 else round(tail)
                    start_log_number = 0 if number_of_lines > len(logs_list) else len(logs_list) - number_of_lines
                    return_content = os.linesep.join(list(islice(logs_list, start_log_number, None)))
                    logger.debug(f'Only printing out last logs, lines {start_log_number} to {len(logs_list)} ...')

                logger.debug('Printing out console text logs ...')
                print2(return_content)
            else:
                logger.debug('Following/streaming logs from server ...')
                logger.debug(
                    'NOTE: Jenkins server does not support requesting partial byte ranges, MUST download entire log to get log message differences'
                )
                auth = requests.auth.HTTPBasicAuth(self.rest.username, self.rest.api_token)
                old_dict = {}
                fetch_number = 1
                try:
                    while True:
                        # FIXME: Preserve already used session!  Use Rest object
                        response = requests.head(request_url, auth=auth)
                        if 'content-length' not in response.headers:
                            fail_out(
                                f'Failed to find "content-length" key in server response headers: {response.headers}')
                        content_length_sample_1 = int(response.headers['Content-Length'])
                        sleep(1)
                        response = requests.head(request_url, auth=auth)
                        content_length_sample_2 = int(response.headers['Content-Length'])

                        content_length_diff = content_length_sample_2 - content_length_sample_1
                        if content_length_diff:
                            logger.debug(
                                f'FETCH {fetch_number}: Content length difference: {content_length_diff} bytes')
                            return_content, _, return_success = self.rest.request(request_url,
                                                                                  'get',
                                                                                  is_endpoint=False,
                                                                                  json_content=False)
                            # new_dict = dict.fromkeys([ x for x in (line.strip() for line in return_content.splitlines()) if x ])
                            new_dict = dict.fromkeys(list(map(lambda num: num.strip(), return_content.splitlines())))

                            diff = dict.fromkeys(x for x in new_dict if x not in old_dict)
                            diff_list = list(diff.keys())
                            diff_text = os.linesep.join(diff_list)

                            old_dict = new_dict
                            fetch_number += 1

                            print2(diff_text)
                        else:
                            logger.debug('NO content length difference')
                except KeyboardInterrupt:
                    logger.debug('Keyboard Interrupt (CTRL-C) by user. Stopping log following ...')
        return True

    def browser_open(self,
                     build_url: str = '',
                     job_name: str = '',
                     job_url: str = '',
                     build_number: int = None,
                     latest: bool = False) -> bool:
        """TODO Docstring

        Args:
            TODO

        Returns:
            TODO
        """
        # Need URL
        if build_url:
            logger.debug(f'Build URL passed: {build_url}')
            build_url = build_url.strip('/')
        else:
            logger.debug('NO build URL passed. Getting build information ...')
            build_info = self.info(build_url, job_name, job_url, build_number, latest)
            build_url = build_info['url']

        # Open the build in browser
        logger.debug(f'Opening build in web browser: "{build_url}" ...')
        success = utility.browser_open(url=build_url)
        if not success:
            fail_out('Failed to open build in web browser')
        logger.debug('Successfully opened build in web browser')

        return success

    def monitor(self,
                build_url: str = '',
                job_name: str = '',
                job_url: str = '',
                build_number: int = None,
                latest: bool = False,
                sound: bool = False) -> bool:
        """TODO Docstring

        Args:
            TODO

        Returns:
            TODO
        """
        if build_url:
            logger.debug(f'Build URL passed: {build_url}')
            if not self.rest.request(f"{build_url.strip('/')}/api/json", 'head', is_endpoint=False)[0]:
                fail_out(f'Failed to find build. The build may not exist: {build_url}')
            url = build_url
        else:
            logger.debug('NO build URL passed. Getting build information ...')
            build_info = self.info(build_url, job_name, job_url, build_number, latest)
            url = build_info['url']

        logger.debug(f'Starting monitor for: "{url}" ...')
        success = self.build_monitor.monitor_start(build_url=url, sound=sound)
        if not success:
            fail_out('Failed to start build monitor')
        logger.debug('Successfully started build monitor')

        return success

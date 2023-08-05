#!/usr/bin/env python3

import json
import logging
import sys

import click
import xmltodict

from yojenkins.cli import cli_utility as cu
from yojenkins.cli.cli_utility import log_to_history
from yojenkins.utility.utility import print2

# Getting the logger reference
logger = logging.getLogger()


@log_to_history
def info(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool, profile: str, folder: str) -> None:
    """Folder information

    Args:
        TODO

    Returns:
        None
    """
    yj_obj = cu.config_yo_jenkins(profile)
    if cu.is_full_url(folder):
        data = yj_obj.folder.info(folder_url=folder)
    else:
        data = yj_obj.folder.info(folder_name=folder)
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)


@log_to_history
def search(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool, profile: str, search_pattern: str,
           search_folder: str, depth: int, fullname: bool, opt_list: bool) -> None:
    """Search folders by REGEX pattern

    Args:
        TODO

    Returns:
        None
    """
    yj_obj = cu.config_yo_jenkins(profile)
    if cu.is_full_url(search_folder):
        data, data_list = yj_obj.folder.search(search_pattern=search_pattern,
                                               folder_url=search_folder,
                                               folder_depth=depth,
                                               fullname=fullname)
    else:
        data, data_list = yj_obj.folder.search(search_pattern=search_pattern,
                                               folder_name=search_folder,
                                               folder_depth=depth,
                                               fullname=fullname)
    if not data:
        print2("No folders found", color="yellow")
        sys.exit(1)
    data = data_list if opt_list else data
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)


@log_to_history
def subfolders(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool, profile: str, folder: str,
               opt_list: bool) -> None:
    """List all subfolders in folder

    Args:
        TODO

    Returns:
        None
    """
    yj_obj = cu.config_yo_jenkins(profile)
    if cu.is_full_url(folder):
        data, data_list = yj_obj.folder.subfolder_list(folder_url=folder)
    else:
        data, data_list = yj_obj.folder.subfolder_list(folder_name=folder)
    data = data_list if opt_list else data
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)


@log_to_history
def jobs(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool, profile: str, folder: str,
         opt_list: bool) -> None:
    """List all jobs in folder

    Args:
        TODO

    Returns:
        None
    """
    yj_obj = cu.config_yo_jenkins(profile)
    if cu.is_full_url(folder):
        data, data_list = yj_obj.folder.jobs_list(folder_url=folder)
    else:
        data, data_list = yj_obj.folder.jobs_list(folder_name=folder)
    data = data_list if opt_list else data
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)


@log_to_history
def views(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool, profile: str, folder: str,
          opt_list: int) -> None:
    """List all views in folder

    Args:
        TODO

    Returns:
        None
    """
    yj_obj = cu.config_yo_jenkins(profile)
    if cu.is_full_url(folder):
        data, data_list = yj_obj.folder.view_list(folder_url=folder)
    else:
        data, data_list = yj_obj.folder.view_list(folder_name=folder)
    data = data_list if opt_list else data
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)


@log_to_history
def items(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool, profile: str, folder: str,
          opt_list: int) -> None:
    """List all items in folder

    Args:
        TODO

    Returns:
        None
    """
    yj_obj = cu.config_yo_jenkins(profile)
    if cu.is_full_url(folder):
        data, data_list = yj_obj.folder.item_list(folder_url=folder)
    else:
        data, data_list = yj_obj.folder.item_list(folder_name=folder)
    data = data_list if opt_list else data
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)


@log_to_history
def browser(profile: str, folder: str) -> None:
    """Open folder in web browser

    Args:
        TODO

    Returns:
        None
    """
    yj_obj = cu.config_yo_jenkins(profile)
    if cu.is_full_url(folder):
        yj_obj.folder.browser_open(folder_url=folder)
    else:
        yj_obj.folder.browser_open(folder_name=folder)


@log_to_history
def config(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool, opt_json: bool, profile: str, folder: str,
           filepath: str) -> None:
    """Get folder configuration

    Args:
        TODO

    Returns:
        None
    """
    yj_obj = cu.config_yo_jenkins(profile)
    if cu.is_full_url(folder):
        data = yj_obj.folder.config(filepath=filepath,
                                    folder_url=folder,
                                    opt_json=opt_json,
                                    opt_yaml=opt_yaml,
                                    opt_toml=opt_toml)
    else:
        data = yj_obj.folder.config(filepath=filepath,
                                    folder_name=folder,
                                    opt_json=opt_json,
                                    opt_yaml=opt_yaml,
                                    opt_toml=opt_toml)
    # Converting XML to dict
    # data = json.loads(json.dumps(xmltodict.parse(data)))

    opt_xml = not any([opt_json, opt_yaml, opt_toml])
    data = data if opt_xml else json.loads(json.dumps(xmltodict.parse(data)))
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)


@log_to_history
def create(profile: str, name: str, folder: str, type: str, config: str, config_is_json: bool) -> None:
    """Create an item

    Args:
        TODO

    Returns:
        None
    """
    # TODO: Maybe return the newly created item url

    yj_obj = cu.config_yo_jenkins(profile)
    if cu.is_full_url(folder):
        data = yj_obj.folder.create(name=name,
                                    type=type,
                                    config=config,
                                    folder_url=folder,
                                    config_is_json=config_is_json)
    else:
        data = yj_obj.folder.create(name=name,
                                    type=type,
                                    config=config,
                                    folder_name=folder,
                                    config_is_json=config_is_json)
    click.echo(click.style('success', fg='bright_green', bold=True))


@log_to_history
def copy(profile: str, folder: str, original_name: str, new_name: str) -> None:
    """Copy an existing item

    Args:
        TODO

    Returns:
        None
    """
    # TODO: Maybe return the newly copied item url

    yj_obj = cu.config_yo_jenkins(profile)
    if cu.is_full_url(folder):
        data = yj_obj.folder.copy(original_name=original_name, new_name=new_name, folder_url=folder)
    else:
        data = yj_obj.folder.copy(original_name=original_name, new_name=new_name, folder_name=folder)
    click.echo(click.style('success', fg='bright_green', bold=True))


@log_to_history
def delete(profile: str, folder: str) -> None:
    """Delete folder or view

    Args:
        TODO

    Returns:
        None
    """
    yj_obj = cu.config_yo_jenkins(profile)
    if cu.is_full_url(folder):
        data = yj_obj.folder.delete(folder_url=folder)
    else:
        data = yj_obj.folder.delete(folder_name=folder)
    click.echo(click.style('success', fg='bright_green', bold=True))

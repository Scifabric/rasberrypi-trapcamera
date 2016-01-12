#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of PyBOSSA.
#
# PyBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBOSSA.  If not, see <http://www.gnu.org/licenses/>.
"""
A trap camera command line tool.

This tool allows you to take pictures and create tasks in a PyBossa server:


"""

import click
import pbclient
import ConfigParser
import os.path
import shutil
from os.path import expanduser
from helpers import *


class Config(object):

    """Config class for the command line."""

    def __init__(self):
        """Init the configuration default values."""
        self.verbose = False
        self.server = None
        self.api_key = None
        self.project = None
        self.flickr_api = None
        self.flickr_secret = None
        self.flickr_license_id = 4
        self.flickr_photoset_name = 'PyBossa Rasberry'
        self.parser = ConfigParser.ConfigParser()
        self.offline = 'offline'
        self.data = 'data'
        self.pbclient = None

pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--config-file', help='Config file')
@click.option('--flickr-api', help='Your Flickr API key')
@click.option('--flickr-secret', help='Your Flickr API secret')
@click.option('--pybossa-api', help='Your PYBOSSA API key')
@click.option('--pybossa-server', help='The PYBOSSA server')
@click.option('--pybossa-project', help='The PYBOSSA project ID')
@pass_config
def cli(config, config_file, flickr_api, flickr_secret,
        pybossa_api, pybossa_server, pybossa_project):
    """Create the cli command line."""
    import flickrapi
    home = expanduser("~")
    if os.path.isfile(os.path.join(home, '.trapcamera.cfg')):
        # FLICKR config
        config.parser.read(os.path.join(home, '.trapcamera.cfg'))
        config.flickr_api = config.parser.get('flickr', 'api')
        config.flickr_secret = config.parser.get('flickr', 'secret')
        config.flickr_license_id = config.parser.get('flickr', 'license_id')
        config.flickr_photoset_name = config.parser.get('flickr',
                                                        'photoset_name')
        # DATA config
        config.offline = config.parser.get('data', 'offline')
        config.data = config.parser.get('data', 'images')
        # PYBOSSA config
        config.pybossa_api = config.parser.get('pybossa', 'api_key')
        config.pybossa_server = config.parser.get('pybossa', 'endpoint')
        config.pybossa_project = config.parser.get('pybossa', 'project_id')
        # CAMERA config
        config.camera_sharpness = config.parser.get('camera', 'sharpness')
        config.camera_contrast = config.parser.get('camera', 'contrast')
        config.camera_brightness = config.parser.get('camera', 'brightness')
        config.camera_saturation = config.parser.get('camera', 'saturation')
        config.camera_iso = config.parser.get('camera', 'ISO')
        config.camera_video_stabilization = config.parser.get('camera',
                                                              'video_stabilization')
        config.camera_exposure_compensation = config.parser.get('camera', 'exposure_compensation')
        config.camera_exposure_mode = config.parser.get('camera', 'exposure_mode')
        config.camera_meter_mode = config.parser.get('camera', 'meter_mode')
        config.camera_awb_mode = config.parser.get('camera', 'awb_mode')
        config.camera_image_effects = config.parser.get('camera', 'image_effects')
        config.camera_color_effects = config.parser.get('camera', 'color_effects')
        config.camera_rotation = config.parser.get('camera', 'rotation')
        config.camera_hflip = config.parser.get('camera', 'hflip')
        config.camera_vflip = config.parser.get('camera', 'vflip')
        config.camera_crop = config.parser.get('camera', 'crop')
        config.camera_resolution = config.parser.get('camera', 'resolution')
    if flickr_api:
        config.flickr_api = flickr_api
    if flickr_secret:
        config.flickr_secret = flickr_secret

    config.flickrapi = flickrapi.FlickrAPI(config.flickr_api,
                                           config.flickr_secret,
                                           format='parsed-json')

    pbclient.set('endpoint', config.pybossa_server)
    pbclient.set('api_key', config.pybossa_api)

    config.pbclient = pbclient


@cli.command()
@pass_config
def capture(config):
    """Capture one picture."""
    messages, file_name = _capture(config)
    for msg in messages:
        click.secho(msg['msg'], fg=msg['fg'])


@cli.command()
@pass_config
def authenticate(config):
    """Authenticate user in Flickr."""
    config.flickrapi.authenticate_via_browser(perms='write')


@cli.command()
@click.option('--photofile', help="Photo file name to upload to Flickr.")
@pass_config
def upload(config, photofile):
    """Upload picture to Flickr."""
    _upload_photo(config, photofile)


@cli.command()
@click.option('--photoid', help='Photo ID to change the license')
@click.option('--licenseid', help='License ID to change the license', default=4)
@pass_config
def set_license(config, photoid, licenseid):
    """Set photo license."""
    license = config.flickr_license_id
    if licenseid:
        license = licenseid
    rsp = _set_license(config.flickrapi, photoid, license)
    msg = "Status: %s" % rsp['stat']
    click.secho(msg, fg='green')


@cli.command()
@click.option('--photoset', help='Photoset name')
@click.option('--primaryphotoid',
              help='Primary photo ID for cover of the photoset')
@pass_config
def create_photoset(config, photoset, primaryphotoid):
    """Create photoset."""
    photoset_name = config.flickr_photoset_name
    if photoset:
        photoset_name = photoset
    rsp = _create_photoset(config.flickrapi, photoset_name, primaryphotoid)
    msg = "Status: %s" % rsp['stat']
    click.secho(msg, fg='green')


@cli.command()
@click.option('--photoid')
@pass_config
def create_task(config, photoid):
    """Create a task for a given photo ID."""
    if connected_to_internet():
        task = _create_task(config, photoid)
        msg = "PyBossa Task created. ID: %s" % task.id
        click.secho(msg, fg='green')
    else:
        msg = "WARNING: No Internet connection"
        click.secho(msg, fg='yellow')


@cli.command()
@click.option('--photofile')
@pass_config
def capture_upload_task(config, photofile):
    """Capture, upload and create a task for a photo file."""
    if connected_to_internet():
        messages, file_name = _capture(config)
        rsp = _upload_photo(config, file_name)
        task = _create_task(config, rsp['photo_id'])
        msg = "PyBossa Task created. ID: %s" % task.id
        click.secho(msg, fg='green')
    else:
        _create_folder(config.offline)
        shutil.copy(photofile, config.offline)


@cli.command()
@pass_config
def upload_task_pending(config):
    """Upload and create tasks for pending photos."""
    if connected_to_internet():
        img_files = [os.path.join(config.data, f)
                     for f in os.listdir(config.data)
                     if os.path.isfile(os.path.join(config.data, f))]
        if len(img_files) > 0:
            with click.progressbar(img_files,
                                   label="Uploading and creating task for  \
                                   pending images",
                                   ) as bar:
                for f in bar:
                    rsp = _upload_photo(config, f)
                    _create_task(config, rsp['photo_id'])
        else:
            msg = "WARNING: No files to upload. Images folder is empty."
            click.secho(msg, fg='yellow')

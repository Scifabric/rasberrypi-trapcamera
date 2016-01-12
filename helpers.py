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
import os
import uuid
import requests
try: # pragma: no cover
    import picamera
    from picamera.exc import PiCameraValueError
except:
    print "PiCamera not available"
    picamera = None
    PiCameraValueError = ValueError

__all__ = ['_set_license', '_create_photoset', '_get_photoset_id',
           '_add_photo_to_photoset', '_get_photo_urls', '_create_task',
           'connected_to_internet', '_upload_photo', '_create_task',
           '_create_folder', '_set_photo_name', '_get_stock_photo',
           '_capture']


def connected_to_internet(url='http://www.google.com/', timeout=5):
    try:
        tmp = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False


def _set_license(flickr, photoid, licenseid):
    """Set photo license id."""
    rsp = flickr.photos.licenses.setLicense(photo_id=photoid,
                                            license_id=licenseid)
    return rsp


def _get_photoset_id(flickr, photoset):
    """Return photoset ID."""
    rsp = flickr.photosets.getList(per_page=500)
    for s in rsp['photosets']['photoset']:
        if s['title']['_content'] == photoset:
            return s['id']
    return None


def _create_photoset(flickr, photoset, primary_photo_id):
    """Create photoset."""
    photoset_id = _get_photoset_id(flickr, photoset)
    if photoset_id is None:
        rsp = flickr.photosets.create(title=photoset,
                                      primary_photo_id=primary_photo_id)
        return rsp
    else:
        return dict(stat='exists', photoset_id=photoset_id)


def _add_photo_to_photoset(flickr, photosetid, photoid):
    """Add photo to photoset."""
    rsp = flickr.photosets.addPhoto(photoset_id=photosetid,
                                    photo_id=photoid)
    return rsp


def _upload_photo(config, photofile):
    """Upload a photo to Flickr."""
    photoset_id = _get_photoset_id(config.flickrapi,
                                   config.flickr_photoset_name)
    resp = config.flickrapi.upload(filename=photofile,
                                   title='Example',
                                   descriptoin='Description',
                                   tags='pybossa',
                                   is_public='0',
                                   format='etree')
    # print "status: %s" % resp.attrib['stat']
    photo_id = resp.findall('photoid')[0].text
    if photo_id:
        _create_folder(config.offline)
        name = "%s.task.pending" % photo_id
        name = os.path.join(config.offline, name)
        open(name, 'a').close()
    # print "photo ID: %s" % photo_id
    _set_license(config.flickrapi, photo_id, config.flickr_license_id)

    # Check if a photoset exists otherwise create it first
    if photoset_id is None:
        rsp = _create_photoset(config.flickrapi,
                               photoset=config.flickr_photoset_name,
                               primary_photo_id=photo_id)
    else:
        rsp = _add_photo_to_photoset(config.flickrapi, photoset_id, photo_id)
    rsp['photo_id'] = photo_id
    if rsp['stat'] == 'ok':
        os.remove(photofile)
    return rsp


def _get_photo_urls(flickr, photo_id):
    """Return a dict with photo URLs."""
    rsp = flickr.photos.getInfo(photo_id=photo_id)
    urls = dict(url_m=None, url_s=None, url_t=None,
                url_b=None, url_z=None, url_o=None)
    sizes = "mstzbo"
    photo = rsp['photo']
    url = "https://farm%s.staticflickr.com/%s/%s_%s_%s.jpg"
    url_o = "https://farm%s.staticflickr.com/%s/%s_%s_o.%s"
    for s in sizes:
        if s != 'o':
            photo_url = url % (photo['farm'], photo['server'],
                               photo['id'], photo['secret'], s)
        else:
            photo_url = url_o % (photo['farm'], photo['server'],
                                 photo['id'], photo['originalsecret'],
                                 photo['originalformat'])
        urls['url_' + s] = photo_url
    rsp['photo_urls'] = urls
    return rsp


def _create_task(config, photoid):
    """Create a PYBOSSA task for a photo."""
    data = _get_photo_urls(config.flickrapi, photoid)
    task_info = dict()
    task_info = data['photo_urls']
    task = config.pbclient.create_task(config.pybossa_project, task_info)
    if task is not None:
        name = '%s.task.pending' % photoid
        os.remove(os.path.join(config.offline, name))
    return task


def _create_folder(folder):
    """Create folder if it does not exists."""
    if not os.path.exists(folder):
        os.makedirs(folder)


def _set_photo_name(folder):
    """Return photo name for captured image."""
    _create_folder(folder)
    file_name = str(uuid.uuid4())
    file_name = os.path.join(folder, file_name) + '.jpg'
    return file_name


def _get_stock_photo(file_name):
    """Download stock photo."""
    url = 'http://scifabric.com/images/citiesatnight-facebookcard.png'
    # Use PNG
    file_name = file_name.replace('.jpg', '.png')
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:  # pragma: no cover
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return file_name


def _setup_camera(config, camera):
    """Configure camera."""
    camera.sharpness = config.camera_sharpness
    camera.contrast = config.camera_contrast
    camera.brightness = config.camera_brightness
    camera.saturation = config.camera_saturation
    camera.ISO = config.camera_iso
    camera.video_stabilization = config.camera_video_stabilization
    camera.exposure_compensation = config.camera_exposure_compensation
    camera.exposure_mode = config.camera_exposure_mode
    camera.meter_mode = config.camera_meter_mode
    camera.awb_mode = config.camera_awb_mode
    camera.image_effect = config.camera_image_effect
    camera.color_effects = config.camera_color_effects
    camera.rotation = config.camera_rotation
    camera.hflip = config.camera_hflip
    camera.vflip = config.camera_vflip
    camera.crop = config.camera_crop
    camera.resolution = config.camera_resolution
    return camera


def _capture(config):
    """Capture a photo and save it to a file."""
    messages = []
    try:
        with picamera.PiCamera() as camera:
            camera = _setup_camera(config, camera)
            file_name = _set_photo_name(config.data)
            camera.capture(file_name)
            msg = dict(msg="Image captured: %s" % file_name, fg='green')
            messages.append(msg)
    except (PiCameraValueError, ValueError) as e:
        msg = "ERROR: PiCamera %s" % e.message
        messages.append(dict(msg=msg, fg='red'))
        file_name = None
    except:
        messages.append(dict(msg="ERROR: PiCamera not working properly",
                             fg='red'))
        messages.append(dict(msg="INFO: Using a stock image as the captured one.",
                    fg='yellow'))
        file_name = _set_photo_name(config.data)
        file_name = _get_stock_photo(file_name)
        msg = "Image captured: %s" % file_name
        messages.append(dict(msg=msg, fg='green'))
    return messages, file_name

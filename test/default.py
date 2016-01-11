"""Test module for trapcamera client."""
from mock import MagicMock
import ConfigParser
import pbclient
import xml.etree.ElementTree as ET


class TestDefault(object):

    """Test class for trapcamera.helpers."""

    config = MagicMock()
    config.server = 'http://server'
    config.api_key = 'apikey'
    config.project = 1
    config.flickr_api = 'flickr'
    config.flickr_secret = 'secret'
    config.flickr_license_id = 4
    config.flickr_photoset_name = 'PyBossa Rasberry'
    config.parser = ConfigParser.ConfigParser()
    config.offline = 'offline'
    config.data = 'data'
    config.pbclient = MagicMock()
    config.flickrapi = MagicMock()

    photoset_list = { "photosets": { "cancreate": 1, "page": 1, "pages": 1, "perpage": 500, "total": 21,
                                    "photoset": [
                                        { "id": "1", "primary": "1", "secret": "secret", "server": "1", "farm": 1, "photos": 1, "videos": 0,
                                         "title": { "_content": "Raspberry" },
                                         "description": { "_content": "" }, "needs_interstitial": 0, "visibility_can_see_set": 1, "count_views": 0, "count_comments": 0, "can_comment": 1, "date_create": "1452001703", "date_update": "1452517064" },
                                    ] }, "stat": "ok" }

    photo_upload_rest = ET.fromstring('<?xml version="1.0" encoding="utf-8" ?><rsp stat="ok"><photoid>1</photoid></rsp>')

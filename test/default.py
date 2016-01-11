"""Test module for trapcamera client."""
from mock import MagicMock
import ConfigParser
import pbclient


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
    config.pbclient = pbclient

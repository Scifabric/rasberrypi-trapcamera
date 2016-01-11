"""Test module for pbs client."""
import pbclient
from default import TestDefault
from helpers import *
from mock import patch, MagicMock
from nose.tools import assert_raises


class TestHelpers(TestDefault):

    """Test class for trapcamera.helpers."""

    def test_connected_to_internet(self):
        """Test connected to internet works."""
        url = 'http://somethingwrong.comu'
        assert connected_to_internet()
        assert connected_to_internet(url) is False

    def test_set_license(self):
        """Test set_license method works."""
        flickr = MagicMock()
        flickr.photos.licenses.setLicense.return_value = dict(stat='ok')
        resp = _set_license(flickr, 1, 4)
        flickr.photos.licenses.setLicense.assert_called_with(photo_id=1,
                                                             license_id=4)
        assert resp['stat'] == 'ok', resp

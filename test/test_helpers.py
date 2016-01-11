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

    def test_getphoset_id_returns_ID(self):
        """Test getphotoset_id returns a photoset ID."""
        flickr = MagicMock()
        flickr.photosets.getList.return_value = self.photoset_list
        resp = _get_photoset_id(flickr, "Raspberry")
        assert resp == "1", resp

    def test_getphoset_id_returns_none(self):
        """Test getphotoset_id returns NONE when not found."""
        flickr = MagicMock()
        flickr.photosets.getList.return_value = self.photoset_list
        resp = _get_photoset_id(flickr, "Something")
        assert resp == None, resp

    @patch('helpers._get_photoset_id')
    def test_create_photoset(self, mock):
        """Test create_photoset method works."""
        mock.return_value = None
        flickr = MagicMock()
        flickr.photosets.create.return_value = dict(stat='ok')
        resp = _create_photoset(flickr, "Raspberry", 1)
        flickr.photosets.create.assert_called_with(title='Raspberry',
                                                   primary_photo_id=1)
        assert resp['stat'] == 'ok'

    @patch('helpers._get_photoset_id')
    def test_create_photoset_exists(self, mock):
        """Test create_photoset exists method works."""
        mock.return_value = 1
        flickr = MagicMock()
        resp = _create_photoset(flickr, "Raspberry", 1)
        assert resp['stat'] == 'exists', resp
        assert resp['photoset_id'] == 1, resp


    def test_add_photo_to_photoset(self):
        """Test add photo to photoset works."""
        flickr = MagicMock()
        flickr.photosets.addPhoto.return_value = dict(stat='ok')
        resp = _add_photo_to_photoset(flickr, 1, 1)
        flickr.photosets.addPhoto.assert_called_with(photoset_id=1, photo_id=1)
        assert resp['stat'] == 'ok', resp

    @patch('helpers.os.remove')
    @patch('helpers._add_photo_to_photoset', return_value=dict(stat='ok'))
    @patch('helpers._set_license', return_value=dict(stat='ok'))
    @patch('helpers._get_photoset_id', return_value="1")
    def test_upload_photo(self, mock_get_photoset_id, mock_set_license,
                          mock_add_photo_to_photoset, mock_os):
        """Test upload_photo method works."""
        self.config.flickrapi = MagicMock()
        self.config.flickrapi.upload.return_value = self.photo_upload_rest
        resp = _upload_photo(self.config, "1")
        assert resp['stat'] == 'ok', resp
        mock_get_photoset_id.assert_called_with(self.config.flickrapi,
                                                self.config.flickr_photoset_name)
        mock_add_photo_to_photoset.assert_called_with(self.config.flickrapi,
                                                      '1', '1')
        mock_set_license.assert_called_with(self.config.flickrapi, '1', 4)
        mock_os.assert_called_with('1')

    @patch('helpers._create_photoset', return_value=dict(stat='ok'))
    @patch('helpers.os.remove')
    @patch('helpers._add_photo_to_photoset', return_value=dict(stat='ok'))
    @patch('helpers._set_license', return_value=dict(stat='ok'))
    @patch('helpers._get_photoset_id', return_value=None)
    def test_upload_photo_without_photoset(self, mock_get_photoset_id,
                                           mock_set_license,
                                           mock_add_photo_to_photoset,
                                           mock_os,
                                           mock_create_photoset):
        """Test upload_photo method works."""
        self.config.flickrapi = MagicMock()
        self.config.flickrapi.upload.return_value = self.photo_upload_rest
        resp = _upload_photo(self.config, "1")
        assert resp['stat'] == 'ok', resp
        mock_get_photoset_id.assert_called_with(self.config.flickrapi,
                                                self.config.flickr_photoset_name)
        mock_create_photoset.assert_called_with(self.config.flickrapi,
                                                photoset=self.config.flickr_photoset_name,
                                                primary_photo_id='1')
        mock_set_license.assert_called_with(self.config.flickrapi, '1', 4)
        mock_os.assert_called_with('1')

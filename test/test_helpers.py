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

    def test_get_photo_urls(self):
        """Test get_photo_urls works."""
        flickr = MagicMock()
        flickr.photos.getInfo.return_value = dict(photo=dict(farm=1, server=1, id=1,
                                                  secret='secret',
                                                  originalsecret='o',
                                                  originalformat='jpg'))
        resp = _get_photo_urls(flickr, 1)
        sizes = "mstzbo"
        for s in sizes:
            url = 'url_%s' % s
            assert url in resp['photo_urls'].keys(), url
            if s != 'o':
                photo_url = 'https://farm1.staticflickr.com/1/1_secret_%s.jpg' % s
            else:
                photo_url = 'https://farm1.staticflickr.com/1/1_o_%s.jpg' % s
            assert resp['photo_urls'][url] == photo_url, resp['photo_urls'][url]

    @patch('helpers.os.remove')
    def test_create_task(self, mock):
        """Test create_task works."""
        flickr = MagicMock()
        flickr.photos.getInfo.return_value = dict(photo=dict(farm=1, server=1, id=1,
                                                  secret='secret',
                                                  originalsecret='o',
                                                  originalformat='jpg'))
        Task = MagicMock()
        Task.id = 1
        self.config.pbclient.create_task.return_value = Task
        resp = _create_task(self.config, 1)
        assert resp.id == Task.id, resp

    @patch('helpers.os.remove')
    def test_create_task_fails(self, mock):
        """Test create_task fails works."""
        flickr = MagicMock()
        flickr.photos.getInfo.return_value = dict(photo=dict(farm=1, server=1, id=1,
                                                  secret='secret',
                                                  originalsecret='o',
                                                  originalformat='jpg'))
        self.config.pbclient.create_task.return_value = None
        resp = _create_task(self.config, 1)
        assert resp is None

    @patch('helpers.os.makedirs')
    def test_create_folder(self, mock):
        """Test create_folder works."""
        name = '/tmp/aasdfadfa/'
        _create_folder(name)
        mock.assert_called_with(name)

    @patch('helpers.uuid.uuid4', return_value='uuid4')
    @patch('helpers._create_folder')
    def test_set_photo_name(self, mock, mock_uuid):
        """Test set_photo_name works."""
        name = 'folder'
        resp = _set_photo_name(name)
        expected = '%s/%s' % (name, 'uuid4.jpg')
        assert  resp == expected, resp


    @patch('helpers.requests.get')
    def test_get_stock_photo(self, mock):
        """Test get_stock_photo works."""
        url = 'http://scifabric.com/images/citiesatnight-facebookcard.png'
        resp = _get_stock_photo('foo.jpg')
        assert resp == 'foo.png', resp
        mock.assert_called_with(url, stream=True)

    @patch('helpers._set_photo_name', return_value='foo.jpg')
    @patch('helpers.picamera')
    def test_capture(self, mock_picamera, mock):
        """Test capture works."""
        messages, file_name = _capture(self.config)
        assert file_name == 'foo.jpg', file_name
        mock.assert_called_with(self.config.data)
        assert mock_picamera.PiCamera.called
        for msg in messages:
            assert msg['msg'] == "Image captured: foo.jpg", resp

    @patch('helpers._set_photo_name', return_value='foo.jpg')
    @patch('helpers._get_stock_photo', return_value='foo.png')
    def test_capture_no_picamera(self, mock_stock, mock_set):
        """Test capture without picamera works."""
        messages, file_name = _capture(self.config)
        assert file_name == 'foo.png', file_name
        assert len(messages) == 3, messages
        assert messages[2]['msg'] == "Image captured: foo.png", resp

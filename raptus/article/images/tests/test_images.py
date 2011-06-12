# -*- coding: utf-8 -*-
"""Tests for utility methods for retrieving Article's images. """

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.images.tests.base import RAImagesIntegrationTestCase

import mock
import unittest2 as unittest


class TestGetImages(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.images.images.Images.getImages().
    """

    @mock.patch('raptus.article.images.images.getToolByName')
    def test_path(self, getToolByName):
        """Test that path parameter is correctly assembled."""
        from raptus.article.images.images import Images

        context = mock.Mock(spec='getPhysicalPath'.split())
        context.getPhysicalPath.return_value = ['foo', 'bar']

        Images(context).getImages()
        getToolByName.return_value.assert_called_once_with(portal_type='Image', sort_on='getObjPositionInParent',
                                                           path={'query': 'foo/bar', 'depth': 1})

    @mock.patch('raptus.article.images.images.getToolByName')
    def test_kwargs(self, getToolByName):
        """Test that **kwargs are used in catalog() call."""
        from raptus.article.images.images import Images

        context = mock.sentinel.context
        context = mock.Mock(spec='getPhysicalPath'.split())
        context.getPhysicalPath.return_value = []

        Images(context).getImages(foo='bar')
        getToolByName.return_value.assert_called_once_with(portal_type='Image', sort_on='getObjPositionInParent',
                                                           path={'query': '', 'depth': 1}, foo='bar')


class TestGetImagesIntegration(RAImagesIntegrationTestCase):
    """Test getImages() method of raptus.article.images.images.Images."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')
        self.portal.article.invokeFactory('Image', 'image1')
        self.portal.article.invokeFactory('Image', 'image2')

    def test_get_images(self):
        """Test getting Article's images."""
        from raptus.article.images.images import Images
        images = Images(self.portal.article).getImages()
        self.assertEquals(len(images), 2)
        self.assertEquals('image1 image2'.split(), [i.id for i in images])

    def test_get_images_only_from_article(self):
        """Test that only Article's images are returned."""

        # add an Image to another Article
        self.portal.invokeFactory('Article', 'other_article')
        self.portal.other_article.invokeFactory('Image', 'other_image')

        from raptus.article.images.images import Images
        images = Images(self.portal.article).getImages()
        self.assertEquals(len(images), 2)
        self.assertEquals('image1 image2'.split(), [i.id for i in images])


class TestGetImageURL(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.images.images.Image.getImageURL().
    """

    def test_not_an_image(self):
        """Test return value when there is no image."""

        schema = {'image': mock.Mock(spec='get'.split())}
        schema['image'].get.return_value = None

        image = mock.Mock(spec='Schema'.split())
        image.Schema.return_value = schema

        from raptus.article.images.images import Image
        self.assertEquals(None, Image(image).getImageURL())

    @mock.patch('raptus.article.images.images.Image.getSize')
    def test_w_and_h_not_set(self, getSize):
        """Test return value when w and h are not set."""
        getSize.return_value = 0, 0

        schema = {'image': mock.Mock(spec='get'.split())}

        image = mock.Mock(spec='Schema absolute_url'.split())
        image.Schema.return_value = schema
        image.absolute_url.return_value = 'http://plone/image'

        from raptus.article.images.images import Image
        self.assertEquals('http://plone/image/image', Image(image).getImageURL())

    @mock.patch('raptus.article.images.images.Image.getSize')
    @mock.patch('raptus.article.images.images.component')
    def test_w_or_h_set(self, zope_component, getSize):
        """Test return value when w or h are set."""

        scale_url = 'http://plone/image/@@images/b16...fa2.jpeg'
        zope_component.getMultiAdapter.return_value.scale.return_value.url = scale_url
        getSize.return_value = 100, 100

        schema = {'image': mock.Mock(spec='get'.split())}
        image = mock.Mock(spec='Schema absolute_url REQUEST'.split())
        image.Schema.return_value = schema
        image.absolute_url.return_value = 'http://plone/image'

        from raptus.article.images.images import Image
        self.assertEquals(scale_url, Image(image).getImageURL())

    @mock.patch('raptus.article.images.images.Image.getSize')
    def test_size_is_used(self, getSize):
        """Test that size parameter is used."""

        getSize.return_value = 0, 0

        schema = {'image': mock.Mock(spec='get'.split())}
        image = mock.Mock(spec='Schema absolute_url'.split())
        image.Schema.return_value = schema

        from raptus.article.images.images import Image
        Image(image).getImageURL(size='foo')
        getSize.assert_called_one_with(size='foo')


class TestGetImage(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.images.images.Image.getImage().
    """

    @mock.patch('raptus.article.images.images.Image.getImageURL')
    def test_no_url(self, getImageURL):
        """Test return value when url is None."""

        getImageURL.return_value = None

        from raptus.article.images.images import Image
        image = mock.Mock(spec=''.split())
        self.assertEquals(None, Image(image).getImage())

    @mock.patch('raptus.article.images.images.Image.getImageURL')
    def test_size_is_used(self, getImageURL):
        """Test that size parameter is used."""

        getImageURL.return_value = None

        from raptus.article.images.images import Image
        image = mock.Mock(spec=''.split())
        Image(image).getImage(size='foo')

        getImageURL.assert_called_one_with(size='foo')

    @mock.patch('raptus.article.images.images.Image.getImageURL')
    @mock.patch('raptus.article.images.images.Image.getCaption')
    def test_get_image_tag(self, getCaption, getImageURL):
        """Test HTML image tag return value of getImage()."""

        getImageURL.return_value = "http://plone/image"
        getCaption.return_value = 'foo'

        from raptus.article.images.images import Image
        image = mock.Mock(spec=''.split())
        self.assertEquals('<img src="http://plone/image" alt="foo" />', Image(image).getImage())


class TestGetSize(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.images.images.Image.getSize().
    """

    @mock.patch('raptus.article.images.images.getToolByName')
    def test_get_size(self, getToolByName):
        """Test return value of getSize()."""
        from raptus.article.images.images import Image
        getToolByName.return_value.raptus_article.getProperty.return_value = 9

        # test result
        image = mock.Mock(spec=''.split())
        w, h = Image(image).getSize('foo')
        self.assertEquals((9, 9), (w, h))

        # test call parameters
        call_args_list = getToolByName.return_value.raptus_article.getProperty.call_args_list
        self.assertEquals(call_args_list[0], (('images_foo_width', 0), {}))
        self.assertEquals(call_args_list[1], (('images_foo_height', 0), {}))


class TestGetCaption(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.images.images.Image.getCaption().
    """

    def test_title(self):
        """Test return value when only title is set."""

        image = mock.Mock(spec='Title Description'.split())
        image.Title.return_value = 'foo'
        image.Description.return_value = None

        from raptus.article.images.images import Image
        self.assertEquals('foo', Image(image).getCaption())

    def test_description(self):
        """Test return value when only description is set."""

        image = mock.Mock(spec='Title Description'.split())
        image.Title.return_value = None
        image.Description.return_value = 'bar'

        from raptus.article.images.images import Image
        self.assertEquals('bar', Image(image).getCaption())

    def test_title_and_description(self):
        """Test that only description is returned when both title and
        description are set."""

        image = mock.Mock(spec='Title Description'.split())
        image.Title.return_value = 'foo'
        image.Description.return_value = 'bar'

        from raptus.article.images.images import Image
        self.assertEquals('bar', Image(image).getCaption())


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

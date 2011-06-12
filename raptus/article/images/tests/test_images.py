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


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

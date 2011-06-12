# -*- coding: utf-8 -*-
"""Tests how archetypes.schemaextender extends content-types."""

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.images.tests.base import RAImagesIntegrationTestCase

import unittest2 as unittest


class TestImage(RAImagesIntegrationTestCase):
    """Test extensions of Image's schema."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article', title='Raptus Article')
        self.portal.article.invokeFactory('Image', 'image', title='Image')

    def test_components_field(self):
        """Test if 'components' field is there."""
        image = self.portal.article.image
        self.assertTrue('components' in image.Schema())
        self.assertEquals('lines', image.Schema()['components'].type)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

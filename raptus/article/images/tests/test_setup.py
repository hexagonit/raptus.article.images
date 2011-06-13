# -*- coding: utf-8 -*-
"""Tests for installation and setup of this package."""

from Products.CMFCore.utils import getToolByName
from raptus.article.images.tests.base import RAImagesIntegrationTestCase

import unittest2 as unittest


class TestInstall(RAImagesIntegrationTestCase):
    """Test installation of raptus.article.images into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_product_installed(self):
        """Test if raptus.article.gallery is installed with
        portal_quickinstaller.
        """
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('raptus.article.images'))

    def test_dependencies_installed(self):
        """Test if raptus.article.images' dependencies are installed with
        portal_quickinstaller.
        """
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('raptus.article.core'))

    # propertiestool.xml
    def test_article_properties(self):
        """Test if raptus_article properties are correctly set."""

        article_props = self.portal.portal_properties.raptus_article
        self.assertEquals(article_props.images_thumb_width, 100)
        self.assertEquals(article_props.images_thumb_height, 0)
        self.assertEquals(article_props.images_popup_width, 600)
        self.assertEquals(article_props.images_popup_height, 500)

    # workflows.xml
    def test_image_has_no_workflow(self):
        """Test if Image is set to have no workflow."""
        workflow = getToolByName(self.portal, 'portal_workflow')
        for portal_type, chain in workflow.listChainOverrides():
            if portal_type in ('Image',):
                self.assertEquals((), chain)

    # types.xml
    def test_image_is_addable(self):
        """Test if Image can be added to Article."""
        types = getToolByName(self.portal, 'portal_types')
        self.assertIn('Image', types.Article.allowed_content_types)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

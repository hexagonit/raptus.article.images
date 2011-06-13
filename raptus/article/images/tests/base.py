# -*- coding: utf-8 -*-
"""Layers and TestCases for our tests."""

from __future__ import with_statement

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2

import unittest2 as unittest


class RaptusArticleImagesLayer(PloneSandboxLayer):
    """Layer for Raptus Article Images tests."""

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        """Prepare Zope."""
        import raptus.article.images
        self.loadZCML(package=raptus.article.images)
        z2.installProduct(app, 'raptus.article.core')
        z2.installProduct(app, 'raptus.article.images')

    def setUpPloneSite(self, portal):
        """Install into Plone site using portal_setup."""
        applyProfile(portal, 'raptus.article.images:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'raptus.article.core')
        z2.uninstallProduct(app, 'raptus.article.images')


# FIXTURES
RAPTUS_ARTICLE_IMAGES_FIXTURE = RaptusArticleImagesLayer()

# LAYERS
INTEGRATION_TESTING = IntegrationTesting(
    bases=(RAPTUS_ARTICLE_IMAGES_FIXTURE, ),
    name="raptus.article.images:Integration")

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RAPTUS_ARTICLE_IMAGES_FIXTURE,),
    name="raptus.article.images:Functional")


# TESTCASES
class RAImagesIntegrationTestCase(unittest.TestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit
    test cases.
    """
    layer = INTEGRATION_TESTING


class RAImagesFunctionalTestCase(unittest.TestCase):
    """We use this base class for all functional tests in this package -
    tests that require a full-blown Plone instance for testing.
    """
    layer = FUNCTIONAL_TESTING

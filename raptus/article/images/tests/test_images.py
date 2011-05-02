import unittest
import transaction
from StringIO import StringIO

from base import RACoreFunctionalTestCase
from base import RACoreIntegrationLayer
from base import R_A_CORE_FUNCTIONAL_FIXTURE
from plone.testing.z2 import Browser
from plone.testing import z2
from zope.configuration import xmlconfig
from plone.app.testing import PLONE_FIXTURE, FunctionalTesting
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import applyProfile

PNG_IMAGE = ('\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00'
             '\x01\x01\x00\x00\x00\x007n\xf9$\x00\x00\x00\nIDATx\x9cc`\x00\x00'
             '\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82')

class RAImagesIntegrationLayer(RACoreIntegrationLayer):
    """Layer for Raptus Article Images Integration tests."""

    defaultBases = (PLONE_FIXTURE, )
    def setUpZope(self, app, configurationContext):
        super(RAImagesIntegrationLayer, self).setUpZope(app, configurationContext)
        import raptus.article.images
        xmlconfig.file('configure.zcml',
                       raptus.article.images, context=configurationContext)
        z2.installProduct(app, 'raptus.article.images')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        super(RAImagesIntegrationLayer, self).setUpPloneSite(portal)
        applyProfile(portal, 'raptus.article.images:default')

R_A_IMAGES_INTEGRATION_FIXTURE = RAImagesIntegrationLayer()

R_A_IMAGES_FUNCTIONAL_TESTING = FunctionalTesting(
                            bases=(R_A_IMAGES_INTEGRATION_FIXTURE,
                                   R_A_CORE_FUNCTIONAL_FIXTURE),
                            name="RAImages:Functional")


class TestInstall(RACoreFunctionalTestCase):
    """Test addition of images to an article """
    layer = R_A_IMAGES_FUNCTIONAL_TESTING
    def test_raptus_images_add_image_in_browser(self):
        portal = self.layer['portal']
        browser = Browser(self.layer['app'])
        browser.addHeader('Authorization',
                  'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD))
        portal.invokeFactory('Article', 'some-article')
        article = portal['some-article']
        transaction.commit()
        browser.open(article.absolute_url())
        browser.getLink('Image').click()
        ctrl = browser.getControl(name='image_file')
        ctrl.add_file(StringIO(PNG_IMAGE), 'image/png', 'test_image.png')
        browser.getControl('Save').click()
        self.assertTrue('Changes saved' in browser.contents)
        self.assertTrue('test_image.png' in browser.url)
        self.assertEqual(article['test_image.png'].data, PNG_IMAGE)
        browser.open(article['test_image.png'].absolute_url())
        self.assertEqual(browser.contents, PNG_IMAGE)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)


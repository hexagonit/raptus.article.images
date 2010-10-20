from zope import interface, component

from Products.CMFCore.utils import getToolByName

try: # Plone 4 and higher
    from Products.ATContentTypes.interfaces.image import IATImage
except: # BBB Plone 3
    from Products.ATContentTypes.interface.image import IATImage

from raptus.article.core.interfaces import IArticle
from raptus.article.images.interfaces import IImages, IImage

class Images(object):
    """ Provider for images contained in an article
    """
    interface.implements(IImages)
    component.adapts(IArticle)
    
    def __init__(self, context):
        self.context = context
        
    def getImages(self, **kwargs):
        """ Returns a list of images based on the criteria passed as kwargs (catalog brains)
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(portal_type='Image', path={'query': '/'.join(self.context.getPhysicalPath()),
                                                  'depth': 1}, sort_on='getObjPositionInParent', **kwargs)

class Image(object):
    """ Handler for image thumbing and captioning
    """
    interface.implements(IImage)
    component.adapts(IATImage)
    
    def __init__(self, context):
        self.context = context
        
    def getImageURL(self, size="original"):
        """
        Returns the url to the image in the specific size
        
        The sizes are taken from the raptus_article properties sheet
        and are formed by the following name schema:
        
            images_<size>_(height|width)
        """
        if not self.context.Schema()['image'].get(self.context):
            return None
        
        w, h = self.getSize(size)
        
        url = '%s/image' % self.context.absolute_url()
        if w or h:
            scales = component.getMultiAdapter((self.context, self.context.REQUEST), name='images')
            scale = scales.scale('image', width=(w or 100000), height=(h or 100000))
            if scale is not None:
                url = scale.url
        return url
        
    def getImage(self, size="original"):
        """ 
        Returns the html tag of the image in the specific size
        
        The sizes are taken from the raptus_article properties sheet
        and are formed by the following name schema:
        
            images_<size>_(height|width)
        """
        url = self.getImageURL(size)
        if not url:
            return None
        
        return '<img src="%s" alt="%s" />' % (url, self.getCaption())
        
    def getSize(self, size):
        """
        Returns the width and height registered for the specific size
        """
        props = getToolByName(self.context, 'portal_properties').raptus_article
        return props.getProperty('images_%s_width' % size, 0), props.getProperty('images_%s_height' % size, 0)
    
    def getCaption(self):
        """
        Returns the caption for the image
        """
        return self.context.Description() or self.context.Title()

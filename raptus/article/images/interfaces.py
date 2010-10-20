from zope import interface

class IImages(interface.Interface):
    """ Provider for images contained in an article
    """
    
    def getImages(**kwargs):
        """ Returns a list of images based on the criteria passed as kwargs (catalog brains)
        """

class IImage(interface.Interface):
    """ Handler for image thumbing and captioning
    """
        
    def getImageURL(size="original"):
        """
        Returns the url to the image in the specific size
        
        The sizes are taken from the raptus_article properties sheet
        and are formed by the following name schema:
        
            images_<size>_(height|width)
        """
    
    def getImage(size="orginal"):
        """ 
        Returns the html tag of the image in the specific size
        
        The sizes are taken from the raptus_article properties sheet
        and are formed by the following name schema:
        
            images_<size>_(height|width)
        """
        
    def getSize(size):
        """
        Returns the width and height registered for the specific size
        """
    
    def getCaption():
        """
        Returns the caption for the image
        """

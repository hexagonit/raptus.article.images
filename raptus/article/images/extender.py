from zope.interface import implements
from zope.component import adapts

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from plone.indexer.interfaces import IIndexer

from Products.Archetypes import atapi
from Products.ZCatalog.interfaces import IZCatalog

try: # Plone 4 and higher
    from Products.ATContentTypes.interfaces.image import IATImage
except: # BBB Plone 3
    from Products.ATContentTypes.interface.image import IATImage

from raptus.article.core.componentselection import ComponentSelectionWidget
from raptus.article.core import RaptusArticleMessageFactory as _

class LinesField(ExtensionField, atapi.LinesField):
    """ LinesField
    """

class ImageExtender(object):
    """ Adds the component selection field to the image content type
    """
    implements(ISchemaExtender)
    adapts(IATImage)

    fields = [
        LinesField('components',
            enforceVocabulary = True,
            vocabulary_factory = 'componentselectionvocabulary',
            storage = atapi.AnnotationStorage(),
            schemata = 'settings',
            widget = ComponentSelectionWidget(
                description = _(u'description_component_selection_image', default=u'Select the components in which this image should be displayed.'),
                label= _(u'label_component_selection', default=u'Component selection'),
            )
        ),
    ]

    def __init__(self, context):
         self.context = context
         
    def getFields(self):
        return self.fields

class Index(object):
    implements(IIndexer)
    adapts(IATImage, IZCatalog)
    def __init__(self, obj, catalog):
        self.obj = obj
    def __call__(self):
        return self.obj.Schema()['components'].get(self.obj)

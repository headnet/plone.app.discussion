import time
from zope import interface
from zope.component import getUtility

from interfaces import ICommentingTool, IComment
# The commenting tool, which is a local utility

from Products.CMFCore.utils import UniqueObject, getToolByName
from OFS.SimpleItem import SimpleItem

class CommentingTool(UniqueObject, SimpleItem):
        
    interface.implements(ICommentingTool)
    
    meta_type = 'plone.app.discussion tool'
    id = 'portal_discussion'
    
    def reindexObject(self, object):
        """Remove from catalog.
        """
        catalog = getToolByName(self, 'portal_catalog')
        return catalog.reindexObject(object)
        
    indexObject = reindexObject

    def unindexObject(self, object):
        """Remove from catalog.
        """
        catalog = getToolByName(self, 'portal_catalog')
        return catalog.unindexObject(object)
    
    def uniqueValuesFor(self, name):
        """ return unique values for FieldIndex name """
        catalog = getToolByName(self, 'portal_catalog')
        return catalog.uniqueValuesFor(name)

    def searchResults(self, REQUEST=None, **kw):
        """
            Calls ZCatalog.searchResults with extra arguments that
            limit the results to what the user is allowed to see.
        """
        catalog = getToolByName(self, 'portal_catalog')
        object_provides = [IComment.__identifier__]
        if 'object_provides' in kw:
            kw_provides = kw['object_provides']
            if isinstance(str, kw_provides):
                object_provides.append(kw_provides)
            else:
                object_provides.extend(kw_provides)
        if REQUEST is not None and 'object_provides' in REQUEST.form:
            rq_provides = REQUEST.form['object_provides']
            del REQUEST.form['object_provides']
            if isinstance(str, rq_provides):
                object_provides.append(rq_provides)
            else:
                object_provides.extend(rq_provides)
        kw['object_provides'] = object_provides
        return catalog.searchResults(REQUEST, **kw)

def object_added_handler(obj, event):
    tool = getUtility(ICommentingTool)
    tool.indexObject(obj)
    
def object_removed_handler(obj, event):
    tool = getUtility(ICommentingTool)
    tool.unindexObject(obj)
"""A model for one project."""
from google.appengine.ext import ndb


class Project(ndb.Model):
    """A model for one project."""
    title = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    updated_date = ndb.DateTimeProperty(required=True, auto_now=True)
    # TODO(samking): add these fields
    # owner_key =  ndb.KeyProperty(required=True, kind=user.User)
    # tag_keys = ndb.KeyProperty(repeated=True, kind=tag.Tag)
    # is_completed = ndb.BooleanProperty(required=True, default=False)
    # page_views = ndb.IntegerProperty(required=True, default=0)

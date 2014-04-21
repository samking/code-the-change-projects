"""A model for the relationship between a user and a project."""
from google.appengine.ext import ndb
from models import user, project


class Collaborator(ndb.Model):
    """A model for relationship between a user and a project."""
    user_key = ndb.KeyProperty(required=True, kind=user.User)
    project_key = ndb.KeyProperty(required=True, kind=project.Project)
    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    updated_date = ndb.DateTimeProperty(required=True, auto_now=True)

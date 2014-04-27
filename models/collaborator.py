"""A model for the relationship between a user and a project."""
from google.appengine.ext import ndb

from models import project
from models import user


class Collaborator(ndb.Model):
    """A model for relationship between a user and a project."""
    user_key = ndb.KeyProperty(required=True, kind=user.User)
    project_key = ndb.KeyProperty(required=True, kind=project.Project)
    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)


def get_collaboration(user_key, project_key):
    """Returns a collaboration if the user is collaborating on the project."""
    # TODO(samking): after refreshing the page, we get stale data.  Make the
    # collaborator an ancestor query (on the user) to get strong
    # consistency.
    query = Collaborator.query().filter(
        Collaborator.user_key == user_key,
        Collaborator.project_key == project_key)
    collaboration = query.fetch(limit=1)
    return  collaboration[0] if collaboration else None

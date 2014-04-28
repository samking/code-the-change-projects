"""A model for the relationship between a user and a project."""
from google.appengine.ext import ndb

from models import project
from models import user


class Collaborator(ndb.Model):
    """A model for relationship between a user and a project."""
    user_key = ndb.KeyProperty(required=True, kind=user.User)
    project_key = ndb.KeyProperty(required=True, kind=project.Project)
    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)


def get_collaborator(user_key, project_key):
    """Returns a collaboration if the user is collaborating on the project."""
    # TODO(samking): after refreshing the page, we get stale data.  Make the
    # collaborator an ancestor query (on the user) to get strong
    # consistency.
    query = Collaborator.query().filter(
        Collaborator.user_key == user_key,
        Collaborator.project_key == project_key)
    collaborator = query.fetch(limit=1)
    return  collaborator[0] if collaborator else None


def get_projects(user_key):
    """Returns a list of all projects that the user is contributing to."""
    query = Collaborator.query(Collaborator.user_key == user_key)
    query = query.order(-Collaborator.created_date)
    collaborators = query.fetch()
    futures = []
    for collaborator in collaborators:
        futures.append(collaborator.project_key.get_async())
    ndb.Future.wait_all(futures)
    return [future.get_result() for future in futures]

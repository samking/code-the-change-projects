"""A model for the relationship between a user and a project."""
from google.appengine.ext import ndb

from ctc.models import user as user_model


class Collaborator(ndb.Model):
    """A model for relationship between a user and a project."""
    user_key = ndb.KeyProperty(required=True, kind=user_model.User)
    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)

    def _pre_put_hook(self):
        """Raises an exception if a new collaborator does not have a parent."""
        assert self.key.parent(), "No parent project for this collaborator."


def get_collaborator(user_key, project_key):
    """Returns a collaboration if the user is collaborating on the project."""
    query = Collaborator.query(ancestor=project_key).filter(
        Collaborator.user_key == user_key)
    collaborator = query.fetch(limit=1)
    return collaborator[0] if collaborator else None


def get_projects(user_key):
    """Returns a list of all projects that the user is contributing to."""
    query = Collaborator.query(Collaborator.user_key == user_key)
    query = query.order(-Collaborator.created_date)
    collaborators = query.fetch()
    futures = [collaborator.key.parent().get_async()
               for collaborator in collaborators]
    ndb.Future.wait_all(futures)
    return [future.get_result() for future in futures]


def get_collaborator_count(project_key):
    """Counts the number of collaborators for a given project."""
    query = Collaborator.query(ancestor=project_key)
    return query.count()


def get_collaborator_emails(project_key):
    """Returns the emails of all collaborating users."""
    query = Collaborator.query(ancestor=project_key)
    query = query.order(Collaborator.created_date)
    collaborators = query.fetch()
    futures = [collaborator.user_key.get_async()
               for collaborator in collaborators]
    ndb.Future.wait_all(futures)
    return [future.get_result().email for future in futures]

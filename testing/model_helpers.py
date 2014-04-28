"""Helpers for testing models."""

from models import project
from models import user


def create_project(
        title='title', description='description', lead='lead',
        tech_objectives='tech_objectives', github='github', owner_key=None):
    """Returns a new datastore-backed project."""
    if owner_key is None:
        owner_key = user.User().put()
    new_project = project.Project(
        title=title, description=description, lead=lead,
        tech_objectives=tech_objectives, github=github, owner_key=owner_key)
    new_project.put()
    return new_project

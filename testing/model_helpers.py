"""Helpers for testing models."""

from models import project


def create_project(title='title', description='description'):
    """Returns a new datastore-backed project."""
    new_project = project.Project(title=title, description=description)
    new_project.put()
    return new_project

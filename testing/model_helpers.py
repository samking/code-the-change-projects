"""Helpers for testing models."""

from models import project


def create_project(
	title='title', description='description', lead='lead',
	tech_objectives='tech_objectives', github='github'):
    """Returns a new datastore-backed project."""
    new_project = project.Project(
    	title=title, description=description, lead=lead, tech_objectives=tech_objectives,
    	github=github)
    new_project.put()
    return new_project

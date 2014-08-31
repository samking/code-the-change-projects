"""Helpers for testing models."""

from ctc.models import project as project_model
from ctc.models import user as user_model


def create_project(
        name='name', overview='overview', organization_name='organization name',
        organization_contact='organization contact',
        organization_mission='organization mission', details='details',
        collaboration_link='collaboration_link', code_link='code link',
        owner_key=None):
    """Returns a new datastore-backed project."""
    if owner_key is None:
        # The current user is the project owner.
        owner_key = user_model.get_current_user_key()
        # If the user is not logged in, an arbitrary user is the owner.
        if owner_key is None:
            owner_key = user_model.User(
                email='arbitrary@codethechange.org').put()
    new_project = project_model.Project(
        name=name, overview=overview, organization_name=organization_name,
        organization_contact=organization_contact,
        organization_mission=organization_mission, details=details,
        collaboration_link=collaboration_link, code_link=code_link,
        owner_key=owner_key)
    new_project.put()
    return new_project

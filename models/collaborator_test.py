"""Tests for the collaborator model."""

import unittest

import models.collaborator
import models.user
from testing import model_helpers
from testing import testutil


# Tests don't need docstrings, so pylint: disable=C0111
class CollaboratorTests(testutil.CtcTestCase):

    def test_get_collaborator(self):
        user_key = models.user.User().put()
        project = model_helpers.create_project(owner_key=user_key)
        self.assertEqual(
            models.collaborator.get_collaborator(user_key, project.key), None)
        collaborator = models.collaborator.Collaborator(
            user_key=user_key, project_key=project.key)
        collaborator.put()
        self.assertEqual(
            models.collaborator.get_collaborator(user_key, project.key),
            collaborator)

    def test_get_projects(self):
        user_key = models.user.User().put()
        self.assertEqual(models.collaborator.get_projects(user_key), [])
        project = model_helpers.create_project(owner_key=user_key)
        models.collaborator.Collaborator(
            user_key=user_key, project_key=project.key).put()
        self.assertEqual(models.collaborator.get_projects(user_key), [project])


if __name__ == '__main__':
    unittest.main()

"""Tests for the collaborator model."""

import unittest

import models.collaborator
import models.user
from testing import model_helpers
from testing import testutil


# Tests don't need docstrings, so pylint: disable=C0111
class CollaboratorTests(testutil.CtcTestCase):

    def test_get_collaborator(self):
        user_key = models.user.User(email='user@codethechange.org').put()
        project = model_helpers.create_project(owner_key=user_key)
        self.assertEqual(
            models.collaborator.get_collaborator(user_key, project.key), None)
        collaborator = models.collaborator.Collaborator(
            user_key=user_key, parent=project.key)
        collaborator.put()
        self.assertEqual(
            models.collaborator.get_collaborator(user_key, project.key),
            collaborator)

    def test_get_projects(self):
        user_key = models.user.User(email='getter@codethechange.org').put()
        self.assertEqual(models.collaborator.get_projects(user_key), [])
        project = model_helpers.create_project(owner_key=user_key)
        models.collaborator.Collaborator(
            user_key=user_key, parent=project.key).put()
        self.assertEqual(models.collaborator.get_projects(user_key), [project])

    def test_get_emails(self):
        user_key = models.user.User(email='user@codethechange.org').put()
        project = model_helpers.create_project(owner_key=user_key)
        collaborator = models.collaborator.Collaborator(
            user_key=user_key, parent=project.key)
        collaborator.put()
        another_user_key = models.user.User(email='another@codethechange.org').put()
        collaborator = models.collaborator.Collaborator(
            user_key=another_user_key, parent=project.key)
        collaborator.put()
        self.assertEqual(
            models.collaborator.get_collaborator_emails(project.key),
            ['user@codethechange.org', 'another@codethechange.org'])



    def test_get_collaborator_count(self):
        user_key = models.user.User(email='user@codethechange.org').put()
        project = model_helpers.create_project(owner_key=user_key)
        collaborator = models.collaborator.Collaborator(
            user_key=user_key, parent=project.key)
        collaborator.put()
        another_user_key = models.user.User(email='another@codethechange.org').put()
        collaborator = models.collaborator.Collaborator(
            user_key=another_user_key, parent=project.key)
        collaborator.put()
        self.assertEqual(
            models.collaborator.get_collaborator_count(project.key),
            2)
        collaborator.key.delete()
        self.assertEqual(
            models.collaborator.get_collaborator_count(project.key),
            1)




if __name__ == '__main__':
    unittest.main()

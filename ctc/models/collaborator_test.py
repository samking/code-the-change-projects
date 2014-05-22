"""Tests for the collaborator model."""

import unittest

from ctc.models import collaborator as collaborator_model
from ctc.models import user as user_model
from ctc.testing import model_helpers
from ctc.testing import testutil


# Tests don't need docstrings, so pylint: disable=C0111
class CollaboratorTests(testutil.CtcTestCase):

    def setUp(self):
        super(CollaboratorTests, self).setUp()
        self.user_key = user_model.User(email='user@codethechange.org').put()
        self.another_user_key = user_model.User(
            email='another@codethechange.org').put()
        self.project = model_helpers.create_project(owner_key=self.user_key)
        self.collaborator = collaborator_model.Collaborator(
            user_key=self.user_key, parent=self.project.key)
        self.another_collaborator = collaborator_model.Collaborator(
            user_key=self.another_user_key, parent=self.project.key)

    def test_get_collaborator(self):
        self.assertEqual(collaborator_model.get_collaborator(
            self.user_key, self.project.key), None)
        self.collaborator.put()
        self.assertEqual(
            collaborator_model.get_collaborator(
                self.user_key, self.project.key),
            self.collaborator)

    def test_get_projects(self):
        self.assertEqual(collaborator_model.get_projects(self.user_key), [])
        self.collaborator.put()
        self.assertEqual(
            collaborator_model.get_projects(self.user_key), [self.project])

    def test_get_emails(self):
        self.collaborator.put()
        self.another_collaborator.put()
        self.assertEqual(
            collaborator_model.get_collaborator_emails(self.project.key),
            ['user@codethechange.org', 'another@codethechange.org'])

    def test_get_collaborator_count(self):
        self.collaborator.put()
        self.another_collaborator.put()
        self.assertEqual(
            collaborator_model.get_collaborator_count(self.project.key),
            2)
        self.another_collaborator.key.delete()
        self.assertEqual(
            collaborator_model.get_collaborator_count(self.project.key),
            1)

    def test_put_collaborator_requires_parent(self):
        bad_collaborator = collaborator_model.Collaborator(
            user_key=self.user_key)
        self.assertRaises(AssertionError, bad_collaborator.put)


if __name__ == '__main__':
    unittest.main()

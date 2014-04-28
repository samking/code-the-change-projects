"""Tests for the collaborator model."""

import unittest

from testing import model_helpers
from testing import testutil
from models import collaborator as collaborator_model
from models import user as user_model


# Tests don't need docstrings, so pylint: disable=C0111
class CollaboratorTests(testutil.CtcTestCase):

    def test_get_collaborator(self):
        user_key = user_model.User().put()
        project = model_helpers.create_project(owner_key=user_key)
        self.assertEqual(
            collaborator_model.get_collaborator(user_key, project.key), None)
        collaborator = collaborator_model.Collaborator(
            user_key=user_key, project_key=project.key)
        collaborator.put()
        self.assertEqual(
            collaborator_model.get_collaborator(user_key, project.key),
            collaborator)


if __name__ == '__main__':
    unittest.main()

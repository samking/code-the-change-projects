"""Tests for the project model."""

import unittest

import models.project
import models.user
from testing import model_helpers
from testing import testutil


# Tests don't need docstrings, so pylint: disable=C0111
class ProjectTests(testutil.CtcTestCase):

    def test_populate(self):
        fields = {'title': 'title', 'description': 'description',
                  'lead': 'lead', 'tech_objectives': 'tech_objectives',
                  'github': 'github'}
        project = models.project.Project()
        populated_project = project.populate(fields)
        self.assertEqual(project, populated_project)
        self.assertEqual(project.title, 'title')
        self.assertEqual(project.description, 'description')
        self.assertEqual(project.lead, 'lead')
        self.assertEqual(project.tech_objectives, 'tech_objectives')
        self.assertEqual(project.github, 'github')

    def test_get_by_owner(self):
        user_key = models.user.User(email='owner@codethechange.org').put()
        self.assertEqual(models.project.get_by_owner(user_key), [])
        project1 = model_helpers.create_project(owner_key=user_key)
        project2 = model_helpers.create_project(owner_key=user_key)
        other_user = models.user.User(
            email='nottheowner@codethechange.org').put()
        model_helpers.create_project(owner_key=other_user)
        # Ordered by most recent.  Doesn't include the other user's project.
        expected_projects = [project2, project1]
        actual_projects = models.project.get_by_owner(user_key)
        self.assertEqual(expected_projects, actual_projects)


if __name__ == '__main__':
    unittest.main()

"""Tests for the project model."""

import unittest

from ctc.models import project as project_model
from ctc.models import user as user_model
from ctc.testing import model_helpers
from ctc.testing import testutil


# Tests don't need docstrings, so pylint: disable=C0111
class ProjectTests(testutil.CtcTestCase):

    def test_populate(self):
        fields = {'title': 'title', 'description': 'description',
                  'lead': 'lead', 'tech_objectives': 'tech_objectives',
                  'github': 'github'}
        project = project_model.Project()
        populated_project = project.populate(fields)
        self.assertEqual(project, populated_project)
        self.assertEqual(project.title, 'title')
        self.assertEqual(project.description, 'description')
        self.assertEqual(project.lead, 'lead')
        self.assertEqual(project.tech_objectives, 'tech_objectives')
        self.assertEqual(project.github, 'github')

    def test_get_by_owner(self):
        user_key = user_model.User(email='owner@codethechange.org').put()
        self.assertEqual(project_model.get_by_owner(user_key), [])
        project1 = model_helpers.create_project(owner_key=user_key)
        project2 = model_helpers.create_project(owner_key=user_key)
        other_user = user_model.User(
            email='nottheowner@codethechange.org').put()
        model_helpers.create_project(owner_key=other_user)
        # Ordered by most recent.  Doesn't include the other user's project.
        expected_projects = [project2, project1]
        actual_projects = project_model.get_by_owner(user_key)
        self.assertEqual(expected_projects, actual_projects)


if __name__ == '__main__':
    unittest.main()

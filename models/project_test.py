"""Tests for the project model."""

import unittest

from testing import testutil
import models.project


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


if __name__ == '__main__':
    unittest.main()

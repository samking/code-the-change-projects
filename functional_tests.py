"""Tests that the basic actions on the site work.

See http://webapp-improved.appspot.com/guide/testing.html for the webapp2
handler testing guide or http://webtest.pythonpaste.org/en/latest/ for webtest.
"""

import unittest

import webtest

from google.appengine.ext import testbed

import server
from models import project
from testing import model_helpers

# Tests don't need docstrings, so pylint: disable=C0111

class FunctionalTests(unittest.TestCase):
    """Test cases for handlers."""

    def setUp(self):
        super(FunctionalTests, self).setUp()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # It's annoying to have to figure out the right stub while you're
        # writing tests, so initialize ALL the stubs!
        self.testbed.init_all_stubs()
        self.testapp = webtest.TestApp(server.APP)

    def tearDown(self):
        super(FunctionalTests, self).tearDown()
        self.testbed.deactivate()
    
    def test_get_new_project(self):
        response = self.testapp.get('/project/new')
        self.assertEqual(response.status_int, 200)
        # It should have the POST link.
        self.assertIn('post', response.body)
        # It should have a field for title and description.
        self.assertIn('Title', response.body)
        self.assertIn('Description', response.body)

    def test_post_new_project(self):
        # There should be no projects to start.
        self.assertEqual(project.Project.query().count(), 0)
        response = self.testapp.post('/project/new', {
            'title': 'test_title', 'description': 'test_description'})
        # There should be a new project created.
        self.assertEqual(project.Project.query().count(), 1)
        # It should redirect to the page displaying the project.
        self.assertEqual(response.status_int, 302)
        new_project = project.Project.query().fetch()[0]
        self.assertTrue(
            response.location.endswith('/%d' % new_project.key.id()))
        # The project should have the corect title and description.
        self.assertEqual(new_project.title, 'test_title')
        self.assertEqual(new_project.description, 'test_description')

    def test_list_projects(self):
        model_helpers.create_project('hello')
        model_helpers.create_project('world')
        response = self.testapp.get('/projects')
        self.assertEqual(response.status_int, 200)
        self.assertIn('hello', response.body)
        self.assertIn('world', response.body)

    def test_get_edit_project(self):
        project_to_edit = model_helpers.create_project('hello', 'world')
        project_id = project_to_edit.key.id()
        edit_page = self.testapp.get('/project/%d/edit' % project_id)
        self.assertEqual(edit_page.status_int, 200)
        self.assertIn('hello', edit_page.body)
        self.assertIn('world', edit_page.body)

    def test_post_edit_project(self):
        project_to_edit = model_helpers.create_project('hello', 'world')
        project_id = project_to_edit.key.id()
        response = self.testapp.post(
            '/project/%d/edit' % project_id, {'title': 'goodbye'})
        self.assertEqual(response.status_int, 302)
        self.assertTrue(response.location.endswith('/%d' % project_id))
        edited_project = project_to_edit.key.get()
        self.assertEqual(edited_project.title, 'goodbye')
        self.assertEqual(edited_project.description, '')

    def test_display_project(self):
        project_to_display = model_helpers.create_project('hello', 'world')
        project_id = project_to_display.key.id()
        project_page = self.testapp.get('/project/%d' % project_id)
        self.assertEqual(project_page.status_int, 200)
        self.assertIn('hello', project_page.body)
        self.assertIn('world', project_page.body)
        self.assertIn('/project/%d/edit' % project_id, project_page.body)

    def test_get_main_page(self):
        self.testbed.setup_env(
            USER_EMAIL = 'test@codethechange.org', 
            USER_ID = '123', 
            overwrite = True)
        main_page = self.testapp.get('/')
        self.assertEqual(main_page.status_int, 200)
        self.assertIn('Code the Change', main_page.body)

    def test_analytics(self):
        page = self.testapp.get('/projects')
        self.assertIn('google-analytics', page)


if __name__ == '__main__':
    unittest.main()

"""Tests that the basic actions on the site work.

See http://webapp-improved.appspot.com/guide/testing.html for the webapp2
handler testing guide or http://webtest.pythonpaste.org/en/latest/ for webtest.
"""

import unittest

import models.project
import models.user
import server
from helpers import csrf
from testing import model_helpers
from testing import testutil

# Tests don't need docstrings, so pylint: disable=C0111
class FunctionalTests(testutil.CtcTestCase):
    """Test cases for handlers."""

    def setUp(self):
        super(FunctionalTests, self).setUp()
        self.testapp = testutil.TestApp(server.APP)

    def test_get_new_project(self):
        self.login()
        response = self.testapp.get('/project/new', status=200)
        # It should have the POST link.
        self.assertIn('post', response.body)
        # It should have a field for title and description.
        self.assertIn('Title', response.body)
        self.assertIn('Description', response.body)

    def test_post_new_project(self):
        self.login()
        csrf_token = csrf.make_token('/project/new')
        # There should be no projects to start.
        self.assertEqual(models.project.Project.query().count(), 0)
        response = self.testapp.post('/project/new', {
            'title': 'test_title', 'description': 'test_description',
            'csrf_token': csrf_token})
        # There should be a new project created.
        self.assertEqual(models.project.Project.query().count(), 1)
        # It should redirect to the page displaying the project.
        self.assertEqual(response.status_int, 302)
        new_project = models.project.Project.query().fetch()[0]
        self.assertTrue(
            response.location.endswith('/%d' % new_project.key.id()))
        # The project should have the corect title and description.
        self.assertEqual(new_project.title, 'test_title')
        self.assertEqual(new_project.description, 'test_description')

    def test_list_projects(self):
        model_helpers.create_project('hello')
        model_helpers.create_project('world')
        response = self.testapp.get('/projects', status=200)
        self.assertIn('hello', response.body)
        self.assertIn('world', response.body)

    def test_get_edit_project(self):
        self.login()
        project = model_helpers.create_project('hello', 'world')
        project_id = project.key.id()
        page = self.testapp.get('/project/%d/edit' % project_id, status=200)
        self.assertIn('hello', page.body)
        self.assertIn('world', page.body)

    def test_post_edit_project(self):
        self.login()
        project = model_helpers.create_project('hello', 'world')
        project_id = project.key.id()
        csrf_token = csrf.make_token('/project/%d/edit' % project_id)
        response = self.testapp.post(
            '/project/%d/edit' % project_id,
            {'title': 'goodbye', 'csrf_token': csrf_token}, status=302)
        self.assertTrue(response.location.endswith('/%d' % project_id))
        edited_project = project.key.get()
        self.assertEqual(edited_project.title, 'goodbye')
        self.assertEqual(edited_project.description, '')

    def test_only_creator_can_edit_project(self):
        self.login()
        other_user = models.user.User()
        other_user.put()
        project = model_helpers.create_project(owner_key=other_user.key)
        project_id = project.key.id()
        self.testapp.post('/project/%d/edit' % project_id, status=403)

    def test_display_project(self):
        project = model_helpers.create_project('hello', 'world')
        project_id = project.key.id()
        project_page = self.testapp.get('/project/%d' % project_id, status=200)
        self.assertIn('hello', project_page.body)
        self.assertIn('world', project_page.body)

    def test_get_main_page(self):
        main_page = self.testapp.get('/', status=200)
        self.assertIn('Code the Change', main_page.body)

    def test_analytics(self):
        page = self.testapp.get('/')
        self.assertIn('google-analytics', page)

    def test_login_required(self):
        project = model_helpers.create_project()
        display_project = '/project/%d' % project.key.id()
        login_required_get_urls = [
            '/dashboard', '/project/new', display_project + '/edit']
        login_required_post_urls = [
            '/project/new', display_project + '/edit',
            display_project + '/join', display_project + '/leave']
        login_not_required_urls = ['/', '/projects', display_project]
        for url in login_not_required_urls:
            self.testapp.get(url, status=200)
        for url in login_required_get_urls:
            page = self.testapp.get(url, status=302)
            self.assertIn('Login', page.location)
        for url in login_required_post_urls:
            # If login is required and the user isn't logged in, they will fail
            # the CSRF check.
            csrf_token = csrf.make_token(url)
            self.testapp.post(url, {'csrf_token': csrf_token}, status=403)

    # TODO(samking): add end to end tests (eg, go to the GET page and then send
    # the POST to use the actual hidden field).
    def test_forms_have_csrf_tokens(self):
        self.login()
        project = model_helpers.create_project()
        display_project = '/project/%d' % project.key.id()
        # These URLs have forms that should have CSRF tokens in them.
        form_urls = ['/project/new', display_project, display_project + '/edit']
        for url in form_urls:
            page = self.testapp.get(url, status=200)
            self.assertIn('csrf_token', page.body)


if __name__ == '__main__':
    unittest.main()

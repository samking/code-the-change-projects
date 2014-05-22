"""Tests that the basic actions on the site work.

See http://webapp-improved.appspot.com/guide/testing.html for the webapp2
handler testing guide or http://webtest.pythonpaste.org/en/latest/ for webtest.
"""

import unittest

import webtest

import models.project
import models.user
import server
from testing import model_helpers
from testing import testutil


# Tests don't need docstrings, so pylint: disable=C0111
class FunctionalTests(testutil.CtcTestCase):
    """Test cases for handlers."""

    def setUp(self):
        super(FunctionalTests, self).setUp()
        self.testapp = webtest.TestApp(server.APP)

    def login(self):
        """Creates a user, logs in, and returns the user."""
        user = models.user.User(id='12345',
                                email='test@codethechange.org')
        user.put()
        self.testbed.setup_env(
            USER_EMAIL='test@codethechange.org',
            USER_ID=user.key.id(),
            overwrite=True)
        return user

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
        # There should be no projects to start.
        self.assertEqual(models.project.Project.query().count(), 0)
        response = self.testapp.post('/project/new', {
            'title': 'test_title', 'description': 'test_description'})
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
        response = self.testapp.post(
            '/project/%d/edit' % project_id, {'title': 'goodbye'}, status=302)
        self.assertTrue(response.location.endswith('/%d' % project_id))
        edited_project = project.key.get()
        self.assertEqual(edited_project.title, 'goodbye')
        self.assertEqual(edited_project.description, '')

    def test_only_creator_can_edit_project(self):
        self.login()
        other_user = models.user.User(email='anotheruser@codethechange.org')
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

    def test_project_page_includes_counts(self):
        user_key = self.login().key
        project = model_helpers.create_project('hello', 'world')
        project_id = project.key.id()
        # Check to see that the count is present and 0.
        project_page = self.testapp.get('/project/%d' % project_id, status=200)
        self.assertRegexpMatches(
            project_page.body,
            'id="numbers".*\n.*<h1>0</h1>.*\n.*People Involved')
        # Add a collaborator and check to see the count increments.
        collab = models.collaborator.Collaborator(
            user_key=user_key, parent=project.key)
        collab.put()
        project_page = self.testapp.get('/project/%d' % project_id, status=200)
        self.assertRegexpMatches(
            project_page.body,
            'id="numbers".*\n.*<h1>1</h1>.*\n.*People Involved')

    def test_only_show_emails_of_collaborators_to_other_collaborators(self):
        project = model_helpers.create_project('hello', 'world')
        project_id = project.key.id()
        project_page = self.testapp.get('/project/%d' % project_id, status=200)
        self.assertNotIn('email', project_page.body)
        self.assertNotIn('@', project_page.body)
        self.assertIn('Login to', project_page.body)
        # Now, make the user a collaborator and verify the emails are present.
        user_key = self.login().key
        collab = models.collaborator.Collaborator(
            user_key=user_key, parent=project.key)
        collab.put()
        project_page = self.testapp.get('/project/%d' % project_id, status=200)
        self.assertIn('email', project_page.body)
        self.assertIn('@', project_page.body)

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
            page = self.testapp.get(url, status=200)
        for url in login_required_get_urls:
            page = self.testapp.get(url, status=302)
            self.assertIn('Login', page.location)
        for url in login_required_post_urls:
            page = self.testapp.post(url, status=302)
            self.assertIn('Login', page.location)


    def test_join_and_leave_project(self):
        self.login()
        self.testapp.post('/project/new', {
            'title': 'test_title', 'description': 'test_description'})
        new_project = models.project.Project.query().fetch()[0]
        project_id = new_project.key.id()
        response = self.testapp.post('/project/' + str(project_id) + '/join', status=302)
        page = self.testapp.get('/project/' + str(project_id))
        self.assertRegexpMatches(
            page.body,
            'id="numbers".*\n.*<h1>1</h1>.*\n.*People Involved')
        response = self.testapp.post('/project/'+ str(project_id) + '/leave', status=302)
        page = self.testapp.get('/project/' + str(project_id))
        self.assertRegexpMatches(
            page.body,
            'id="numbers".*\n.*<h1>0</h1>.*\n.*People Involved')

    def test_display_user(self):
        self.login()
        profile = models.user.User(
            id='123',
            email='testprofile@codethechange.org',
            biography='i am awesome',
            website='github!'
        )
        profile.put()
        profile_id = profile.key.id()
        page = self.testapp.get('/user/%d' % int(profile_id), status=200)
        self.assertIn('i am awesome', page.body)
        self.assertIn('github!', page.body)
        self.assertNotIn('Secondary Contact', page.body)
        self.assertNotIn('Edit', page.body)

    def test_edit_user(self):
        user_profile = self.login()
        profile_id = user_profile.key.id()
        page = self.testapp.get('/user/%d' % int(profile_id), status=200)
        self.assertIn('test@codethechange.org', page.body)
        self.assertIn('Edit', page.body)

    def test_post_edit_user(self):
        user_profile = self.login()
        user_id = user_profile.key.id()
        response = self.testapp.post(
            '/user/%d/edit' % int(user_id),
            {'biography': 'i can edit'}
            , status=302
        )
        self.assertTrue(response.location.endswith('/%d' % int(user_id)))
        edited_profile = user_profile.key.get()
        self.assertEqual(edited_profile.email, 'test@codethechange.org')
        self.assertEqual(edited_profile.biography, 'i can edit')

    def test_only_owner_can_edit_profile(self):
        self.login()
        other_profile = models.user.User(
            id='222222',
            email='testprofile@codethechange.org',
            biography='i am awesome',
            website='github!'
        ).put()
        other_id = other_profile.id()
        self.testapp.post('/user/%d/edit' % int(other_id), status=403)

if __name__ == '__main__':
    unittest.main()

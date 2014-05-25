"""Tests that the basic actions on the site work.

See http://webapp-improved.appspot.com/guide/testing.html for the webapp2
handler testing guide or http://webtest.pythonpaste.org/en/latest/ for webtest.
"""

import unittest

from ctc import server
from ctc.helpers import csrf
from ctc.models import collaborator as collaborator_model
from ctc.models import project as project_model
from ctc.models import user as user_model
from ctc.testing import model_helpers
from ctc.testing import testutil


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
        self.assertEqual(project_model.Project.query().count(), 0)
        response = self.testapp.post('/project/new', {
            'title': 'test_title', 'description': 'test_description',
            'csrf_token': csrf_token})
        # There should be a new project created.
        self.assertEqual(project_model.Project.query().count(), 1)
        # It should redirect to the page displaying the project.
        self.assertEqual(response.status_int, 302)
        new_project = project_model.Project.query().fetch()[0]
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

    def test_edit_project_requires_owner(self):
        # Create the project before logging in so that the project owner is
        # different from the currently-logged-in user.
        project = model_helpers.create_project()
        self.login()
        path = '/project/%d/edit' % project.key.id()
        self.testapp.get(path, status=403)
        csrf_token = csrf.make_token(path)
        self.testapp.post(path, {'csrf_token': csrf_token}, status=403)

    def test_only_creator_can_edit_project(self):
        self.login()
        other_user = user_model.User(email='anotheruser@codethechange.org')
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
        collab = collaborator_model.Collaborator(
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
        collab = collaborator_model.Collaborator(
            user_key=user_key, parent=project.key)
        collab.put()
        project_page = self.testapp.get('/project/%d' % project_id, status=200)
        self.assertIn('email', project_page.body)
        self.assertIn('@', project_page.body)

    def test_get_main_page(self):
        main_page = self.testapp.get('/', status=200)
        self.assertIn('Code the Change', main_page.body)

    def test_get_dashboard(self):
        self.login()
        dashboard = self.testapp.get('/dashboard', status=200)
        self.assertIn('Projects I Own', dashboard.body)

    def test_analytics(self):
        page = self.testapp.get('/')
        self.assertIn('google-analytics', page)

    def test_login_required(self):
        project = model_helpers.create_project()
        user_key = user_model.User(email='test@codethechange.org').put()
        display_project = '/project/%d' % project.key.id()
        display_user = '/user/%s' % user_key.id()
        login_required_get_urls = [
            '/dashboard', '/project/new', display_project + '/edit',
            display_user, display_user + '/edit']
        login_required_post_urls = [
            '/project/new', display_project + '/edit',
            display_project + '/join', display_project + '/leave',
            display_user + '/edit']
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
        user = self.login()
        project = model_helpers.create_project()
        display_project = '/project/%d' % project.key.id()
        display_user = '/user/%s' % user.key.id()
        # These URLs have forms that should have CSRF tokens in them.
        form_urls = [
            '/project/new', display_project, display_project + '/edit',
            display_user + '/edit']
        for url in form_urls:
            page = self.testapp.get(url, status=200)
            self.assertIn('csrf_token', page.body)

    def test_join_and_leave_project(self):
        self.login()
        # Make a project.
        new_project_token = csrf.make_token('/project/new')
        self.testapp.post('/project/new', {
            'title': 'test_title', 'description': 'test_description',
            'csrf_token': new_project_token})
        new_project = project_model.Project.query().fetch()[0]
        project_id = new_project.key.id()
        # Join the project.
        join_path = '/project/%d/join' % project_id
        join_token = csrf.make_token(join_path)
        self.testapp.post(join_path, {'csrf_token': join_token}, status=302)
        page = self.testapp.get('/project/' + str(project_id))
        self.assertRegexpMatches(
            page.body, 'id="numbers".*\n.*<h1>1</h1>.*\n.*People Involved')
        # Leave the project.
        leave_path = '/project/%d/leave' % project_id
        leave_token = csrf.make_token(leave_path)
        self.testapp.post(leave_path, {'csrf_token': leave_token}, status=302)
        page = self.testapp.get('/project/' + str(project_id))
        self.assertRegexpMatches(
            page.body, 'id="numbers".*\n.*<h1>0</h1>.*\n.*People Involved')
        # Leaving the project when not a collaborator shouldn't cause any
        # problems.
        self.testapp.post(leave_path, {'csrf_token': leave_token}, status=302)
        page = self.testapp.get('/project/' + str(project_id))
        self.assertRegexpMatches(
            page.body, 'id="numbers".*\n.*<h1>0</h1>.*\n.*People Involved')

    def test_display_user(self):
        self.login()
        profile = user_model.User(
            id='123', email='testprofile@codethechange.org',
            biography='i am awesome', website='github!')
        profile.put()
        profile_id = profile.key.id()
        page = self.testapp.get('/user/%s' % profile_id, status=200)
        self.assertIn('i am awesome', page.body)
        self.assertIn('github!', page.body)
        self.assertNotIn('Secondary Contact', page.body)
        self.assertNotIn('Edit', page.body)

    def test_display_user_for_owner(self):
        user = self.login()
        user.biography = 'i own this'
        user.put()
        page = self.testapp.get('/user/%s' % user.key.id(), status=200)
        self.assertIn('i own this', page.body)
        self.assertIn('Edit Your Profile', page.body)

    def test_edit_user(self):
        user_profile = self.login()
        profile_id = user_profile.key.id()
        page = self.testapp.get('/user/%s/edit' % profile_id, status=200)
        self.assertIn('Secondary Contact', page.body)

    def test_post_edit_user(self):
        user_profile = self.login()
        user_id = user_profile.key.id()
        csrf_token = csrf.make_token('/user/%s/edit' % user_id)
        response = self.testapp.post(
            '/user/%s/edit' % user_id,
            {'biography': 'i can edit', 'csrf_token': csrf_token}, status=302)
        self.assertTrue(response.location.endswith('/%s' % user_id))
        edited_profile = user_profile.key.get()
        self.assertEqual(edited_profile.email, 'test@codethechange.org')
        self.assertEqual(edited_profile.biography, 'i can edit')

    def test_only_owner_can_edit_profile(self):
        self.login()
        other_profile_key = user_model.User(
            id='222222', email='testprofile@codethechange.org',
            biography='i am awesome', website='github!').put()
        other_id = other_profile_key.id()
        edit_path = '/user/%s/edit' % other_id
        csrf_token = csrf.make_token(edit_path)
        self.testapp.post(edit_path, {'csrf_token': csrf_token}, status=403)


if __name__ == '__main__':
    unittest.main()

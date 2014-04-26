"""All handlers for ctc projects."""
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

from helpers import templates
from models import project


class MainPage(webapp2.RequestHandler):
    """The handler for the root page."""

    def get(self):
        """Renders the main landing page in response to a GET request."""
        values = {
            'login_url': users.create_login_url('/dashboard'),
            'logout_url': users.create_logout_url('/')
        }
        self.response.write(templates.render('main.html', values))


class DisplayDashboard(webapp2.RequestHandler):
    """The handler for displaying a which projects the user is working on"""

    def get(self):
        """Renders the dashboard corresponding to the logged in user"""
        user = users.get_current_user()
        if user:
            values = {
              'logout_url' : users.create_logout_url('/'),
              'own': [
                {'title': 'awesome project', 'id': '1'},
                {'title': 'awesomer project', 'id': '2'},
              ],
              'contributing': [
                {'title': 'pandas need my help', 'id':'3'},
                {'title': 'fixing education', 'id':'4'},
              ],
            }
            self.response.write(templates.render('dashboard.html', values))
        else:
            self.redirect(users.create_login_url(self.request.uri))


class DisplayProject(webapp2.RequestHandler):
    """The handler for displaying a project."""

    def get(self, project_id):
        """Renders the project page in response to a GET request."""
        project_to_display = ndb.Key(project.Project, int(project_id)).get()
        edit_link = self.uri_for(EditProject, project_id=project_id)
        values = {'project': project_to_display, 'edit_link': edit_link}
        self.response.write(templates.render('display_project.html', values))


class EditProject(webapp2.RequestHandler):
    """The handler for editing a project."""

    def get(self, project_id):
        """Renders the edit project page in response to a GET request."""
        project_to_edit = ndb.Key(project.Project, int(project_id)).get()
        edit_link = self.uri_for(EditProject, project_id=project_id)
        values = {
            'project': project_to_edit, 'action_link': edit_link,
            'action': 'Edit Your'}
        self.response.write(templates.render('edit_project.html', values))

    def post(self, project_id):
        """Edits the provided project."""
        project_to_edit = ndb.Key(project.Project, int(project_id)).get()
        project_to_edit.populate(self.request).put()
        self.redirect_to(DisplayProject, project_id=project_id)


class ListProjects(webapp2.RequestHandler):
    """The handler for the projects list."""

    def get(self):
        """Renders the projects page in response to a GET request."""
        query = project.Project.query().order(project.Project.updated_date)
        projects = query.fetch()
        links = []
        for curr_project in projects:
            project_id = curr_project.key.id()
            links.append(self.uri_for(DisplayProject, project_id=project_id))
        values = {'projects_and_links': zip(projects, links)}
        self.response.write(templates.render('list_projects.html', values))


class NewProject(webapp2.RequestHandler):
    """The handler for a new project."""

    def get(self):
        """Renders the new project page in response to a GET request."""
        values = {
            'action': 'Create a New', 'action_link': self.uri_for(NewProject)}
        self.response.write(templates.render('edit_project.html', values))

    def post(self):
        """Accepts a request to create a new project."""
        new_project = project.Project().populate(self.request)
        new_project_key = new_project.put()
        self.redirect_to(DisplayProject, project_id=new_project_key.id())

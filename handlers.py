"""All handlers for ctc projects."""
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

from functools import wraps

from helpers import templates
from models import collaborator
from models import project
from models import user as user_model

def require_login(request_func):
    """Decorator: only handle the provided request if the user is logged in.
    Else, redirect to the login page.
  Args:
   request_func: function. A function that handles a request.
  Returns:
    A function that will execute request_func only if the user is logged in.
  """
    @wraps(request_func)
    def new_request_func(self):
        """Redirects logged out users to the login page."""
        if users.get_current_user():
            return request_func(self)
        else:
            self.redirect(users.create_login_url(self.request.uri))
    return new_request_func



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
            'action': 'Edit'}
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
            'action': 'Create New', 'action_link': self.uri_for(NewProject)}
        self.response.write(templates.render('new_project.html', values))

    @require_login
    def post(self):
        """Accepts a request to create a new project."""
        current_user_key = user_model.get_current_user_key()
        new_project = project.Project().populate(self, current_user_key)
        new_project_key = new_project.put()
        self.redirect_to(DisplayProject, project_id=new_project_key.id())


class JoinProject(webapp2.RequestHandler):
    """Handler for a request to join a project."""

    def get(self, project_id):
        """Renders a join page in response to a GET request."""
        project_to_edit = ndb.Key(project.Project, int(project_id)).get()
        edit_link = self.uri_for(JoinProject, project_id=project_id)
        values = {
            'project': project_to_edit, 'action_link': edit_link,
            'action': 'Join'}
        self.response.write(templates.render('join_project.html', values))

    @require_login
    def post(self, project_id):
        """Accepts a request to join a project."""
        current_user_key = user_model.get_current_user_key()
        collaborator.Collaborator(
            user_key=current_user_key,
            project_key=ndb.Key(project.Project, project_id)).put()
        self.redirect_to(DisplayProject, project_id=project_id)


class NotLoggedIn(webapp2.RequestHandler):
    """Handler for when user is not logged in"""

    def get(self):
        """error page for failure to log in"""
        self.response.write(templates.render('notloggedin.html'))



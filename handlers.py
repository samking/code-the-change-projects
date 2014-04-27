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
    def new_request_func(self, *args, **kwargs):
        """Redirects logged out users to the login page."""
        if users.get_current_user():
            return request_func(self, *args, **kwargs)
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

    @require_login
    def get(self):
        """Renders the dashboard corresponding to the logged in user"""
        user_key = user_model.get_current_user_key()

        query = project.Project.query(project.Project.owner_key == user_key)\
            .order(project.Project.updated_date)
        owned_projects = query.fetch()
        query = collaborator.Collaborator.query(
            collaborator.Collaborator.user_key == user_key)\
            .order(collaborator.Collaborator.created_date)
        collaborations = query.fetch()
        contributing_projects = []
        for collaboration in collaborations:
            contributing_projects.append(
                project.Project.query(
                    project.Project.key.id() == collaboration.project_key
                ).fetch()[0]
            )

        values = {
              'logout_url': users.create_logout_url('/'),
              'own': [{'title': owned_project.title,
                       'id': owned_project.key.id()}
                       for owned_project in owned_projects
              ],
              'contributing': [
                  {'title': contributing_project.title,
                   'id': contributing_project.key.id()}
                  for contributing_project in contributing_projects
              ]
        }
        self.response.write(templates.render('dashboard.html', values))


class DisplayProject(webapp2.RequestHandler):
    """The handler for displaying a project."""

    def get(self, project_id):
        """Renders the project page in response to a GET request."""
        project_to_display = ndb.Key(project.Project, int(project_id)).get()
        edit_link = self.uri_for(EditProject, project_id=project_id)

        user_key = user_model.get_current_user_key()
        if (user_key and len(collaborator.Collaborator.query(
            ndb.AND(collaborator.Collaborator.project_key ==
                        ndb.Key(project.Project, int(project_id)),
                    collaborator.Collaborator.user_key == user_key)
        ).fetch()) == 1):
            action = "Leave"
            action_link = self.uri_for(LeaveProject, project_id=project_id)
        else:
            action = "Join"
            action_link = self.uri_for(JoinProject, project_id=project_id)


        values = {'project': project_to_display,
                  'edit_link': edit_link,
                  'action_link': action_link,
                  'action': action
        }
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

    @require_login
    def post(self):
        """Accepts a request to create a new project."""
        current_user_key = user_model.get_current_user_key()
        new_project = project.Project().populate(self.request, current_user_key)
        new_project_key = new_project.put()
        self.redirect_to(DisplayProject, project_id=new_project_key.id())

class JoinProject(webapp2.RequestHandler):
    """Handler for a request to join a project."""

    @require_login
    def post(self, project_id):
        """Accepts a request to join a project."""
        current_user_key = user_model.get_current_user_key()
        collaborator.Collaborator(
            user_key=current_user_key,
            project_key=ndb.Key(project.Project, int(project_id))).put()
        self.redirect_to(DisplayProject, project_id=project_id)


class LeaveProject(webapp2.RequestHandler):
    """Handler for a request to leave a project."""

    @require_login
    def post(self, project_id):
        """Accepts a request to leave a project."""
        current_user_key = user_model.get_current_user_key()
        query = collaborator.Collaborator.query(
            ndb.AND(collaborator.Collaborator.user_key == current_user_key,
                    collaborator.Collaborator.project_key ==
                    ndb.Key(project.Project, int(project_id))))
        collaboration_to_delete = query.fetch()
        if len(collaboration_to_delete == 1):
            collaboration_to_delete[0].key.delete()
        self.redirect_to(DisplayProject, project_id=project_id)

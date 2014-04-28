"""All handlers for ctc projects."""
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

from helpers import templates
from models import collaborator as collaborator_model
from models import project
from models import user as user_model


class BaseHandler(webapp2.RequestHandler):
    """Superclass for all CtC handlers."""

    def require_login(self):
        """Redirect to the login page and abort if the user is not logged in."""
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri), abort=True)


class MainPage(BaseHandler):
    """The handler for the root page."""

    def get(self):
        """Renders the main landing page in response to a GET request."""
        values = {
            'login_url': users.create_login_url('/dashboard'),
            'logout_url': users.create_logout_url('/')
        }
        self.response.write(templates.render('main.html', values))


class DisplayDashboard(BaseHandler):
    """The handler for displaying a which projects the user is working on"""

    def get(self):
        """Renders the dashboard corresponding to the logged in user"""
        self.require_login()
        user_key = user_model.get_current_user_key()
        # Get the most recent projects that the current user owns.
        query = project.Project.query(project.Project.owner_key == user_key)
        query = query.order(-project.Project.updated_date)
        owned_projects = query.fetch()
        # Get the most recent projects that the current user is contributing to.
        query = collaborator_model.Collaborator.query(
            collaborator_model.Collaborator.user_key == user_key)
        query = query.order(-collaborator_model.Collaborator.created_date)
        collaborator = query.fetch()
        contributing_projects = []
        for collaborator in collaborator:
            contributing_projects.append(collaborator.project_key.get())
        values = {
            'logout_url': users.create_logout_url('/'),
            'own': owned_projects,
            'contributing': contributing_projects
        }
        self.response.write(templates.render('dashboard.html', values))


class DisplayProject(BaseHandler):
    """The handler for displaying a project."""

    def get(self, project_id):
        """Renders the project page in response to a GET request."""
        project_to_display = ndb.Key(project.Project, int(project_id)).get()
        edit_link = self.uri_for(EditProject, project_id=project_id)
        user_key = user_model.get_current_user_key()
        is_collaborating = collaborator_model.get_collaborator(
            user_key, project_to_display.key)
        if user_key and is_collaborating:
            action = 'Leave'
            action_link = self.uri_for(LeaveProject, project_id=project_id)
        else:
            # TODO(samking): This doesn't quite work for logged-out users.
            action = 'Join'
            action_link = self.uri_for(JoinProject, project_id=project_id)
        values = {'project': project_to_display,
                  'edit_link': edit_link,
                  'action_link': action_link,
                  'action': action
        }
        self.response.write(templates.render('display_project.html', values))


class EditProject(BaseHandler):
    """The handler for editing a project."""

    def require_project_owner(self, project_to_edit):
        """Aborts the current request if the user isn't the project's owner."""
        current_user_key = user_model.get_current_user_key()
        if current_user_key != project_to_edit.owner_key:
            self.abort(403)

    def get(self, project_id):
        """Renders the edit project page in response to a GET request."""
        self.require_login()
        project_to_edit = ndb.Key(project.Project, int(project_id)).get()
        self.require_project_owner(project_to_edit)
        edit_link = self.uri_for(EditProject, project_id=project_id)
        values = {
            'project': project_to_edit, 'action_link': edit_link,
            'action': 'Edit Your'}
        self.response.write(templates.render('edit_project.html', values))

    def post(self, project_id):
        """Edits the provided project."""
        self.require_login()
        project_to_edit = ndb.Key(project.Project, int(project_id)).get()
        self.require_project_owner(project_to_edit)
        project_to_edit.populate(self.request).put()
        self.redirect_to(DisplayProject, project_id=project_id)


class ListProjects(BaseHandler):
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


class NewProject(BaseHandler):
    """The handler for a new project."""

    def get(self):
        """Renders the new project page in response to a GET request."""
        self.require_login()
        values = {
            'action': 'Create a New', 'action_link': self.uri_for(NewProject)}
        self.response.write(templates.render('edit_project.html', values))

    def post(self):
        """Accepts a request to create a new project."""
        self.require_login()
        current_user_key = user_model.get_current_user_key()
        new_project = project.Project().populate(self.request)
        new_project.owner_key = current_user_key
        new_project_key = new_project.put()
        self.redirect_to(DisplayProject, project_id=new_project_key.id())


class JoinProject(BaseHandler):
    """Handler for a request to join a project."""

    def post(self, project_id):
        """Accepts a request to join a project."""
        self.require_login()
        current_user_key = user_model.get_current_user_key()
        # TODO(samking): ensure that there's at most one collaborator per user
        # and project.
        collaborator_model.Collaborator(
            user_key=current_user_key,
            project_key=ndb.Key(project.Project, int(project_id))).put()
        self.redirect_to(DisplayProject, project_id=project_id)


class LeaveProject(BaseHandler):
    """Handler for a request to leave a project."""

    def post(self, project_id):
        """Accepts a request to leave a project."""
        self.require_login()
        current_user_key = user_model.get_current_user_key()
        collaborator = collaborator_model.get_collaborator(
            current_user_key, ndb.Key(project.Project, int(project_id)))
        if collaborator:
            collaborator.key.delete()
        self.redirect_to(DisplayProject, project_id=project_id)

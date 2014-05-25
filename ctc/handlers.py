"""All handlers for CtC projects."""

from google.appengine.api import users
from google.appengine.ext import ndb

from ctc.helpers import csrf
from ctc.helpers import templates
from ctc.models import collaborator as collaborator_model
from ctc.models import project as project_model
from ctc.models import user as user_model


class BaseHandler(csrf.CsrfHandler):
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
            # TODO: initialize login and logout urls in base handler?
            'login_url': users.create_login_url('/dashboard'),
            'logout_url': generate_logout_url()
        }
        self.response.write(templates.render('main.html', values))


class DisplayDashboard(BaseHandler):
    """The handler for displaying a which projects the user is working on"""

    def get(self):
        """Renders the dashboard corresponding to the logged in user"""
        self.require_login()
        user_key = user_model.get_current_user_key()
        owned_projects = project_model.get_by_owner(user_key)
        contributing_projects = collaborator_model.get_projects(user_key)
        values = {
            'logout_url': generate_logout_url(),
            'own': owned_projects,
            'contributing': contributing_projects
        }
        self.response.write(templates.render('dashboard.html', values))


class DisplayUser(BaseHandler):
    """The handler for displaying a user page."""

    def get(self, user_id):
        """Renders the user page in response to a GET request."""
        self.require_login()
        requesting_user_id = user_model.get_current_user_key().id()
        profile_object = user_model.User.get_by_id(user_id)
        is_profile_owner = (user_id == requesting_user_id)
        edit_link = None
        if is_profile_owner:
            edit_link = self.uri_for(EditUser, user_id=user_id)
        values = {
            'profile': profile_object,
            'edit_link': edit_link,
            'logout_url': generate_logout_url()
        }
        self.response.write(templates.render('display_user.html', values))


class EditUser(BaseHandler):
    """The handler for editing a user profile."""

    def require_owner(self, user_id):
        """Aborts the current request if the user isn't the profile's owner."""
        current_user_id = user_model.get_current_user_key().id()
        if current_user_id != user_id:
            self.abort(403)

    def get(self, user_id):
        """Renders the edit user page in response to a GET request."""
        self.require_login()
        self.require_owner(user_id)
        profile_object = user_model.User.get_by_id(user_id)
        edit_link = self.uri_for(EditUser, user_id=user_id)
        values = {
            'profile': profile_object, 'action_link': edit_link,
            'action': 'Update', 'logout_url': generate_logout_url(),
            'csrf_token': self.csrf_token}
        self.response.write(templates.render('edit_user.html', values))

    def post(self, user_id):
        """Edits the provided project."""
        self.require_login()
        self.require_owner(user_id)
        profile_object = user_model.User.get_by_id(user_id)
        profile_object.populate(self.request).put()
        self.redirect_to(DisplayUser, user_id=user_id)


class DisplayProject(BaseHandler):
    """The handler for displaying a project."""

    def get(self, project_id):
        """Renders the project page in response to a GET request."""
        project = ndb.Key(project_model.Project, int(project_id)).get()
        user_key = user_model.get_current_user_key()
        edit_link = None
        collaborator_emails = []
        # Initialize some truthy objects for the following display logic.
        is_logged_in = user_key
        is_collaborating = collaborator_model.get_collaborator(
            user_key, project.key)
        is_project_owner = is_logged_in and project.owner_key == user_key
        should_show_collaborator_emails = is_collaborating or is_project_owner
        # Use the above as booleans to guide permissions.
        if is_project_owner:
            edit_link = self.uri_for(EditProject, project_id=project_id)
        if should_show_collaborator_emails:
            collaborator_emails = collaborator_model.get_collaborator_emails(
                    ndb.Key(project_model.Project, int(project_id))
            )
        if is_collaborating:
            action = 'Leave'
            action_link = self.uri_for(LeaveProject, project_id=project_id)
        if not is_collaborating and is_logged_in:
            action = 'Join'
            action_link = self.uri_for(JoinProject, project_id=project_id)
        if not is_logged_in:
            action = 'Login to Join'
            action_link = users.create_login_url(self.request.uri)
        values = {'project': project,
                  'num_contributors':
                      collaborator_model.get_collaborator_count(
                          ndb.Key(project_model.Project, int(project_id))),
                  'edit_link': edit_link,
                  'action_link': action_link,
                  'action': action,
                  'csrf_token': csrf.make_token(action_link),
                  'logout_url': generate_logout_url(),
                  'collaborator_emails': collaborator_emails,
                  'logged_out_user': user_key is None
        }
        self.response.write(templates.render('display_project.html', values))


class EditProject(BaseHandler):
    """The handler for editing a project."""

    def require_project_owner(self, project):
        """Aborts the current request if the user isn't the project's owner."""
        current_user_key = user_model.get_current_user_key()
        if current_user_key != project.owner_key:
            self.abort(403)

    def get(self, project_id):
        """Renders the edit project page in response to a GET request."""
        self.require_login()
        project = ndb.Key(project_model.Project, int(project_id)).get()
        self.require_project_owner(project)
        edit_link = self.uri_for(EditProject, project_id=project_id)
        values = {
            'project': project, 'action_link': edit_link,
            'action': 'Edit Your', 'csrf_token': self.csrf_token,
            'logout_url': generate_logout_url()}
        self.response.write(templates.render('edit_project.html', values))

    def post(self, project_id):
        """Edits the provided project."""
        self.require_login()
        project = ndb.Key(project_model.Project, int(project_id)).get()
        self.require_project_owner(project)
        project.populate(self.request).put()
        self.redirect_to(DisplayProject, project_id=project_id)


class ListProjects(BaseHandler):
    """The handler for the projects list."""

    def get(self):
        """Renders the projects page in response to a GET request."""
        query = project_model.Project.query()
        query = query.order(project_model.Project.updated_date)
        projects = query.fetch()
        links = []
        for curr_project in projects:
            project_id = curr_project.key.id()
            links.append(self.uri_for(DisplayProject, project_id=project_id))
        values = {'projects_and_links': zip(projects, links),
                  'logout_url': generate_logout_url()}
        self.response.write(templates.render('list_projects.html', values))


class NewProject(BaseHandler):
    """The handler for a new project."""

    def get(self):
        """Renders the new project page in response to a GET request."""
        self.require_login()
        values = {
            'action': 'Create a New', 'action_link': self.uri_for(NewProject),
            'csrf_token': self.csrf_token, 'logout_url': generate_logout_url()}
        self.response.write(templates.render('edit_project.html', values))

    def post(self):
        """Accepts a request to create a new project."""
        self.require_login()
        current_user_key = user_model.get_current_user_key()
        new_project = project_model.Project().populate(self.request)
        new_project.owner_key = current_user_key
        new_project_key = new_project.put()
        self.redirect_to(DisplayProject, project_id=new_project_key.id())


class JoinProject(BaseHandler):
    """Handler for a request to join a project."""

    def post(self, project_id):
        """Accepts a request to join a project."""
        self.require_login()
        current_user_key = user_model.get_current_user_key()
        collaborator_model.Collaborator.get_or_insert(
            current_user_key.id(),
            user_key=current_user_key,
            parent=ndb.Key(project_model.Project, int(project_id))
        )
        self.redirect_to(DisplayProject, project_id=project_id)


class LeaveProject(BaseHandler):
    """Handler for a request to leave a project."""

    def post(self, project_id):
        """Accepts a request to leave a project."""
        self.require_login()
        current_user_key = user_model.get_current_user_key()
        collaborator = collaborator_model.get_collaborator(
            current_user_key, ndb.Key(project_model.Project, int(project_id)))
        if collaborator:
            collaborator.key.delete()
        self.redirect_to(DisplayProject, project_id=project_id)


def generate_logout_url():
    """Returns logout url if user is logged in; otherwise returns None."""
    return users.create_logout_url('/') if users.get_current_user() else None

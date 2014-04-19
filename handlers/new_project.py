"""A page for creating a new project."""
import webapp2

from helpers import templates
from models import project

class NewProject(webapp2.RequestHandler):
    """The handler for a new project."""

    def get(self):
        """Renders the new project page in response to a GET request."""
        self.response.write(templates.render('new_project.html'))

    def post(self):
        """Accepts a request to create a new project."""



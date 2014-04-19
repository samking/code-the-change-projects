"""A page to list all projects."""
import webapp2

from helpers import templates


class ListProjects(webapp2.RequestHandler):
    """The handler for the projects list."""

    def get(self):
        """Renders the projects page in response to a GET request."""
        values = {}
        self.response.write(templates.render('list_projects.html', values))

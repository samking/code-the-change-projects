"""A page to list all projects."""
import webapp2

from google.appengine.api import users

from helpers import templates


class ListProjects(webapp2.RequestHandler):
    """The handler for the projects list."""

    def get(self):
        values = {}
        self.response.write(templates.render('list_projects.html', values))

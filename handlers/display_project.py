"""A page for displaying a project."""
import webapp2

from helpers import templates


class DisplayProject(webapp2.RequestHandler):
    """The handler for displaying a project."""

    def get(self, project_id):
        values = {'project_id': project_id}
        self.response.write(templates.render('display_project.html', values))

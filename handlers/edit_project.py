"""A page for editing a project."""
import webapp2

from helpers import templates


class EditProject(webapp2.RequestHandler):
    """The handler for editing a project."""

    def get(self, project_id):
        values = {'project_id': project_id}
        self.response.write(templates.render('edit_project.html', values))

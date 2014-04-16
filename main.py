"""A simple webapp2 server."""

import os

# TODO(samking): get lint working
import jinja2
import webapp2

from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def render_template(template_name, template_values):
    """Renders the template with the provided name and values.

    Args:
      template_name: a string with the filename of the Jinja2 template.
      template_values: a dict with the values to be used in the template.

    Returns:
      The rendered template as a string.
    """
    return JINJA_ENVIRONMENT.get_template(template_name).render(template_values)


class MainPage(webapp2.RequestHandler):
    """The handler for the root page."""

    def get(self):
        user = users.get_current_user()
        if user:
            values = {'email': user.email()}
            self.response.write(render_template('main.html', values))
        else:
            self.redirect(users.create_login_url(self.request.uri))


# TODO(samking): remove debug=True before a production release
application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

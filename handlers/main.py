"""A simple webapp2 server."""

import webapp2

from google.appengine.api import users

from helpers import templates


class MainPage(webapp2.RequestHandler):
    """The handler for the root page."""

    def get(self):
        user = users.get_current_user()
        if user:
            values = {'email': user.email()}
            self.response.write(templates.render('main.html', values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

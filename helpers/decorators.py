"""All custom decorators for ctc-projects are here."""

from google.appengine.api import users

from functools import wraps

def require_login(request_func):
    """Decorator: only handle the provided request if the user is logged in.
    Else, redirect to the login page.
  Args:
   request_func: function. A function that handles a request.
  Returns:
    A function that will execute request_func only if the user is logged in.
  """
    @wraps(request_func)
    def new_request_func(self):
        """Redirects logged out users to the login page."""
        if users.get_current_user():
            return request_func(self)
        else:
            self.redirect(users.create_login_url(self.request.uri))
    return new_request_func

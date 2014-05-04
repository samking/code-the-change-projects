"""Helpers for using CSRF tokens in webapp2 handlers.

The easiest way to use this module is to make your handlers subclass
CsrfHandler.  Then, all you need to do is put self.csrf_token into forms.

If you want to manually use it, then you should override dispatch() in a base
handler to do the following:
  If the request is a get request, create a CSRF token like:
      self.csrf_token = csrf.make_token()
  If the request is a post request, ensure that CSRF tokens is valid like:
      if not csrf.validate_token(self.request):
          self.abort(403)
The reason that you should override dispatch() is because using a decorator or a
function call in all post() requests is error prone.  Specifically, if you
forgot to annotate a request, you would fail insecurely.  This way, post()
requests won't succeed unless you have the proper CSRF token.

Note that the default handler makes CSRF tokens that are valid for the current
URL.  That means that you would need to POST to the same URL that the form lives
at.  If that isn't the case, you need to specify a path:
    csrf.make_token(path)

Also, this module doesn't differentiate different HTTP mutator methods (POST,
PUT, DELETE), so if you define multiple mutator methods at a given URL and want
separate validation for them, you would need to modify this module.
"""
# Inspired by https://github.com/cyberphobia/xsrfutil

from datetime import datetime
from datetime import timedelta
import os

from google.appengine.ext import ndb


SECRET_KEY_SIZE_BITS = 256
SECRET_KEY_SIZE_BYTES = SECRET_KEY_SIZE_BITS / 8
TOKEN_DURATION = timedelta(weeks=1)


class SecretKey(ndb.Model):
    """A secret key for use with CSRF tokens."""

    secret_key = ndb.BlobProperty(required=True)


def make_token():
  pass


def validate_token(request):
    token = request.get('csrf_token')
    token_time = token.split('-')[-1]
    if not token:
        return False
    user = users.get_current_user()
    if not user:
        return False
    current_time = datetime.utcnow()
    user_id = user.user_id()
    path = request.path
    

def _get_secret_key():
    """Returns the CSRF key, creating one in necessary."""
    ndb_key = ndb.Key(SecretKey, 'csrf')
    secret_key = ndb_key.get()
    if secret_key:
        return secret_key.secret_key
    # The secret key wasn't found, so create it.
    random_bytes = os.urandom(SECRET_KEY_SIZE_BYTES)
    secret_key = SecretKey(secret_key=random_bytes, key=ndb_key)
    secret_key.put()
    return random_bytes

"""Helpers for using CSRF tokens in webapp2 handlers.

The easiest way to use this module is to make your handlers subclass
CsrfHandler.  Then, all you need to do is put self.csrf_token into forms.

Note that the default handler makes CSRF tokens that are valid for the current
URL.  That means that you would need to POST to the same URL that the form lives
at.  If that isn't the case, you need to specify a path:
    csrf.make_token(path)

Also, this module doesn't differentiate different HTTP mutator methods (POST,
PUT, DELETE), so if you define multiple mutator methods at a given URL and want
separate validation for them, you would need to modify this module.

If you don't want to subclass the CsrfHandler, then you should override
dispatch() in a base handler to do the following:
  If the request is a get request, create a CSRF token like:
      self.csrf_token = csrf.make_token()
  If the request is a post request, ensure that CSRF tokens is valid like:
      if not csrf.taken_is_valid(request.get('csrf_token'):
          self.abort(403)
The reason that you should override dispatch() is because using a decorator or a
function call in all post() requests is error prone.  Specifically, if you
forgot to annotate a request, you would fail insecurely.  This way, post()
requests won't succeed unless you have the proper CSRF token.
"""
# Inspired by https://github.com/cyberphobia/xsrfutil

import hashlib
import hmac
import os
import time

import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb


SECRET_KEY_SIZE_BITS = 256
SECRET_KEY_SIZE_BYTES = SECRET_KEY_SIZE_BITS / 8
# One week in seconds.
TOKEN_DURATION_SECONDS = 60*60*24*7
CSRF_ERROR_MESSAGE = ('Your request looks suspicious, so we rejected it.  This '
    'would happen if you loaded the form a week before submitting it, but '
    "other legitimate requests shouldn't trigger this error.  Email "
    'admin@codethechange.org if you think something is wrong.')


class SecretKey(ndb.Model):
    """A secret key for use with CSRF tokens."""

    secret_key = ndb.BlobProperty(required=True)
    

class CsrfHandler(webapp2.RequestHandler):
    """A request handler that is CSRF-safe.

    Specifically, all GET requests will have self.csrf_token, which they can
    embed in any forms for the same URL, and all mutator requests (POST, PUT,
    DELETE) will validate their CSRF token.  An app that follows HTTP method
    conventions (GET, HEAD, OPTIONS, and TRACE don't have side effects) should
    be safe.

    If you use this, you will need to manually put the CSRF token into your
    forms.  Also, if you have any forms that POST to a different URL than the
    GET where the form lives, you will need to manually call
    csrf.make_token(path) to make the CSRF token.
    """

    def __init__(self, *args, **kwargs):
        super(CsrfHandler, self).__init__(*args, **kwargs)
        self.csrf_token = None

    def dispatch(self):
        """Make a CSRF token for GET requests and verify it for mutators."""
        method = self.request.method
        if method == 'GET':
            self.csrf_token = make_token()
        if method == 'POST' or method == 'PUT' or method == 'DELETE':
            if not token_is_valid(self.request.get('csrf_token')):
                self.abort(403, detail=CSRF_ERROR_MESSAGE)
        super(CsrfHandler, self).dispatch()


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


def _tokens_are_equal(token1, token2):
    """Returns (token1 == token2).  Always takes the same amount of time.

    This function is necessary to avoid timing attacks.  The == operator will
    return faster if two things are unequal earlier, and an attacker could use
    that to figure out which letter they guessed wrong.

    Args:
        token1: A string to compare.
        token2: A string to compare.

    Returns:
        True iff token1 == token2.
    """
    # Similar to the PyCrypto constant_time_comparison function (which isn't yet
    # available in PyCrypto).
    # https://github.com/dlitz/pycrypto/pull/52/files
    if len(token1) != len(token2):
        return False
    differences = 0
    for char1, char2 in zip(token1, token2):
        differences |= ord(char1) ^ ord(char2)
    return not differences


def make_token(path=None, token_time=None):
    """Creates a CSRF token for the current user and the provided path and time.

    Args:
        path: a string for the path where the CSRF token is valid.  Defaults to
            the current path.
        token_time: The number of seconds since the Unix epoch (time.time())
            when this token was created.  Defaults to the current time.

    Returns:
        A string CSRF token for use with validate_token.  It is hex encoded, and
        the token will include the token_time after a space.  Returns None if
        there is no user currently logged in.
    """
    if path is None:
        path = os.environ.get('PATH_INFO', '/')
    if token_time is None:
        token_time = time.time()
    token_time = int(token_time)
    current_user = users.get_current_user()
    if not current_user:
        return None
    current_user_id = current_user.user_id()
    digester = hmac.new(key=_get_secret_key(), digestmod=hashlib.sha256)
    digester.update('%s %s %d' % (current_user_id, path, token_time))
    digest = digester.hexdigest()
    token = '%s %d' % (digest, token_time)
    return token


def token_is_valid(token):
    """Validates that the provided CSRF token is correct.

    This checks that there is a token which includes a timestamp that hasn't
    expired, that the user is logged in, and that the token is correct (it
    hashes properly).

    Args:
        token: a CSRF token generated using make_token()

    Returns:
        True iff token is valid.
    """
    # There must be a token.
    if not token:
        return False
    # The token must include a time.
    if token.count(' ') != 1:
        return False
    token_time = int(token.split()[-1])
    # The token must not have expired.
    if token_time + TOKEN_DURATION_SECONDS < time.time():
        return False
    # The user must be logged in.
    if not users.get_current_user():
        return False
    correct_token = make_token(token_time=token_time)
    return _tokens_are_equal(token, correct_token)

"""Helpers for using CSRF tokens in webapp2 handlers."""
# Inspired by https://github.com/cyberphobia/xsrfutil

import os

from google.appengine.ext import ndb


SECRET_KEY_SIZE_BITS = 256
SECRET_KEY_SIZE_BYTES = SECRET_KEY_SIZE_BITS / 8


class SecretKey(ndb.Model):
    """A secret key for use with CSRF tokens."""

    secret_key = ndb.BlobProperty(required=True)


def get_csrf_key():
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


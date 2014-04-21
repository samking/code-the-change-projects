"""A model for one user."""
from google.appengine.ext import ndb
from google.appengine.api import users


class User(ndb.Model):
    """A model for one user."""
    user_id = ndb.StringProperty(required=True)
    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    updated_date = ndb.DateTimeProperty(required=True, auto_now=True)

def get_current_user_key():
    """gets the ndb Key for the current logged in user,
    creates user if necessary. Returns None if user not logged in"""
    user_object = None
    if users.get_current_user():
        user_id = users.get_current_user().user_id()
        user_object = User.get_by_id(user_id)
    if id and not user_object:
        user_object = User(user_id=user_id)
        user_object.put()
    else:
        return None

    return ndb.Key(User, user_object.user_id)

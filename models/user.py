"""A model for one user."""
from google.appengine.ext import ndb
from google.appengine.api import users


class User(ndb.Model):
    """A model for one user."""
    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)

def get_current_user_key():
    """Gets the ndb Key for the current logged in user,
    creates user if necessary. Returns None if user not logged in."""
    user_object = None
    user_id = None
    if users.get_current_user():
        user_id = users.get_current_user().user_id()
        user_object = User.get_by_id(user_id)
    if not user_id:
        return None
    if not user_object:
        user_object = User(id=user_id)
        user_object.put()

    return ndb.Key(User, user_object.key.id())

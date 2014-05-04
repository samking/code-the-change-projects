"""A model for one user."""
from google.appengine.ext import ndb
from google.appengine.api import users


class User(ndb.Model):
    """A model for one user."""
    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    email = ndb.StringProperty(required=True)

def get_current_user_key():
    """Gets the ndb.Key for the current user, creating it if necessary.

    Returns None if the user is not logged in.
    """
    local_user_object = None
    user_id = None
    appengine_user = users.get_current_user()
    if appengine_user:
        user_id = appengine_user.user_id()
        local_user_object = User.get_by_id(user_id)
    # The user is not logged in.
    if not user_id:
        return None
    # The user is logged in but isn't in the datastore.
    if not local_user_object:
        local_user_object = User(id=user_id, email=appengine_user.email())
        local_user_object.put()
    return local_user_object.key

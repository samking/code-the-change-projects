"""A model for one user."""
from google.appengine.ext import ndb
from google.appengine.api import users


class User(ndb.Model):
    """A model for one user."""
    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    email = ndb.StringProperty(required=True)
    name = ndb.StringProperty(default="")
    secondary_contact = ndb.StringProperty(default="")
    biography = ndb.StringProperty(default="")
    website = ndb.StringProperty(default="")

    def populate(self, request):
        """Populates the fields in a user's profile from a web request.

        Args:
            request: A WebOb.Request with string values for each settable
                User parameter.

        Returns:
            self for the sake of chaining.
        """
        settable_fields = [
            'name', 'secondary_contact', 'biography', 'website']
        for field in settable_fields:
            setattr(self, field, request.get(field))
        return self

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

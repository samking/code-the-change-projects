"""A model for one project."""

from google.appengine.ext import ndb
from ctc.models import user as user_model


SETTABLE_FIELDS = [
    'name', 'overview', 'organization_name', 'organization_contact',
    'organization_mission', 'details', 'collaboration_link', 'code_link']

class Project(ndb.Model):
    """A model for one project."""
    # TODO(samking): String and text properties means that they have to be
    # defined, but they can still be the empty string.  We probably want to
    # require that there is actual text.  We might want to use a pre-put-hook
    # for this.
    name = ndb.StringProperty(required=True)
    overview = ndb.TextProperty(required=True)

    # Details about the organization as a whole.
    organization_name = ndb.StringProperty(required=True)
    organization_contact = ndb.TextProperty(required=True)
    organization_mission = ndb.TextProperty(required=True)

    # Details about the specific project.
    details = ndb.TextProperty(required=True)
    collaboration_link = ndb.TextProperty(required=True)
    code_link = ndb.TextProperty()

    # Bookkeeping.
    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    updated_date = ndb.DateTimeProperty(required=True, auto_now=True)
    owner_key = ndb.KeyProperty(required=True, kind=user_model.User)
    # TODO(samking): add these fields
    # tag_keys = ndb.KeyProperty(repeated=True, kind=tag.Tag)
    # is_completed = ndb.BooleanProperty(required=True, default=False)
    # page_views = ndb.IntegerProperty(required=True, default=0)

    def populate(self, request):
        """Populates the fields in a project from a web request.

        Args:
            request: A WebOb.Request with string values for each settable
                Project parameter.

        Returns:
            self for the sake of chaining.
        """
        for field in SETTABLE_FIELDS:
            setattr(self, field, request.get(field))
        return self


def get_by_owner(owner_key):
    """Returns a list of all projects owned by the provided user."""
    query = Project.query(Project.owner_key == owner_key)
    query = query.order(-Project.updated_date)
    return query.fetch()

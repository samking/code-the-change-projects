"""A model for one project."""

from google.appengine.ext import ndb
from models import user

class Project(ndb.Model):
    """A model for one project."""
    # TODO(samking): String and text properties means that they have to be
    # defined, but they can still be the empty string.  We probably want to
    # require that there is actual text.  We might want to use a pre-put-hook
    # for this.
    title = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)

    lead = ndb.TextProperty(required=True)
    tech_objectives = ndb.TextProperty(required=True)
    github = ndb.TextProperty(required=True)

    num_commits = ndb.IntegerProperty(required=False, default=0)
    num_contributors = ndb.IntegerProperty(required=False, default=0)

    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    updated_date = ndb.DateTimeProperty(required=True, auto_now=True)
    owner_key = ndb.KeyProperty(required=True, kind=user.User)
    # TODO(samking): add these fields
    # tag_keys = ndb.KeyProperty(repeated=True, kind=tag.Tag)
    # is_completed = ndb.BooleanProperty(required=True, default=False)
    # page_views = ndb.IntegerProperty(required=True, default=0)

    def populate(self, request, submitting_user):
        """Populates the fields in a project from a web request.

        Args:
            request: A WebOb.Request with string values for each settable
                Project parameter.

        Returns:
            self for the sake of chaining.
        """
        settable_fields = [
            'title', 'description', 'lead', 'tech_objectives', 'github']
        for field in settable_fields:
            setattr(self, field, request.get(field))
        setattr(self, 'owner_key', submitting_user)
        return self

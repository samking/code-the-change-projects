"""The server which handles all routing logic."""
import os

import webapp2

import handlers


IS_DEV = os.environ['SERVER_SOFTWARE'].startswith('Development')


def named_route(path, handler):
    """Returns a webapp2 route with a name populated.

    Args:
        path: the string path to handle.
        handler: a class that will be used as the handler and as the name.

    Returns:
        The corresponding webapp2 handler.
    """
    return webapp2.Route(path, handler=handler, name=handler)


APP = webapp2.WSGIApplication([
    named_route(r'/', handlers.MainPage),
    named_route(r'/projects', handlers.ListProjects),
    named_route(r'/project/<project_id:\d+>', handlers.DisplayProject),
    named_route(r'/project/<project_id:\d+>/edit', handlers.EditProject),
    named_route(r'/project/<project_id:\d+>/join', handlers.JoinProject),
    named_route(r'/project/new', handlers.NewProject),
    named_route(r'/notloggedin', handlers.NotLoggedIn),
], debug=IS_DEV)

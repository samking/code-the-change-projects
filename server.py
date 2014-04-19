"""The server which handles all routing logic."""
import os

import webapp2

from handlers import display_project
from handlers import edit_project
from handlers import list_projects
from handlers import main
from handlers import new_project


IS_DEV = os.environ['SERVER_SOFTWARE'].startswith('Development')


APP = webapp2.WSGIApplication([
    ('/', main.MainPage),
    ('/projects', list_projects.ListProjects),
    ('/project/(\d+)', display_project.DisplayProject),
    ('/project/(\d+)/edit', edit_project.EditProject),
    ('/project/new', new_project.NewProject),
], debug=IS_DEV)

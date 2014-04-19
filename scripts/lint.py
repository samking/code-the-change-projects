#!/usr/bin/env python
"""Fixes environment variables and runs pylint on the project directory."""
import os
import subprocess


# Libraries, like Jinja or Webapp2, that App Engine provides automatically.
EXTRA_LIBRARIES = ['jinja2-2.6', 'webapp2-2.5.2']
# The path, relative to the Google Cloud SDK directory, where the app engine
# library lives.
APP_ENGINE_API_PATH = 'platform/google_appengine/'
# The path, relative to the Google Cloud SDK directory, where libraries live.
LIBRARY_PATH = APP_ENGINE_API_PATH + 'lib/'


def get_cloud_dir():
    """Returns the root of the Google Cloud SDK by getting it from the path."""
    # Use os.environ rather than sys.path because, for some reason, sys.path
    # doesn't always have the google cloud dir in it.
    path = os.environ['PATH'].split(':')
    google_cloud_dir = None
    for directory in path:
        if 'google-cloud-sdk' in directory:
            google_cloud_dir = directory
    assert google_cloud_dir, 'Error: No Google Cloud SDK found in path.'
    # The directory added to the path will be the /bin directory.  We want the
    # root, so we strip this.
    google_cloud_dir = os.path.dirname(google_cloud_dir)
    return google_cloud_dir
            

def fix_python_path():
    """Adds App Engine libraries to the PYTHONPATH.
    
    Returns: 
        A copy of os.environ with the modified PYTHONPATH.
    """
    google_cloud_dir = get_cloud_dir() + '/'
    google_cloud_library_base = google_cloud_dir + LIBRARY_PATH
    # Add the extra libraries to PYTHONPATH
    envs = os.environ.copy()
    envs['PYTHONPATH'] += ':' + google_cloud_dir + APP_ENGINE_API_PATH
    for library in EXTRA_LIBRARIES:
        envs['PYTHONPATH'] += ':' + google_cloud_library_base + library
    return envs


def get_project_dir():
    """Returns the directory of the project containing this script."""
    # The parent of this script's directory is the project's root.
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_files_to_lint():
    """Returns a list of all python files in the project's directory."""
    project_dir = get_project_dir()
    files_to_lint = []
    for root, _, filenames in os.walk(project_dir):
        for filename in filenames:
            # We use empty __init__ files for imports.  They don't need
            # docstrings.
            if filename.endswith('.py') and filename != '__init__.py':
                files_to_lint.append(root + '/' + filename)
    return files_to_lint


def get_pylint_command(files_to_lint):
    """Returns a list representing the pylint command.
    
    Args:
        files_to_lint: A list of files to run pylint on.
    """
    # We need to specify the rcfile because we want it to be a dotfile, but
    # pylint expects it to be called "pylintrc" without the dot.
    pylint_command = ['pylint', '--rcfile=%s/.pylintrc' % get_project_dir()]
    return pylint_command + files_to_lint


def run_lint():
    """Runs lint on all python files in the project, setting the path first."""
    envs = fix_python_path()
    files_to_lint = get_files_to_lint()
    pylint_command = get_pylint_command(files_to_lint)
    subprocess.call(pylint_command, env=envs)


if __name__ == '__main__':
    run_lint()

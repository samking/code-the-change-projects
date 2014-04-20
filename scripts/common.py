"""Common utilities for scripts."""

import os
import sys


# The path, relative to the Google Cloud SDK directory, where the app engine
# library lives.
APP_ENGINE_API_PATH = 'platform/google_appengine/'


def get_project_dir():
    """Returns the directory of the project containing this script."""
    # The parent of this script's directory is the project's root.
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_app_engine_dir():
    """Returns the root of the Google App Engine directory from the path."""
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
    return google_cloud_dir + '/' + APP_ENGINE_API_PATH


def fix_app_engine_path():
    """Adds App Engine paths to the system path."""
    # Add the project directory in case we want to run a script from outside of
    # the main project directory.
    sys.path.append(get_project_dir())
    # Add the main app engine directory so that we can import dev_appserver.
    sys.path.append(get_app_engine_dir())
    import dev_appserver
    dev_appserver.fix_sys_path()
    # Add the new sys.path to PYTHONPATH since child processes (like nose and
    # lint) don't inherit sys.path.
    new_paths = ':' + ':'.join(sys.path)
    os.environ['PYTHONPATH'] += new_paths

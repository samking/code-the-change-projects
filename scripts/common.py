"""Common utilities for scripts."""

import os


def get_project_dir():
    """Returns the directory of the project containing this script."""
    # The parent of this script's directory is the project's root.
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))



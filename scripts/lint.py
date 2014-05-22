#!/usr/bin/env python
"""Fixes environment variables and runs pylint on the project directory.

Note that this uses pylint, so you must have pylint installed.  You will get
an OSError if you don't have it installed.
"""
import os
import subprocess

# To support running this file from the root, pylint: disable=F0401
import common
# pylint: enable=F0401


def get_files_to_lint():
    """Returns a list of all python files in the project's directory."""
    project_dir = common.get_project_dir()
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
    pylint_command = [
        'pylint', '--rcfile=%s/.pylintrc' % common.get_project_dir()]
    return pylint_command + files_to_lint


def run_lint():
    """Runs lint on all python files in the project, setting the path first."""
    common.fix_app_engine_path()
    files_to_lint = get_files_to_lint()
    # TODO(samking): run a different lint on test files versus normal files
    # since test files have different rules (eg, docstrings and private
    # methods).
    pylint_command = get_pylint_command(files_to_lint)
    subprocess.call(pylint_command)


if __name__ == '__main__':
    run_lint()

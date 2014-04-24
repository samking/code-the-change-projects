#!/usr/bin/env python
"""Runs all unit tests."""

import subprocess

# To support running this file from the root, pylint: disable=F0401
import common
# pylint: enable=F0401


def run_tests():
    """Runs unit tests using nose and the NoseGAE plugin."""
    app_engine_dir = common.get_app_engine_dir()
    project_dir = common.get_project_dir()
    subprocess.call(
        ['nosetests', '--with-gae', '--without-sandbox', '--gae-lib-root',
         app_engine_dir, project_dir])


if __name__ == '__main__':
    run_tests()

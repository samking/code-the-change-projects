#!/usr/bin/env python
"""Runs all unit tests."""

import os
import subprocess

# To support running this file from the root, pylint: disable=F0401
import common
# pylint: enable=F0401


def run_tests(with_coverage=False):
    """Runs unit tests using nose and the NoseGAE plugin."""
    app_engine_dir = common.get_app_engine_dir()
    project_dir = common.get_project_dir()
    # NoseGAE wants us to be in the project directory.
    os.chdir(project_dir)
    # TODO(samking): Use https://github.com/jkrebs/nose-gae-index to
    # automatically update indexes when unit tests are run.
    command = [
        'nosetests', '--with-gae', '--without-sandbox', 
        '--gae-lib-root=' + app_engine_dir, '--nologcapture', project_dir]
    if with_coverage:
        # Documentation for these flags is at
        # http://nose.readthedocs.org/en/latest/plugins/cover.html
        command += [
            '--with-coverage', '--cover-package=ctc', '--cover-inclusive',
            '--cover-erase', '--cover-branches']
    subprocess.call(command)


if __name__ == '__main__':
    run_tests()

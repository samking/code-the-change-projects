#!/usr/bin/env python
"""Removes miscellaneous non-code files from the project directory."""

import os

import common


def clean():
    """Removes all .pyc files from the project directory."""
    project_dir = common.get_project_dir()
    for root, _, filenames in os.walk(project_dir):
        for filename in filenames:
            if filename.endswith('.pyc'):
                os.remove(root + '/' + filename)


if __name__ == '__main__':
    clean()

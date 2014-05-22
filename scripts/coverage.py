#!/usr/bin/env python
"""Runs all unit tests with coverage analysis."""

import test


if __name__ == '__main__':
    test.run_tests(with_coverage=True)

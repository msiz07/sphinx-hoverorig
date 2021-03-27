"""
    pytest config for sphinx/tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import os
import shutil

import docutils
import pytest

import sphinx
#from sphinx.testing import comparer
from sphinx.testing.path import path


pytest_plugins = 'sphinx.testing.fixtures'


# copied from "sphinx.testing.fixtures" module to suppress warning
# messages during pytest execution in my environment
def pytest_configure(config):
    DEFAULT_ENABLED_MARKERS = [
        (
            'sphinx(builder, testroot=None, freshenv=False,'
            ' confoverrides=None, tags=None, docutilsconf=None, parallel=0): '
            ' arguments to initialize the sphinx test application.'
        ),
        'test_params(shared_result=...): test parameters.',
    ]
    # register custom markers
    for marker in DEFAULT_ENABLED_MARKERS:
        config.addinivalue_line('markers', marker)


# Exclude 'roots' dirs for pytest test collector
collect_ignore = ['roots']


@pytest.fixture(scope='session')
def rootdir():
    return path(__file__).parent.abspath() / 'roots'


def pytest_report_header(config):
    header = ("libraries: Sphinx-%s, docutils-%s" %
              (sphinx.__display_version__, docutils.__version__))
    if hasattr(config, '_tmp_path_factory'):
        header += "\nbase tempdir: %s" % config._tmp_path_factory.getbasetemp()

    return header


#def pytest_assertrepr_compare(op, left, right):
#    comparer.pytest_assertrepr_compare(op, left, right)


def _initialize_test_directory(session):
    if 'SPHINX_TEST_TEMPDIR' in os.environ:
        tempdir = os.path.abspath(os.getenv('SPHINX_TEST_TEMPDIR'))
        print('Temporary files will be placed in %s.' % tempdir)

        if os.path.exists(tempdir):
            shutil.rmtree(tempdir)

        os.makedirs(tempdir)


def pytest_sessionstart(session):
    _initialize_test_directory(session)

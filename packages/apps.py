# -*- coding: utf-8 -*-
#
# Copyright © 2015  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# Any Red Hat trademarks that are incorporated in the source
# code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission
# of Red Hat, Inc.
#

'''
Top level of the fedora-packages Flask application.
'''

import logging
import logging.handlers
import os
import sys
import urlparse

import flask
import munch


__version__ = '0.1'
__api_version__ = '0.1'

APP = flask.Flask(__name__)

APP.config.from_object('packages.default_config')
if 'PKGS_CONFIG' in os.environ:  # pragma: no cover
    APP.config.from_envvar('PKGS_CONFIG')


# Log to stderr as well
STDERR_LOG = logging.StreamHandler(sys.stderr)
STDERR_LOG.setLevel(logging.INFO)
APP.logger.addHandler(STDERR_LOG)

LOG = APP.logger

@APP.route('/')
def index():
    ''' Display the index package DB page. '''
    subpkgs = []
    for subpkg in \
            [
                {'name': 'python-debug'},
                {'name': 'python-devel'},
                {'name': 'python-libs'},
                {'name': 'python-macro'},
                {'name': 'python-test'},
                {'name': 'python-tools'},
                {'name': 'tkinter'},
            ]:
        subpkgs.append(munch.Munch(subpkg))

    package = munch.Munch(
        {
            'name': 'python',
            'summary': 'An interpreted, interactive, object-oriented programming language',
            'latest_build': '2.7.10-10.fc24',
            'poc': 'mstuchli',
            'sub_pkgs': subpkgs,
            'description':'Python is an interpreted, interactive, object-oriented programming language often compared to Tcl, Perl, Scheme or Java. Python includes modules, classes, exceptions, very high level dynamic data types and dynamic typing. Python supports interfaces to many system calls and libraries, as well as to various windowing systems (X11, Motif, Tk, Mac and MFC). Programmers can write new built-in modules for Python in C or C++. Python can be used as an extension language for applications that need a programmable interface. Note that documentation for Python is provided in the python-docs package. This package provides the "python" executable; most of the actual implementation is within the "python-libs" package.',
            'homepage': 'http://www.python.org',
        }
    )

    return flask.render_template('package.html', package=package)


## pylint: disable=W0613
#@APP.teardown_request
#def shutdown_session(exception=None):
    #""" Remove the DB session at the end of each request. """
    #SESSION.remove()


# pylint: disable=W0613
@APP.before_request
def set_session():
    """ Set the flask session as permanent. """
    flask.session.permanent = True

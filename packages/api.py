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
API for the fedora-packages Flask application.
'''

import flask
import requests

from packages.apps import APP


def check_callback(response):
    """ Check the callback argument provided with the request to allow
    JQuery ajax calls.
    """
    callback = flask.request.args.get('callback', None)
    if callback:
        response = flask.Response(
            response="%s(%s);" % (callback, response.response),
            status=response.status_code,
            mimetype='application/javascript',
        )
    return response


@APP.route('/api/history/<package>')
def api_history(package):
    ''' Return the recent history of a package. '''
    url = APP.config.get(
        'datagrepper_url',
        'https://apps.fedoraproject.org/datagrepper/raw/')
    headers = dict(accept='text/html')
    params = [
        ('order', 'desc'),
        ('rows_per_page', 5),
        ('package', package),
        ('chrome', 'false'),
        ('not_topic', 'org.fedoraproject.prod.buildsys.tag'),
        ('not_topic', 'org.fedoraproject.prod.buildsys.untag'),
    ]
    try:
        response = requests.get(url, headers=headers, params=params)
        output = {'text': response.text}
    except:
        output = {'text': '<p>Could not connect to datagrepper</p>'}

    return flask.jsonify(output)

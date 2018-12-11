# Copyright (C) 2008 Abiquo Holdings S.L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import requests
import sys

from authorize import Credentials
from authorize import get_access_token
from requests_oauthlib import OAuth1Session
from os.path import isfile

def register_app(api_url, credentials, app_name):
    """ Registers a new Application in the Abiquo API. """ 
    user_info = requests.get("%s/login" % api_url, verify=False,
            headers={'Accept': 'application/vnd.abiquo.user+json',
                     'Authorization': credentials.auth})
    app_link = filter(lambda l: l['rel'] == 'applications', user_info.json()['links'])[0]
    app = requests.post(app_link['href'], verify=False,
            headers={'Content-type': 'application/vnd.abiquo.application+json',
                     'Authorization': credentials.auth},
            data=json.dumps({'name': app_name})).json()
    return (app['apiKey'], app['apiSecret'])

if __name__ == '__main__':
    api_url = raw_input('Abiquo API endpoint: ')
    id_input = raw_input('Username or OpenID access_token (prefixed with "openid:") or file (prefixed with "file:"): ')
    identity = None
    credential = None
    if id_input.startswith('openid:'):
        identity = id_input.rstrip()
    elif id_input.startswith('file:'):
        fpath = id_input.split(":")[-1]
        try:
            f = open(fpath, 'r')
            identity = f.read().rstrip()
        except IOError as e:
            print "Error reading file '%s'" % fpath
            sys.exit(1)
    else:
        identity = id_input
        credential = raw_input('Password: ')
    app_name = raw_input('Application name: ')
    credentials = Credentials(identity, credential)
    appkey, appsecret = register_app(api_url, credentials, app_name)
    access_token, access_token_secret = get_access_token(api_url, credentials, appkey, appsecret)
    print "App key: %s\nApp secret: %s" % (appkey, appsecret)
    print "Access token: %s\nAccess token secret: %s" % (access_token, access_token_secret)

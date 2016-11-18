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

import base64
import json
import requests

from requests_oauthlib import OAuth1Session

class Credentials(object):
    def __init__(self, identity, credential=None):
        if identity.startswith('openid:'):
            user = identity[7:]
            self.auth = 'Bearer %s' % user
        else:
            self.auth = 'Basic %s' % base64.b64encode('%s:%s' % (identity, credential))


def get_access_token(api_url, credentials, app_key, app_secret):
    """ Generates a pair of authorized tokens for a given application. """
    oauth = OAuth1Session(app_key, client_secret=app_secret, callback_uri='oob')
    tokens = oauth.fetch_request_token("%s/oauth/request_token" % api_url, verify=False)
    r = requests.get("%s/oauth/authorize?oauth_token=%s" % (api_url, tokens['oauth_token']),
            headers={'Authorization': credentials.auth},
            allow_redirects=False,
            verify=False)
    location = r.headers['location']
    verifier_index = location.index('oauth_verifier=')
    verifier = location[verifier_index+15:]
    oauth = OAuth1Session(app_key, client_secret=app_secret,
            resource_owner_key=tokens['oauth_token'],
            resource_owner_secret=tokens['oauth_token_secret'],
            verifier=verifier)
    access_tokens = oauth.fetch_access_token("%s/oauth/access_token" % api_url, verify=False)
    return (access_tokens['oauth_token'], access_tokens['oauth_token_secret'])

if __name__ == '__main__':
    api_url = raw_input('Abiquo API endpoint: ')
    identity = raw_input('Username or OpenID access_token (prefixed with "openid:"): ')
    credential = None if identity.startswith('openid:') else raw_input('Password: ')
    appkey = raw_input('Api Key: ')
    appsecret = raw_input('Api Secret: ')
    credentials = Credentials(identity, credential)
    access_token, access_token_secret = get_access_token(api_url, credentials, appkey, appsecret)
    print "Access token: %s\nAccess token secret: %s" % (access_token, access_token_secret)

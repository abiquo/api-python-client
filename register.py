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

from requests_oauthlib import OAuth1Session


def register_app(api_url, identity, credential, app_name):
    """ Registers a new Application in the Abiquo API. """ 
    user_info = requests.get("%s/login" % api_url,
            auth=(identity, credential),
            headers={'Accept': 'application/vnd.abiquo.user+json'})
    app_link = filter(lambda l: l['rel'] == 'applications', user_info.json()['links'])[0]
    app = requests.post(app_link['href'],
            auth=(identity, credential),
            headers={'Content-type': 'application/vnd.abiquo.application+json'},
            data=json.dumps({'name': app_name})).json()
    return (app['apiKey'], app['apiSecret'])

def get_access_token(api_url, identity, credential, app_key, app_secret):
    """ Generates a pair of authorized tokens for a given application. """
    oauth = OAuth1Session(app_key, client_secret=app_secret, callback_uri='oob')
    tokens = oauth.fetch_request_token("%s/oauth/request_token" % api_url)
    r = requests.get("%s/oauth/authorize?oauth_token=%s" % (api_url, tokens['oauth_token']),
            auth=(identity, credential),
            allow_redirects=False)
    location = r.headers['location']
    verifier_index = location.index('oauth_verifier=')
    verifier = location[verifier_index+15:]
    oauth = OAuth1Session(app_key, client_secret=app_secret,
            resource_owner_key=tokens['oauth_token'],
            resource_owner_secret=tokens['oauth_token_secret'],
            verifier=verifier)
    access_tokens = oauth.fetch_access_token("%s/oauth/access_token" % api_url)
    return (access_tokens['oauth_token'], access_tokens['oauth_token_secret'])

if __name__ == '__main__':
    api_url = raw_input('Abiquo API endpoint: ')
    identity = raw_input('Username: ')
    credential = raw_input('Password: ')
    app_name = raw_input('Application name: ')
    appkey, appsecret = register_app(api_url, identity, credential, app_name)
    access_token, access_token_secret = get_access_token(api_url, identity, credential, appkey, appsecret)
    print "App key: %s\nApp secret: %s" % (appkey, appsecret)
    print "Access token: %s\nAccess token secret: %s" % (access_token, access_token_secret)

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

import httpretty

from abiquo.client import Abiquo
from urlparse import urlparse

api = Abiquo(url="http://fake/api", auth=('user', 'name'))

def register(method, uri, status, body):
    httpretty.register_uri(
        method=method, 
        uri=uri,
        body=body,
        status=status)
    
def assert_request(self, expected_path, method=None, params=None, headers=None, 
    body=None, status=None):
    request = httpretty.last_request()
    if method:
        self.assertEqual(method, request.method)
    if params:
        for param, value in params.items():
            self.assertIn(param, request.querystring)
            self.assertIn(value,request.querystring[param])
    if headers:
        self.assertTrue(all(item in request.headers.items() for item in headers.items()))
    if body:
        self.assertEqual(urlparse(request.path).path, expected_path)

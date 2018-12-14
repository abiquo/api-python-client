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
import json
import unittest

from . import *
from abiquo.client import ObjectDto
    
class TestObjectDto(unittest.TestCase):   
    @classmethod
    def setUpClass(cls):
        httpretty.enable()

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()

    def test_object_accessors(self):
        obj = ObjectDto(json={}, content_type='dummy')
        obj.newprop = 'foo'
        obj.content_type = 'updated'
        obj.newprop = 'bar'

        self.assertEqual(obj.__dict__['content_type'], 'updated')
        self.assertEqual(obj.content_type, 'updated')
        self.assertEqual(obj.json['newprop'],'bar')
        self.assertNotIn('newprop', obj.__dict__)
        self.assertEqual(obj.newprop, 'bar')

    def test_object_links_accessors(self):
        data = {'links': [{'rel': 'foo', 'type': 'bar', 'href': 'http://localhost'}]}
        obj = ObjectDto(data)

        linked = obj.foo
        self.assertIn('http://localhost', linked.headers)
        self.assertEqual(linked.headers['http://localhost']['accept'], 'bar')

    def test_put_self(self):
        data = {'foo':'bar','links':[{'rel':'edit','href':'http://fake/api/admin/datacenters/1',
            'type':'application/vnd.abiquo.datacenter+json'}]}
        register('GET', 'http://fake/api/admin/datacenters/1', 200, json.dumps(data))

        updated = data
        updated['foo'] = 'updated'
        register('PUT', 'http://fake/api/admin/datacenters/1', 200, json.dumps(updated))

        res, obj = api.admin.datacenters.get(id='1')
        obj.foo = 'updated'
        code, obj_put = obj.put()

        assert_request(self, '/api/admin/datacenters/1', method='PUT', body=json.dumps(updated),
                headers={'accept': 'application/vnd.abiquo.datacenter+json',
                         'content-type': 'application/vnd.abiquo.datacenter+json'})
        self.assertEqual(code, 200)
        self.assertEqual(obj.foo, obj_put.foo)

    def test_delete_self(self):
        data = {'foo':'bar','links':[{'rel':'edit','href':'http://fake/api/admin/datacenters/1',
            'type':'application/vnd.abiquo.datacenter+json'}]}
        register('GET', 'http://fake/api/admin/datacenters/1', 200, json.dumps(data))
        register('DELETE', 'http://fake/api/admin/datacenters/1', 204, '{}')

        res, obj = api.admin.datacenters.get(id='1')
        code, resp = obj.delete()

        assert_request(self, '/api/admin/datacenters/1', method='DELETE')
        self.assertEqual(code, 204)

    def test_refresh_self(self):
        data = json.dumps({'foo':'bar','links':[{'rel':'edit','href':'http://fake/api/admin/datacenters/1',
            'type':'application/vnd.abiquo.datacenter+json'}]})
        register('GET', 'http://fake/api/admin/datacenters/1', 200, data)
        register('DELETE', 'http://fake/api/admin/datacenters/1', 200, data)

        res, obj = api.admin.datacenters.get(id='1')
        code, obj_refresh = obj.refresh()

        assert_request(self, '/api/admin/datacenters/1', method='GET',
                headers={'accept': 'application/vnd.abiquo.datacenter+json'})
        self.assertEqual(code, 200)
        self.assertEqual(obj.foo, obj_refresh.foo)

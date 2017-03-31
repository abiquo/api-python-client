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

import unittest

from abiquo.client import ObjectDto
    
class TestObjectDto(unittest.TestCase):   

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


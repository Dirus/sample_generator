import json
import unittest
import datetime

from instantiate import instantiate

class InstantiateTest(unittest.TestCase):
# Test suit for Primitives
    def test_should_instantiate_string(self):
        schema = {
            'type':'string'
        }
        result = instantiate(schema)
        if isinstance(result,str):
            type = True
        self.assertTrue(type)

    def test_should_instantiate_null(self):
        schema = {
            'type': 'null'
        }
        result = instantiate(schema)
        expected = None
        self.assertEqual(expected, result)

    def test_should_instantiate_number(self):
        schema = {'type': 'number'}

        result = instantiate(schema)
        expected = 0
        self.assertEqual(expected,result)

    def test_should_instantiate_boolean(self):
        schema = {
            'type': 'boolean'
        }
        result = instantiate(schema)
        expected = 'false'
        self.assertEqual(expected,result)

    def test_should_use_default_property(self):
        schema = {
            'type': 'number',
            'default': 4000
        }
        result = instantiate(schema)
        expected = 4000
        self.assertEqual(expected, result)
    
    def test_should_instantiate_date(self):
        schema = {
            'type': 'string',
            'format': 'date'
        }
        result = instantiate(schema)
        datetime_object = datetime.datetime.strptime(result, '%Y-%m-%d')
        self.assertTrue(isinstance(datetime_object, datetime.datetime))
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
            schema_type = True
        self.assertTrue(schema_type)

    def test_should_instantiate_string_with_minlength_maxlength(self):
        schema = {
            'type':'string',
            'minLength':5,
            'maxLength':10
        }
        result = instantiate(schema)
        self.assertIn(len(result),range(5,10))

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
        self.assertTrue(0 < result < 1000000)

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
    
    def test_should_instantiate_number_with_min_max_values(self):
        schema = {
            'type': 'number',
            'minimum': 1,
            'maximum': 6
        }
        result = instantiate(schema)
        self.assertIn(result,[1,2,3,4,5,6])
# Test Suite for Objects
    def test_should_instantiate_object_without_properties(self):
        schema = {
            'type': 'object'
        }
        result = instantiate(schema)
        expected = {}
        self.assertEqual(result, expected)

    def test_should_instantiate_object_with_property(self):
        schema = {
            'type': 'object',
            'properties': {
                'title': {
                    'type': 'string'
                }
            }
        }
        result = instantiate(schema)
        self.assertIn('title', result)
        self.assertTrue(len(result['title']) > 0)
import json
import string
from random import choice, randint, randrange
import datetime

# The JSON Object that defines the default values of certain types.
typesInstantiator = {
  'string': '',
  'number': 0,
  'integer': 0,
  'null': None,
  'boolean': 'false', 
  'object': {},
}

# Generates a random string with min/max lengths
# @params min_size - minLength for string
# @params max_size - maxLength for string
# @params allowed_chars - allowed character set for string generation
def random_string_generator_variable_size(min_size, max_size, allowed_chars):
    return ''.join(choice(allowed_chars) for x in range(randint(min_size, max_size)))

# Checks whether a property is on required array.
# @param property - the property to check.
# @param requiredArray - the required array.
def isPropertyRequired(property,requiredArray):
    found = False
    for item in requiredArray:
        if item == property:
            found = True
    return found

def shouldVisit(property, obj, options):
    if options['requiredPropertiesOnly']:
        # Return True if required array is present in schema object in case of options{true}.
        if obj.get('required'):
            return isPropertyRequired(property, obj['required'])
        else: 
            return False
    # Return true as requirePropertiesOnly not required hence visit all properties.
    return True

#  Extracts the type of the object.
#  @param obj - An object.
def getObjectType(obj):
    return obj.get('type')

#  Instantiate a primitive.
#  @param obj - The object that represents the primitive.
def instantiatePrimitive(obj,name):
    if obj.get('default'):
        return obj['default']
    # Provide current date with YYYY-MM-DD format
    if obj.get('format') == 'date':
        return (datetime.datetime.now()-datetime.timedelta(days=randint(0, 366))).strftime("%Y-%m-%d")
    obj_type = obj.get('type')
    # Instantiate for string values
    if obj_type == 'string':
        obj['minLength'] = obj.get('minLength') or 1
        obj['maxLength'] = obj.get('maxLength') or 9
        chars = string.ascii_lowercase
        return random_string_generator_variable_size(obj['minLength'], obj['maxLength'], chars)
    # Instantiate for numbers
    if obj_type in ('number', 'integer'):
        obj['minimum'] = obj.get('minimum') or 1
        obj['maximum'] = obj.get('maximum') or 999999
        return randint(obj['minimum'], obj['maximum'])
    return typesInstantiator[obj_type]

#  The main function.
#  Calls sub-objects recursively, depth first, using the sub-function 'visit'.
#  @param schema - The schema to instantiate.
#  @param options - options to include only required properties or not.
def instantiate(schema,options=None):
    if options is None:
        options = {'requiredPropertiesOnly': False}

    # traverse through a dictionary recursively.
    def traverseDict(obj, name, data):
        if isinstance(data,dict) and data.get(name) is None:
            data[name] = {}
        elif isinstance(data,list):
            data.append({})

        # Visit each property
        for key,value in obj['properties'].items():
            if shouldVisit(key, obj, options):
                visit(value,key,data[name])
    #    Visits each sub-object using recursion.
    #    If it reaches a primitive, instantiate it.
    #    @param obj - The object that represents the schema.
    #    @param name - The name of the current object.
    #    @param data - The instance data that represents the current object.
    def visit(obj, name, data):
        obj_type = getObjectType(obj)
         # We want non-primitives objects (primitive == object w/o properties).
        if obj_type == 'object' and obj.get('properties'):
            traverseDict(obj,name,data)
        # elif isinstance(obj,dict):
        #     if isinstance(data,dict) and data.get(name) is None:
        #         data[name] = {}
        #     elif isinstance(data,list) and ({} not in data):
        #         data.append({})
        # instantiate primitives
        elif obj.get('type'):
            data[name] = instantiatePrimitive(obj, name)

    data = {}
    visit(schema,'schema',data)
    return data['schema']

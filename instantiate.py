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
def is_property_required(property,required_array):
    found = False
    for item in required_array:
        if item == property:
            found = True
    return found

def should_visit(property, obj, options):
    if options['requiredPropertiesOnly']:
        # Return True if required array is present in schema object in case of options{true}.
        if obj.get('required'):
            return is_property_required(property, obj['required'])
        else: 
            return False
    # Return true as requirePropertiesOnly not required hence visit all properties.
    return True

#  Extracts the type of the object.
#  @param obj - An object.
def get_object_type(obj):
    return obj.get('type')

#  Instantiate a primitive.
#  @param obj - The object that represents the primitive.
def instantiate_primitive(obj,name):
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

#  Checks whether a variable is an enum.
#  @param obj - an object.
def is_enum(obj):
    if obj.get('enum') or obj.get('enumDescriptions'):
        return True
    return False

#  Instantiate an enum.
#  @param obj - The object that represents the primitive.
def instantiate_enum(obj):
    if obj.get('enum'):
        return obj['enum'][randrange(0,len(obj['enum']))]
    else:
        return list(obj['enumDescriptions'].keys())[randrange(0, len(obj['enumDescriptions']))]


#  The main function.
#  Calls sub-objects recursively, depth first, using the sub-function 'visit'.
#  @param schema - The schema to instantiate.
#  @param options - options to include only required properties or not.
def instantiate(schema,options=None):
    if options is None:
        options = {'requiredPropertiesOnly': False}

    # traverse through a dictionary recursively.
    def traverse_dict(obj, name, data):
        if isinstance(data,dict) and data.get(name) is None:
            data[name] = {}
        elif isinstance(data,list):
            data.append({})

        # Visit each property
        for key,value in obj['properties'].items():
            if should_visit(key, obj, options):
                visit(value,key,data[name])

    # traverse through a list recursively
    def traverse_list(obj,name,data):
        if isinstance(data,dict):
            if data.get(name) is None or len(data[name]) == 0:
                data[name] = []
            # To have minimum one item in array if minItems not provided.
            length = 1
            if obj.get('minItems'):
                length = obj['minItems']
            # Instantiate 'length' items.
            if obj.get('items'):
                for i in range(length):
                    # Array items can contain, allOf, anyOf condition
                    visit(obj['items'], i, data[name])

    #    Visits each sub-object using recursion.
    #    If it reaches a primitive, instantiate it.
    #    @param obj - The object that represents the schema.
    #    @param name - The name of the current object.
    #    @param data - The instance data that represents the current object.
    def visit(obj, name, data):
        obj_type = get_object_type(obj)
        # We want non-primitives objects (primitive == object w/o properties).
        if obj_type == 'object' and obj.get('properties'):
            traverse_dict(obj,name,data)
        elif isinstance(obj,dict) and (('oneOf' in obj and obj['oneOf']) or ('anyOf' in obj and obj['anyOf'])):
            # if data does not contain name and is object
            if isinstance(data,dict) and data.get(name) is None:
                data[name] = {}
            # if data is list and empty
            elif isinstance(data,list) and ({} not in data):
                data.append({})
            if obj_type == 'array':
                traverse_list(obj, name, data)
            if 'oneOf' in obj and obj['oneOf']:
                visit(obj['oneOf'][0],name,data)
            if 'anyOf' in obj and obj['anyOf']:
                visit(obj['anyOf'][0],name,data)

        # instantiate primitives
        elif obj_type == "array":
            traverse_list(obj,name,data)
        elif is_enum(obj):
            data[name] = instantiate_enum(obj)
        elif obj.get('type'):
            if isinstance(data, list):
                data.append(instantiate_primitive(obj, name))
            else:
                data[name] = instantiate_primitive(obj, name)

    data = {}
    visit(schema,'schema',data)
    return data['schema']

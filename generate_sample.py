import json
from instantiate import instantiate

class JSONSample(object):

    def __init__(self,schema):
        self.schema = schema
        self.sample_data = {}

    def generate_sample(self):
        return self._generate_sample()

    def _generate_sample(self):
        sample = instantiate(self.schema)
        return sample

f= open('schema.json')
schema = json.loads(f.read())
obj = JSONSample(schema)
sample = obj.generate_sample()
print(json.dumps(sample,indent=4, separators=(',', ': ')))



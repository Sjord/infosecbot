import json
from infosecbot.model import Link

datafile = 'data.json'

class Storage(dict):
    def __init__(self):
        with open(datafile, 'r') as fp:
            self.update(json.load(fp))
        self['urls'] = [Link(u) for u in self['urls']]

    def save(self):
        serialized = json.dumps(dict(self), default=self.serialize)
        with open(datafile, 'w') as fp:
            fp.write(serialized)

    def serialize(self, obj):
        return obj.__dict__
        

storage = Storage()

if __name__ == "__main__":
    s = Storage()
    s['test'] = 1
    s.save()
    print(s)

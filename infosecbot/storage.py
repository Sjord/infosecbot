import json
from infosecbot.model import Link

datafile = 'data.json'

class Storage(dict):
    def __init__(self):
        self.load()

    def load(self):
        with open(datafile, 'r') as fp:
            self.update(json.load(fp))
        self['links'] = [Link.unserialize(u) for u in self['links']]

    def save(self):
        serialized = json.dumps(dict(self), default=self.serialize)
        with open(datafile, 'w') as fp:
            fp.write(serialized)

    def serialize(self, obj):
        return obj.__dict__

    def get_link(self, id):
        matches = [l for l in self['links'] if l.id == id]
        assert len(matches) == 1
        return matches[0]
        

storage = Storage()

if __name__ == "__main__":
    s = Storage()
    s['test'] = 1
    s.save()
    print(s)

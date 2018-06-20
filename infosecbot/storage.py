import json
from infosecbot.model import Link
from fcntl import flock, LOCK_SH, LOCK_EX

datafile = 'data.json'

class Storage(dict):
    def __init__(self):
        self.load()

    def load(self):
        with open(datafile, 'r') as fp:
            flock(fp, LOCK_SH)
            self.update(json.load(fp))
        self['links'] = [Link.unserialize(u) for u in self['links']]

    def save(self):
        serialized = json.dumps(dict(self), default=self.serialize)
        with open(datafile, 'w') as fp:
            flock(fp, LOCK_EX)
            fp.write(serialized)

    def serialize(self, obj):
        return obj.serialize()

    def get_link(self, id):
        matches = [l for l in self['links'] if l.id == id]
        assert len(matches) == 1
        return matches[0]

    def find_link_by_url(self, url):
        matches = [l for l in self['links'] if l.url== url]
        assert len(matches) <= 1
        if not matches:
            return None
        return matches[0]
        

storage = Storage()

if __name__ == "__main__":
    s = Storage()
    s['test'] = 1
    s.save()
    print(s)

import json

datafile = 'data.json'

class Storage(dict):
    def __init__(self):
        with open(datafile, 'r') as fp:
            self.update(json.load(fp))

    def save(self):
        with open(datafile, 'w') as fp:
            json.dump(dict(self), fp)
        

storage = Storage()

if __name__ == "__main__":
    s = Storage()
    s['test'] = 1
    s.save()
    print(s)

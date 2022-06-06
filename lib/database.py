import json
from google.cloud import datastore


class Database:

    def get_feedback(self):
        return self.query(kind='отзыв')

    def query(self, kind):
        pass


class DatabaseDict(Database):

    def __init__(self):

        self.dictionary = {}
        self.last_id = 0

    def add_note(self, info, kind="отзыв"):

        self.last_id += 1
        info['kind'] = kind
        self.dictionary[self.last_id] = info

    def query(self, kind):

        result = []
        for el in self.dictionary.values():
            if el['kind'] == kind:
                result.append(el)
        return result



class DatabaseJSON(Database):
    filename = "files/db.json"

    def __init__(self):

        # Open file with the database
        f = open(self.filename, "r")

        # Create dictionary with entities
        self.dictionary = {}
        self.dictionary = json.load(f)

        # Store last id of the note
        if len(self.dictionary.keys()) == 0:
            self.last_id = 0
        else:
            ids = [int(x) for x in self.dictionary.keys()]
            self.last_id = max(ids)

        # Close the file
        f.close()

    def add_note(self, info, kind="отзыв"):

        self.last_id += 1
        info['kind'] = kind
        self.dictionary[self.last_id] = info

        self.save()

    def save(self):

        # Open file with the database
        f = open(self.filename, "w", encoding='utf8')

        json.dump(self.dictionary, f, ensure_ascii=False, indent=2)

        f.close()

    def query(self, kind):

        result = []
        for el in self.dictionary.values():
            if el['kind'] == kind:
                result.append(el)
        return result


class DatabaseDatastore(Database):

    def __init__(self):

        self.client = datastore.Client()

    def add_note(self, info):

        key = self.client.key('отзыв')
        entity = datastore.Entity(key)

        entity.update(info)

        self.client.put(entity)

    def query(self, kind):

        query = self.client.query(kind=kind)
        result = list(query.fetch())

        result_dicts = []
        for el in result:
            result_dicts.append(dict(el))

        return result_dicts

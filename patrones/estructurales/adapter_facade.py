from ..struct_data import is_struct
from exceptions import NoDocumentDatabaseException
import pymongo
import couchdb


class DocumentDatabaseBackend(object):
    def get_collection(self, coll_name):
        raise NoDocumentDatabaseException("A document database should be set for this model")

    def set_doc(self, coll_name, doc):
        collection = self.get_collection(coll_name)
        self._serialize(doc)
        collection.save(doc)

    def get_doc(self, coll_name, fdoc, struct_class=None):
        collection = self.get_collection(coll_name)
        doc = collection.find_one(fdoc)
        if doc and struct_class:
            return struct_class(**doc)
        return doc

    def find_docs(self, coll_name, fdoc=None, struct_class=None):
        collection = self.get_collection(coll_name)
        for doc in collection.find(fdoc):
            if doc and struct_class:
                yield struct_class(**doc)
            yield doc

    def delete_doc(self, coll_name, fdoc, struct_class = None):
        collection = self.get_collection(coll_name)
        doc = collection.remove(fdoc)
        if doc and struct_class:
            return struct_class(**doc)
        return doc

    def teardown(self, coll_name):
        raise NoDocumentDatabaseException("A document database should be set for this model")

    def _serialize(self, document):
        for k, v in document.items():
            if k != '_id' and is_struct(v):
                document[k] = v.to_struct()
            elif k == '$set' and isinstance(v, dict):
                for k2, v2 in v.items():
                    if k2 != '_id' and is_struct(v2):
                        v[k2] = v2.to_struct()


class MemoryDatabase(dict):
    pass


class Searchable(object):
    def _search(self, find_doc, document):
        for key, value in find_doc.iteritems():
            if not document.has_key(key) or document[key] != value:
                return False
        return True

    def find_one(self, find_doc):
        for document in self.get_all():
            if self._search(find_doc, self.clean_document(document)):
                return self.clean_document(document)

    def find(self, find_doc):
        for document in self.get_all():
            if self._search(find_doc, self.clean_document(document)):
                yield self.clean_document(document)

    def remove(self, find_doc):
        delete_index = None
        for index, document in enumerate(self.get_all()):
            if self._search(find_doc, document):
                delete_index = index
                break
        if delete_index is not None:
            return self.get_all().pop(delete_index)
        return None


class MemoryCollection(list, Searchable):
    def __init__(self, db, name):
        super(MemoryCollection, self).__init__()
        self.__DATABASE__ = db
        self.__NAME__ = name

    def get_all(self):
        return self

    def clean_document(self, document):
        return document

    def save(self, doc):
        to_update = None

        for index, document in enumerate(self.get_all()):
            if document['_id'] == doc['_id']:
                to_update = index
                break

        if to_update:
            self.get_all().pop(to_update)

        self.get_all().append(doc)

        self.__DATABASE__[self.__NAME__] = self.get_all()


class MemoryDatabaseBackend(DocumentDatabaseBackend):
    def __init__(self):
        super(MemoryDatabaseBackend, self).__init__()
        self.__CONTENT__ = MemoryDatabase()

    def get_collection(self, coll_name):
        return self.__CONTENT__.get(coll_name, MemoryCollection(self.__CONTENT__, coll_name))

    def get_contents(self):
        return self.__CONTENT__

    def teardown(self, coll_name):
        self.__CONTENT__[coll_name] = MemoryCollection(self.__CONTENT__, coll_name)
        return True

    def clean(self):
        self.__CONTENT__ = MemoryDatabase()


class MongoDatabaseBackend(DocumentDatabaseBackend):
    def __init__(self, mongo_uri, mongo_name):
        self.db = pymongo.Connection(mongo_uri)[mongo_name]

    def get_collection(self, coll_name):
        return self.db[coll_name]

    def teardown(self, coll_name):
        return bool(self.db[coll_name].remove())


class CouchDatabaseCollection(Searchable):
    def __init__(self, collection):
        self.__COLLECTION__ = collection

    def get_all(self):
        return self.__COLLECTION__.view('_all_docs', include_docs=True)

    def clean_document(self, document):
        def as_struct(document):
            clean = {}
            for k, v in document.iteritems():
                clean[k] = v
            return clean

        return as_struct(document.doc)

    def save(self, doc):
        _id = doc.pop('_id')
        self.__COLLECTION__[_id] = doc


class CouchDatabaseBackend(DocumentDatabaseBackend):
    def __init__(self, server=None):
        if server is None:
            self.server = couchdb.Server()
        else:
            self.server = couchdb.Server(server)

    def get_collection(self, coll_name):
        try:
            return CouchDatabaseCollection(self.server[coll_name])
        except couchdb.ResourceNotFound:
            return CouchDatabaseCollection(self.server.create(coll_name))

    def teardown(self, coll_name):
        try:
            del self.server[coll_name]
            return True
        except couchdb.ResourceNotFound:
            return False



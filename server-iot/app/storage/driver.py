from typing import List, Optional, TypeVar, Generic
from .client import get_connection
from bson import ObjectId
from decouple import config

TDom = TypeVar('TDom')
FDom = TypeVar('FDom')
DB_NAME = config('DB_NAME')

class MongoDBDriver(Generic[TDom, FDom]):

    def __init__(self,collection_name:str):
        self.client =  get_connection()
        self.db = self.client[DB_NAME]
        self.collection = self.db[collection_name]

    def create(self, item: TDom) -> TDom:
        result = self.collection.insert_one(item)
        return result

    def update(self, id:str|ObjectId, item: TDom) -> Optional[TDom]:
        result = self.collection.update_one({'_id': ObjectId(id)}, {'$set': item})
        if result.raw_result['n'] > 0:
            return item
        else:
            return None

    def delete(self, id:str) -> bool:
        result = self.collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count > 0

    def get_all(self, filter:FDom, options):
        cursor = self.collection.find(filter, **options)
        return [doc for doc in cursor]

    def get_one(self, id:str|ObjectId) -> Optional[TDom]:
        return self.collection.find_one({'_id': ObjectId(id)})

    def count_registers(self, filter:FDom) -> int:
        return self.collection.count_documents(filter)

    def upsert_docs(self, query, items:TDom) -> TDom:
        result = self.collection.update_many(query, {'$set': items}, upsert=True)
        return items

    def create_many(self, items : List[TDom]) -> List[TDom]:
        result = self.collection.insert_many(items)
        return items

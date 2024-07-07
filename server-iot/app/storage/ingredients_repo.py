import uuid
import datetime
import json
from .driver import MongoDBDriver

COLLECTION_NAME = 'ingredient-list'


class IngredientListMongoRepository:

    def __init__(self):
        self.driver = MongoDBDriver(COLLECTION_NAME)
        return None

    def create(self, ingredients,recipes):
        item = {}
        item['_id'] = str(uuid.uuid4())
        item['date'] = datetime.datetime.now()
        item['ingredients'] = json.loads(ingredients)
        item['recipes'] = json.loads(recipes)

        res_item = self.driver.create(item)
        res_item = self.mapObjectToStr(res_item.inserted_id)
        return res_item

    def get_one(self, id):
        res = self.driver.get_one(id)
        res['_id'] = self.mapObjectToStr(res['_id'])
        return res
    
    def get_all(self, filter, options):
        res = self.driver.get_all(filter, options)
        for item in res:
            item['_id'] = self.mapObjectToStr(item['_id'])
        return res
    
    def update(self, id, item):
        res_item = self.driver.update(id, item)
        if res_item is not None:
            return res_item
        else:
            raise Exception("No se ha podido actualizar el producto")
    
    def delete(self, id):
        res = self.driver.delete(id)
        return res

    def mapObjectToStr(self, item):
        return str(item)
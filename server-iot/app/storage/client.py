from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from decouple import config

MONGO_USER = config('MONGO_USER')
MONGO_PASSWORD = config('MONGO_PASSWORD')
MONGO_HOST = config('MONGO_HOST')
MONGO_CLUSTER = config('MONGO_CLUSTER')
DB_NAME = config('DB_NAME')

MONGO_URI = f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{DB_NAME}?retryWrites=true&w=majority&appName={MONGO_CLUSTER}'

def get_connection():
    try:
        client = MongoClient(MONGO_URI)
        return client
    except ConnectionFailure as ex:
        raise ex
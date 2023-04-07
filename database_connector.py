import pymongo
from settings import MONGODB_HOST, MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_DB_NAME


if not MONGODB_HOST or not MONGODB_USERNAME or not MONGODB_PASSWORD or not MONGODB_DB_NAME:
    raise ValueError('Missing MongoDB configuration')

uri = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}/?retryWrites=true&w=majority"


class DatabaseConnector:
    def __init__(self):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[MONGODB_DB_NAME]
        self.users = self.db['users']

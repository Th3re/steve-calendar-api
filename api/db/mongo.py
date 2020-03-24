import pymongo

from api.db.store import Store
from api.model.credentials import Credentials


class MongoStore(Store):
    USER_ID = 'userId'
    REFRESH_TOKEN = 'refreshToken'

    def __init__(self, client: pymongo.MongoClient, database, collection):
        self.client = client
        self.collection = self.client[database][collection]

    def save(self, credentials: Credentials):
        document = {
            '$set': {
                self.USER_ID: credentials.user_id,
                self.REFRESH_TOKEN: credentials.refresh_token,
            }
        }
        query = {
            self.USER_ID: credentials.user_id
        }
        self.collection.find_one_and_update(query, document, upsert=True)

    def get(self, user_id) -> Credentials:
        query = {
            self.USER_ID: user_id
        }
        document = self.collection.find_one(query)
        return Credentials(user_id=user_id, refresh_token=document[self.REFRESH_TOKEN])

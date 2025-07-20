from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
from config import Config

class Database:
    def __init__(self):
        self.config = Config.get_mongo_config()
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        try:
            self.client = MongoClient(self.config["uri"])
            self.db = self.client[self.config["dbname"]]
            return True
        except ConnectionFailure:
            return False
    
    def insert_donation(self, record):
        try:
            result = self.db.donations.insert_one(record)
            return result.inserted_id is not None
        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    def get_donations(self, query=None):
        try:
            if query is None:
                query = {}
            return list(self.db.donations.find(query).sort("donation_date", -1))
        except Exception as e:
            print(f"Database error: {e}")
            return []
    
    def delete_donation(self, donation_id):
        try:
            from bson import ObjectId
            result = self.db.donations.delete_one({"_id": ObjectId(donation_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Database error: {e}")
            return False
        
    def close(self):
        if self.client:
            self.client.close()
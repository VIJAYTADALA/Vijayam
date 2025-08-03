from pymongo import MongoClient
from config import Config
from bson import ObjectId
from datetime import datetime
import streamlit as st

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.DB_NAME]
        self.collection = self.db[Config.COLLECTION_NAME]

    def get_donations(self, page=1, per_page=Config.ITEMS_PER_PAGE):
        skip = (page - 1) * per_page
        donations = list(self.collection.find().skip(skip).limit(per_page))
        total = self.collection.count_documents({})
        return donations, total

    def get_donation_by_id(self, donation_id):
        return self.collection.find_one({"_id": ObjectId(donation_id)})

    def add_donation(self, donor, amount, date, notes):
        donation = {
            "donor": donor,
            "amount": float(amount),
            "date": datetime.strptime(date, "%Y-%m-%d"),
            "notes": notes,
            "created_at": datetime.now()
        }
        result = self.collection.insert_one(donation)
        return result.inserted_id

    def update_donation(self, donation_id, donor, amount, date, notes):
        result = self.collection.update_one(
            {"_id": ObjectId(donation_id)},
            {"$set": {
                "donor": donor,
                "amount": float(amount),
                "date": datetime.strptime(date, "%Y-%m-%d"),
                "notes": notes,
                "updated_at": datetime.now()
            }}
        )
        return result.modified_count > 0

    def delete_donation(self, donation_id):
        result = self.collection.delete_one({"_id": ObjectId(donation_id)})
        return result.deleted_count > 0

    def close(self):
        self.client.close()

        
# Cache decorator with version compatibility
if hasattr(st, 'cache_resource'):
    cache_decorator = st.cache_resource
elif hasattr(st, 'experimental_singleton'):
    cache_decorator = st.experimental_singleton
else:
    cache_decorator = st.cache(allow_output_mutation=True)

@cache_decorator
def get_db():
    return Database()
"""
MongoDB CRUD Operations for BMI Data
DADS6005 Data Streaming — Quiz 1 (MongoDB)
"""

import os
from datetime import datetime
from pymongo import MongoClient, errors
from bson.objectid import ObjectId


class MongoDBManager:
    def __init__(self, connection_string: str = "mongodb://localhost:27017"):
        self.client = MongoClient(connection_string)
        self.db = self.client.person_collection
        self.collection = self.db.bmi

    def ping(self) -> bool:
        try:
            self.client.admin.command('ping')
            return True
        except errors.ConnectionFailure:
            return False

    def list_databases(self) -> list:
        return self.client.list_database_names()

    def list_collections(self) -> list:
        return self.db.list_collection_names()

    def insert_doc(self, comname: str, weight: float, height: float, bmi: float) -> str:
        doc = {
            "_computer_name": comname,
            "_weight": float(weight),
            "_height": float(height),
            "_bmi": round(float(bmi), 2),
            "_date": datetime.today().strftime('%Y-%m-%d')
        }
        result = self.collection.insert_one(doc)
        return str(result.inserted_id)

    def find_all(self) -> list:
        return list(self.collection.find())

    def find_by_id(self, doc_id: str) -> dict:
        return self.collection.find_one({"_id": ObjectId(doc_id)})

    def replace_one(self, doc_id: str, comname: str, weight: float, height: float, bmi: float) -> bool:
        new_doc = {
            "_computer_name": comname,
            "_weight": float(weight),
            "_height": float(height),
            "_bmi": round(float(bmi), 2),
            "_date": datetime.today().strftime('%Y-%m-%d')
        }
        result = self.collection.replace_one({"_id": ObjectId(doc_id)}, new_doc)
        return result.modified_count > 0

    def delete_by_id(self, doc_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(doc_id)})
        return result.deleted_count > 0

    def close(self):
        self.client.close()

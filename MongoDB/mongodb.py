import os
import pprint
from pymongo import MongoClient
from datetime import datetime

#เชื่อมต่อ mongoDB
connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)

#print เพื่อดู db ที่มีทั้งหมด 
dbs = client.list_database_names() 
print(dbs) 

#กำหนดตัวแปร db ไปหา collection ใน db นั้น เทียบ sql คือ database -> table
db = client.person_collection

#print เพื่อดู collection ที่มีทั้งหมด 
collection = db.list_collection_names() 
print(collection)

collection = db.bmi

#I Insert / Create
def insert_doc(comname,weight,height,bmi):
    collection = db.bmi
    insert_data = {
        "_computer_name"    : comname,
        "_weight"   : weight,
        "_height"   : height,
        "_bmi"      : bmi,
        "_date"     : datetime.today().strftime('%Y-%m-%d')
    }
    collection.insert_one(insert_data)
    ins_id = collection.insert_one(insert_data).inserted_id
    print(ins_id)

printer = pprint.PrettyPrinter()
#R Read ค้นหาข้อมูลใน collection
def find_all_people():
    #SELECT * FROM person
    people = collection.find()
    return list(people)

#U Update การอัพเดตข้อมูลใน collection
def replace_one(ids,comname,weight,height,bmi): 
    from bson.objectid import ObjectId
    _id = ObjectId(ids)
    new_doc = {
        "_computer_name": comname,
        "_weight" : weight,
        "_height" : height,
        "_bmi"  : bmi,
        "_date" : datetime.today().strftime('%Y-%m-%d')
    }

    collection.replace_one({"_id":_id},new_doc)

#D ลบ
def delete_doc_by_id(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)
    collection.delete_one({"_id" : _id}) #ลบ 1 row
    return _id



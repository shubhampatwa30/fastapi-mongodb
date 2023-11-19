import asyncio
import config
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class Student(BaseModel):
    name: str
    age: int

app = FastAPI()

uri = config.uri
client = AsyncIOMotorClient(uri)



db = client["library"]

students_collection = db.students
books_collection = db.books
books_lent = db.books_lent


@app.get("/")
async def root():
    return {"message": "Heath check succeeded"}



@app.post("/students/", response_description="Add new student",response_model=Student)
async def insert_student(student: Student):
    student = jsonable_encoder(student)
    new_student = await students_collection.insert_one(student)
    created_student = await students_collection.find_one({"_id": new_student.inserted_id})
    return created_student


@app.delete("/student/{student_name}", response_description="Delete a student")
async def delete_student(student_name: str):
    # document = {"name": student}
    result = await students_collection.delete_one({ "name": student_name });
    # print("result %s" % repr(result.inserted_id))
    return {"student_deleted": student_name}

@app.put("/students/{old_student_name}", response_description="Update a student")
async def update_student(old_student_name: str, new_student_name: str):
    old_document = await students_collection.find_one({"name": old_student_name})
    _id = old_document["_id"]
    result = await students_collection.replace_one({"_id": _id}, {"name": new_student_name})
    return {"Student Updated: ": new_student_name}
    
@app.get("/students/{student_id}")
async def get_student_by_id(student_id):
    document = await students_collection.find_one({"_id": ObjectId(student_id)})
    if document != None:
        return {"Student": document['name']}
    
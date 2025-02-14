import os
import tempfile
from functools import reduce
from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin@localhost:27017/")
db = client["student_db"]
students_db = db["students"]


def add(student=None):
    # Checking if the student exists
    existing_student = students_db.find_one({
        "first_name": student.first_name,
        "last_name": student.last_name
    })

    if existing_student:
        return "the student already exists", 409  # The student can't be added because it already exists

    # Insert student and and get ID
    result = students_db.insert_one(student.to_dict())
    student.student_id = str(result.inserted_id)  # Turn to string
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = students_db.find_one({"_id": student_id}, {"_id": 0})

    if not student:
        return "not found", 404

    return student


def delete(student_id=None):
    result = students_db.delete_one({"_id": student_id})

    if result.deleted_count == 0:
        return "not found", 404

    return student_id
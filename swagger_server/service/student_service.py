import os
import tempfile
from functools import reduce
from bson import ObjectId
from pymongo import MongoClient
from flask import jsonify

client = MongoClient("mongo", 27017)
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
    student.student_id = result.inserted_id
    print(student.student_id)
    return str(student.student_id)


def get_by_id(student_id=None):
    student = students_db.find_one({"_id": ObjectId(student_id)})

    if not student:
        return "not found", 404

    student["_id"] = str(student["_id"])

    return student


def delete(student_id=None):
    student = students_db.find_one({"_id": ObjectId(student_id)})

    if not student:
        return "not found", 404

    student["_id"] = str(student["_id"])

    students_db.delete_one({"_id": ObjectId(student_id)})
    return student
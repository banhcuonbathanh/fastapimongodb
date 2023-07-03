from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
import uuid
# todo schema
def todo_serializer(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "name": todo["name"],
        "description": todo["description"],
        "completed": todo["completed"],
        "date": todo["date"],
    }

def todos_serializer(todos) -> list:
    return [todo_serializer(todo) for todo in todos]

# book schema

def book_serializer(document):
    document_dict = {
        **document,
          '_id': str(document['_id'],),
         "title": document["title"],
        "author": document["author"],
        "description": document["description"],
        "stock": document["stock"],
        "sales": document["sales"],
        "id": document["id"],
        }
    return document_dict


# user schema

class PyObject(ObjectId):
    @classmethod
    def __get_Validators__(cls):
        yield cls.__validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError(" Invalid ObjectID")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="Strig")


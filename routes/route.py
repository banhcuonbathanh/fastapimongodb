from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import errors
from models.models import Todo, Book, User, UserResponse
from typing import List
from config.database import collection_name, book_collection, user_collection
from utlis import get_password_hash
from schemas.schema import todos_serializer, todo_serializer, book_serializer
from bson import ObjectId
import secrets



# ---------- todo-----------------------------
todo_api_router = APIRouter()

# retrieve
@todo_api_router.get("/")
async def get_todos():
    print('thiis is get trong todo_api_router')
    todos = todos_serializer(collection_name.find())
    return todos

@todo_api_router.get("/{id}")
async def get_todo(id: str):
    print(f'this is id todo {id}')
    todo = collection_name.find_one({"_id": ObjectId(id)})
    if todo is None:
        return {"error": "No todo found with this id"}
    return todos_serializer(todo)



# post
@todo_api_router.post("/")
async def create_todo(todo: Todo):
    _id = collection_name.insert_one(dict(todo))
    return todos_serializer(collection_name.find({"_id": _id.inserted_id}))


# update
@todo_api_router.put("/{id}")
async def update_todo(id: str, todo: Todo):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(todo)
    })
    return todos_serializer(collection_name.find({"_id": ObjectId(id)}))

# delete
@todo_api_router.delete("/{id}")
async def delete_todo(id: str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "ok"}


# ---------- book -----------------------------


book_api_router = APIRouter()

# retrieve
@book_api_router.get("/books/{book_id}")
async def get_book(book_id: str):
    print('book_id this is book id')
    print(book_id)
    book = book_collection.find_one({"id": book_id})
    if book:
        return {"data": book_serializer(book)}
    else:
        return {"message": "Book not found"}

# get many 

@book_api_router.get("/booksByAuthor/{author}")
async def get_books_by_author(author: str):
    print(" get all by author")
    books = book_collection.find({"author": author})
    if books:
        # Convert cursor object to list
        books_list = list(books)
        # Return serialized data
        return {"data": [book_serializer(book) for book in books_list]}
    else:
        return {"message": "No books found for this author"}

# create


@book_api_router.post("/books")
async def create_book(book: Book):
    try:
        result = book_collection.insert_one(book.dict())
        return {"message": "Book created successfully", "id": str(result.inserted_id)}
    except errors.DuplicateKeyError:
        return {"message": "A book with this id already exists"}

# update

@book_api_router.put("/books/{id}")
async def update_book(id: str, book: Book):

    book_data = book_collection.find_one({"id": id})
    if book_data:
        updated_book_data = book_collection.find_one_and_update({"id": id}, {"$set": book.dict()})
        if updated_book_data:
            return {"data": book_serializer(updated_book_data)}
        else:
            raise HTTPException(status_code=400, detail="Error updating book")
    else:
        raise HTTPException(status_code=404, detail="Book not found")



# delete by id
@book_api_router.delete("/deletebooks/{id}")
async def delete_book(id: str):
    print('this is delete book')
    print(id)
    book_collection.find_one_and_delete({"id": id})
    return {"status": "ok"}

# delete all
@book_api_router.delete("/deleteAllBooks/{title}")
async def delete_all_books(title: str):
    print('this is delete all book')
    book_collection.delete_many({"title": title})
    return {"status": "All books deleted successfully"}
# delete all
@book_api_router.delete("/deleteAll/{collection}")
async def delete_all_books(collection):
    print('this is delete all')
    book_collection.drop()
    return {"status": "All books deleted successfully"}
#-------------------------- registration ---------------------------


resgistration_router = APIRouter()


@resgistration_router.post("/registration", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user( user: User = Body(...)):
    user = jsonable_encoder(user)
    # check dupi=licate

    user_found = await user_collection.find_one({"name": user["name"]})
    # new_book = request.app.database["books"].insert_one(book)
    # created_book = request.app.database["books"].find_one(
    #     {"_id": new_book.inserted_id}
    
    email_found = await user_collection.find_one({"email": user["email"]})

    if user_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='user name exit')
    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='user email exit')
    
    user["password"] = get_password_hash(user["password"])
    user["apiKey"] = secrets.token_hex(30)
    new_user = await user_collection.insert_one(user)
    created_user = user_collection.find_one(
        {"_id": new_user.inserted_id})
    # send email
    return created_user

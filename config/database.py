from pymongo import MongoClient, errors

uri3 = "mongodb+srv://vu:hZDkxNfcN8FQWzX8@cluster0.exj1kwg.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"

client = MongoClient(uri3)


db = client["todo"]

collection_name = db["todos_app"]

book_collection = db["books"]

user_collection = db["users"]
try:
    book_collection.create_index("id", unique=True)
except errors.DuplicateKeyError as e:
    print(e.details)
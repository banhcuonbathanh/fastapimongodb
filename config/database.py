from pymongo import MongoClient

uri3 = "mongodb+srv://vu:hZDkxNfcN8FQWzX8@cluster0.exj1kwg.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"

client = MongoClient(uri3)


db = client["todo"]

collection_name = db["todos_app"]

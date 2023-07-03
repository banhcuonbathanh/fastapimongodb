from fastapi import FastAPI
from routes.route import todo_api_router, book_api_router

import uvicorn
app = FastAPI()

app.include_router(todo_api_router)
app.include_router(book_api_router)
if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=5555)
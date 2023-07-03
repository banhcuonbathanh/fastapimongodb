
from pydantic import BaseModel, Field, EmailStr
import uuid
class Todo(BaseModel):
    name: str
    description: str
    completed: bool
    date: str

# book model
class Book(BaseModel):
    title: str
    author: str
    description: str
    price: float 
    stock: int
    sales: int
    id: str


# user
class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Don Quixote",
                "email": "Miguel de Cervantes",
                "password": "password"
            }
        }
class UserResponse(BaseModel):

    name: str = Field(...)
    email: EmailStr = Field(...)
 
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
  
                "name": "Don Quixote",
              
            }
        }
        
     #

from pydantic import BaseModel, Field

# esquema de usuario para criação e login
class UserCreate(BaseModel):

    username: str
    password: str = Field(..., min_length=4, max_length=50)
    role: str

# esquema de usuario para resposta
class UserLogin(BaseModel):

    username: str
    password: str
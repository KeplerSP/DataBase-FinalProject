from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    name: str
    email: str
    role: str = "user"  # "user" por defecto, "admin" para administradores
    active: bool = True

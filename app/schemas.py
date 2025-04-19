from pydantic import BaseModel
from typing import Optional


class CategoriaSchema(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True


class UsuarioSchema(BaseModel):
    id: int
    nombre: str
    email: str

    class Config:
        orm_mode = True



class NotaBase(BaseModel):
    titulo: str
    contenido: str

class NotaCreate(NotaBase):
    categoria_id: Optional[int] = None
    usuario_id: int

class NotaSchema(NotaBase):
    id: int
    categoria_id: int
    usuario_id: int

    class Config:
        orm_mode = True



from pydantic import BaseModel
from typing import Optional

class NotaBase(BaseModel):
    titulo: str
    contenido: str

class NotaCreate(BaseModel):
    titulo: str
    contenido: str
    categoria_id: Optional[int] = None  # Asegúrate de agregar este campo

class Nota(NotaBase):
    id: int
    usuario_id: int

    class Config:
        orm_mode = True

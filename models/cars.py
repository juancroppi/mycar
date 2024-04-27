from pydantic import BaseModel
from typing import List

class Marca(BaseModel):
    id_marca: int
    nombre: str

class Modelo(BaseModel):
    id_modelo: int
    nombre: str
    id_marca: int
    descripcion: str
    precio: int
    marca: Marca
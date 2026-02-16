import re
from pydantic import BaseModel
from typing import Optional
from pydantic import validator


class Cliente(BaseModel):
    nome: str
    email: str
    telefone: str
    nif: str
    data_nascimento: date

    @validator('nif')
    def validar_nif(cls, v):
        numeros = re.sub(r'\\D', '', v)
        if len(numeros) != 9:
            raise ValueError('Nif deve conter 9 dígitos')
        return numeros

    @validator('telefone')
    def validar_telefone(cls, v):
        #Remove tudo que não é número
        numeros = re.sub(r'\\D', '', v)

        if len(numeros) < 10 or len(numeros) > 11:
            raise ValueError('Telefonone deve ter 10 ou 11 dígitos')

        #Formata: +351 XX XXX XXXX ou 9XX XXX XXX
        if len(numeros) == 9:
            return f"({numeros[:3]}) {numeros[3:6]} {numeros[6:]}"
        elif len(numeros) == 11 and numeros.startswith('351'):
            return f"+{numeros:3} {numeros[3:5]} {numeros[5:8]} {numeros[8:]}"
        else:
            return f"{numeros[:3]} {numeros[3:6]} {numeros[6:]}"

class Veiculo(BaseModel):
    placa: str
    marca: str
    modelo: str
    ano: int
    cor: Optional[str] = None
    cliente_id: int  # ID do dono do veículo
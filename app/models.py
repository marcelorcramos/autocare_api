import re
from pydantic import BaseModel
from typing import Optional
from pydantic import validator
from datetime import date


class Cliente(BaseModel):
    nome: str
    email: str
    telefone: str
    nif: str
    data_nascimento: date

    @validator('nif')
    def validar_nif(cls, v):
        numeros = re.sub(r'\D', '', v)
        if len(numeros) != 9:
            raise ValueError('Nif deve conter 9 dígitos')
        return numeros

    @validator('telefone')
    def validar_telefone(cls, v):
        #Remove tudo que não é número
        numeros = re.sub(r'\D', '', v)

        if len(numeros) < 9 or len(numeros) > 12:
            raise ValueError('Telefonone deve ter entre 9 a 12 dígitos')

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

    @validator('placa')
    def validar_placa(cls, v):
        placa = v.strip().upper()
        
        padrao_com_hifen = r'^[A-Z]{2}-\d{2}-[A-Z]{2}$'
        padrao_sem_hifen = r'^[A-Z]{2}\d{2}[A-Z]{2}$'
        
        if re.match(padrao_com_hifen, placa):
            return placa 
            
        if re.match(padrao_sem_hifen, placa):
            placa_formatada = f"{placa[:2]}-{placa[2:4]}-{placa[4:]}"
            return placa_formatada
        
        raise ValueError('Placa inválida! Formato correto: AA-00-AA')
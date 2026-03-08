"""
Schemas Pydantic para Veiculo — validação de dados de entrada/saída.
"""

import re
from pydantic import BaseModel, validator
from typing import Optional


class VeiculoCreate(BaseModel):
    """Schema para criar/atualizar um veículo"""
    placa: str
    marca: str
    modelo: str
    ano: int
    cor: Optional[str] = None
    cliente_id: int

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


class VeiculoResponse(BaseModel):
    """Schema para retornar um veículo (inclui ID)"""
    id: int
    placa: str
    marca: str
    modelo: str
    ano: int
    cor: Optional[str] = None
    cliente_id: int

    class Config:
        from_attributes = True

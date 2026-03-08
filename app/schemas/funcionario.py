"""
Schemas Pydantic para Funcionario — validação de dados de entrada/saída.
"""

import re
from pydantic import BaseModel, validator
from datetime import date
from typing import Optional


class FuncionarioCreate(BaseModel):
    """Schema para criar/atualizar um funcionário"""
    nome: str
    telefone: str
    nif: str
    morada: Optional[str] = None
    nivel: str
    salario: str
    area: str
    data_nascimento: date

    @validator('nif')
    def validar_nif(cls, v):
        numeros = re.sub(r'\D', '', v)
        if len(numeros) != 9:
            raise ValueError('Nif deve conter 9 dígitos')
        return numeros

    @validator('telefone')
    def validar_telefone(cls, v):
        numeros = re.sub(r'\D', '', v)

        # Se já tem o indicativo 351, remove para validar os 9 dígitos
        if numeros.startswith('351') and len(numeros) == 12:
            numeros = numeros[3:]

        if len(numeros) != 9:
            raise ValueError('Telefone deve ter 9 dígitos (sem indicativo)')

        # Formata sempre no padrão português: +351 XXX XXX XXX
        return f"+351 {numeros[:3]} {numeros[3:6]} {numeros[6:]}"

    @validator('data_nascimento')
    def validar_data_nascimento(cls, v):
        data_atual = date.today()
        idade = data_atual.year - v.year - ((data_atual.month, data_atual.day) < (v.month, v.day))
        if idade < 18:
            raise ValueError('O funcionário deve ter pelo menos 18 anos')
        if v > data_atual:
            raise ValueError('Data de nascimento não pode ser no futuro')
        if idade > 120:
            raise ValueError('Data de nascimento muito antiga')
        return v

    @validator('nivel')
    def validar_nivel(cls, v):
        nivel = v.strip().lower()
        niveis_validos = ['part time', 'part-time', 'full time', 'full-time']
        if nivel not in niveis_validos:
            raise ValueError('Nível deve ser "Part Time" ou "Full Time"')
        if 'part' in nivel:
            return 'Part Time'
        return 'Full Time'

    @validator('salario')
    def validar_salario(cls, v, values):
        numeros = re.sub(r'\D', '', v)
        try:
            salario = float(numeros)
        except ValueError:
            raise ValueError('Salario inválido')
        nivel = values.get('nivel')
        if nivel == 'Full Time' and salario < 920.00:
            raise ValueError('Salário Full Time não pode ser menor que 920€')
        if nivel == 'Part Time' and salario < 460.00:
            raise ValueError('Salário Part Time não pode ser menor que 460€')
        return salario


class FuncionarioResponse(BaseModel):
    """Schema para retornar um funcionário (inclui ID)"""
    id: int
    nome: str
    telefone: str
    nif: str
    morada: Optional[str] = None
    nivel: str
    salario: float
    area: str
    data_nascimento: date

    class Config:
        from_attributes = True

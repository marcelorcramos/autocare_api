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

    @validator('email')
    def validar_email(cls,v):
        email = v.strip()

        if '@' not in email:
            raise ValueError('Email deve conter @')
        
        if '.com' not in email:
            raise ValueError('Email deve conter .com')

        partes = email.split('@')
        if len(partes) != 2:
            raise ValueError ('Email deve conter apenas um @')

        if '.com' not in partes[1]:
            raise ValueError('.com deve vir após o @')

        if not partes[0]:
            raise ValueError ('Email deve ter um nome de usuário')
        
        if not partes[1].replace('.com', ''):
            raise ValueError ('Email deve ter um domínio válido')

        return email.lower()


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

    @validator('data_nascimento')
    def validar_data_nascimento(cls, v):
        data_atual = date.today()
        
        idade = data_atual.year - v.year - ((data_atual.month, data_atual.day) < (v.month, v.day))
        
        if idade < 18:
            raise ValueError('Cliente deve ter pelo menos 18 anos')
        
        if v > data_atual:
            raise ValueError('Data de nascimento não pode ser no futuro')
        
        if idade > 120:
            raise ValueError('Data de nascimento muito antiga')
        
        return v

class Funcionario(BaseModel):
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
        #Remove tudo que não é número
        numeros = re.sub(r'\D', '', v)

        if len(numeros) < 9 or len(numeros) > 12:
            raise ValueError('Telefone deve ter entre 9 a 12 dígitos')

        #Formata: +351 XX XXX XXXX ou 9XX XXX XXX
        if len(numeros) == 9:
            return f"({numeros[:3]}) {numeros[3:6]} {numeros[6:]}"
        elif len(numeros) == 11 and numeros.startswith('351'):
            return f"+{numeros:3} {numeros[3:5]} {numeros[5:8]} {numeros[8:]}"
        else:
            return f"{numeros[:3]} {numeros[3:6]} {numeros[6:]}"

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
            raise ValueError ('Salario inválido')

        nivel = values.get('nivel')

        if nivel == 'Full Time' and salario < 920.00:
            raise ValueError('Salário Full Time não pode ser menor que 920€')
        
        if nivel == 'Part Time' and salario < 460.00:
            raise ValueError('Salário Part Time não pode ser menor que 460€')

        return salario
    

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

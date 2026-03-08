"""
Modelos ORM (SQLAlchemy) — representam as tabelas no banco de dados.

Cada classe aqui vira uma tabela no SQLite.
Os campos (Column) viram colunas da tabela.
Os relacionamentos (relationship) permitem navegar entre tabelas.

NÃO confundir com os modelos Pydantic (app/models.py) que fazem validação.
"""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Cliente(Base):
    """Tabela: clientes"""
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefone = Column(String(20), nullable=False)
    nif = Column(String(9), unique=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)

    # Relacionamento: um cliente pode ter vários veículos
    veiculos = relationship("Veiculo", back_populates="dono")

    def __repr__(self):
        return f"<Cliente(id={self.id}, nome='{self.nome}', nif='{self.nif}')>"


class Funcionario(Base):
    """Tabela: funcionarios"""
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    nif = Column(String(9), unique=True, nullable=False)
    morada = Column(String(200), nullable=True)
    nivel = Column(String(20), nullable=False)       # "Part Time" ou "Full Time"
    salario = Column(Float, nullable=False)
    area = Column(String(50), nullable=False)
    data_nascimento = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Funcionario(id={self.id}, nome='{self.nome}', area='{self.area}')>"


class Veiculo(Base):
    """Tabela: veiculos"""
    __tablename__ = "veiculos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    placa = Column(String(10), unique=True, nullable=False)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    ano = Column(Integer, nullable=False)
    cor = Column(String(30), nullable=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    # Relacionamento: cada veículo pertence a um cliente
    dono = relationship("Cliente", back_populates="veiculos")

    def __repr__(self):
        return f"<Veiculo(id={self.id}, placa='{self.placa}', marca='{self.marca}')>"

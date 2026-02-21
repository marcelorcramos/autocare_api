from fastapi import APIRouter
from app.models import Funcionario
from app.database import funcionarios_db
from typing import Optional
import re

# Criar router específico para clientes
router = APIRouter(prefix="/funcionarios", tags=["Funcionarios"]) 
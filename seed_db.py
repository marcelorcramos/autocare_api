"""
╔══════════════════════════════════════════════════════════════════╗
║                 AutoCare — Script de Banco de Dados             ║
║                                                                  ║
║  Use este script para:                                           ║
║   • Criar as tabelas no SQLite                                   ║
║   • Inserir dados de exemplo (seed)                              ║
║   • Treinar consultas (SELECT, filtros, joins)                   ║
║   • Atualizar e deletar registros                                ║
║                                                                  ║
║  Como executar:                                                  ║
║      python seed_db.py                                           ║
║                                                                  ║
║  O banco é criado no arquivo: autocare.db                        ║
╚══════════════════════════════════════════════════════════════════╝
"""

from datetime import date
from app.database import engine, SessionLocal, Base
from app.db_models import Cliente, Funcionario, Veiculo


# ══════════════════════════════════════════════════════════════════
# 1. CRIAR TABELAS
# ══════════════════════════════════════════════════════════════════

def criar_tabelas():
    """Cria todas as tabelas definidas em db_models.py"""
    print("🔧 Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!\n")


def apagar_tabelas():
    """Apaga todas as tabelas (cuidado! perde todos os dados)"""
    print("🗑️  Apagando todas as tabelas...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tabelas apagadas!\n")


# ══════════════════════════════════════════════════════════════════
# 2. INSERIR DADOS (CREATE)
# ══════════════════════════════════════════════════════════════════

def seed_clientes(db):
    """Insere clientes de exemplo no banco"""
    clientes = [
        Cliente(
            nome="João Silva",
            email="joao.silva@gmail.com",
            telefone="(912) 345 678",
            nif="123456789",
            data_nascimento=date(1990, 5, 15)
        ),
        Cliente(
            nome="Maria Santos",
            email="maria.santos@hotmail.com",
            telefone="(933) 456 789",
            nif="987654321",
            data_nascimento=date(1985, 8, 22)
        ),
        Cliente(
            nome="Pedro Costa",
            email="pedro.costa@gmail.com",
            telefone="(961) 789 012",
            nif="456789123",
            data_nascimento=date(1978, 3, 10)
        ),
        Cliente(
            nome="Ana Oliveira",
            email="ana.oliveira@yahoo.com",
            telefone="(922) 111 222",
            nif="321654987",
            data_nascimento=date(1995, 12, 1)
        ),
        Cliente(
            nome="Carlos Ferreira",
            email="carlos.ferreira@gmail.com",
            telefone="(966) 333 444",
            nif="654987321",
            data_nascimento=date(1982, 7, 25)
        ),
    ]

    db.add_all(clientes)
    db.commit()
    print(f"✅ {len(clientes)} clientes inseridos!")
    return clientes


def seed_funcionarios(db):
    """Insere funcionários de exemplo no banco"""
    funcionarios = [
        Funcionario(
            nome="António Gonçalves",
            telefone="+351 911 111 111",
            nif="111222333",
            morada="Rua das Oficinas, 42, Lisboa",
            nivel="Full Time",
            salario=1200.00,
            area="Mecânico",
            data_nascimento=date(1988, 1, 20)
        ),
        Funcionario(
            nome="Bruno Ferreira",
            telefone="+351 922 222 222",
            nif="444555666",
            morada="Av. da Liberdade, 100, Porto",
            nivel="Full Time",
            salario=1350.00,
            area="Electricista",
            data_nascimento=date(1992, 6, 14)
        ),
        Funcionario(
            nome="Carla Mendes",
            telefone="+351 933 333 333",
            nif="777888999",
            morada=None,
            nivel="Part Time",
            salario=600.00,
            area="Recepção",
            data_nascimento=date(2000, 9, 5)
        ),
        Funcionario(
            nome="Daniel Sousa",
            telefone="+351 944 444 444",
            nif="112233445",
            morada="Rua do Comercio, 7, Braga",
            nivel="Full Time",
            salario=1100.00,
            area="Pintura e Chapa",
            data_nascimento=date(1985, 11, 30)
        ),
    ]

    db.add_all(funcionarios)
    db.commit()
    print(f"✅ {len(funcionarios)} funcionários inseridos!")
    return funcionarios


def seed_veiculos(db):
    """Insere veículos de exemplo (associados aos clientes já criados)"""
    veiculos = [
        Veiculo(
            placa="AA-11-BB",
            marca="Volkswagen",
            modelo="Golf",
            ano=2019,
            cor="Preto",
            cliente_id=1  # João Silva
        ),
        Veiculo(
            placa="CC-22-DD",
            marca="Renault",
            modelo="Clio",
            ano=2021,
            cor="Branco",
            cliente_id=2  # Maria Santos
        ),
        Veiculo(
            placa="EE-33-FF",
            marca="BMW",
            modelo="Série 3",
            ano=2018,
            cor="Azul",
            cliente_id=1  # João Silva (2º veículo)
        ),
        Veiculo(
            placa="GG-44-HH",
            marca="Mercedes",
            modelo="Classe A",
            ano=2022,
            cor="Cinza",
            cliente_id=3  # Pedro Costa
        ),
        Veiculo(
            placa="II-55-JJ",
            marca="Peugeot",
            modelo="208",
            ano=2020,
            cor="Vermelho",
            cliente_id=4  # Ana Oliveira
        ),
        Veiculo(
            placa="KK-66-LL",
            marca="Toyota",
            modelo="Yaris",
            ano=2023,
            cor=None,
            cliente_id=5  # Carlos Ferreira
        ),
    ]

    db.add_all(veiculos)
    db.commit()
    print(f"✅ {len(veiculos)} veículos inseridos!")
    return veiculos


# ══════════════════════════════════════════════════════════════════
# 3. CONSULTAR DADOS (READ)
# ══════════════════════════════════════════════════════════════════

def listar_todos_clientes(db):
    """Busca todos os clientes"""
    print("\n📋 TODOS OS CLIENTES:")
    print("-" * 60)
    clientes = db.query(Cliente).all()
    for c in clientes:
        print(f"  ID: {c.id} | {c.nome} | NIF: {c.nif} | Email: {c.email}")
    print(f"\nTotal: {len(clientes)} clientes\n")
    return clientes


def buscar_cliente_por_id(db, cliente_id: int):
    """Busca um cliente por ID"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        print(f"\n🔍 Cliente encontrado: {cliente.nome} (NIF: {cliente.nif})")
    else:
        print(f"\n❌ Cliente ID {cliente_id} não encontrado!")
    return cliente


def buscar_cliente_por_nome(db, nome: str):
    """Busca clientes por nome (parcial, case-insensitive)"""
    clientes = db.query(Cliente).filter(Cliente.nome.ilike(f"%{nome}%")).all()
    print(f"\n🔍 Clientes com nome '{nome}':")
    for c in clientes:
        print(f"  ID: {c.id} | {c.nome}")
    return clientes


def listar_veiculos_do_cliente(db, cliente_id: int):
    """Lista todos os veículos de um cliente (usando relacionamento)"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        print(f"\n❌ Cliente ID {cliente_id} não encontrado!")
        return []

    print(f"\n🚗 Veículos de {cliente.nome}:")
    print("-" * 60)
    for v in cliente.veiculos:  # usa o relacionamento definido no modelo!
        print(f"  {v.placa} | {v.marca} {v.modelo} ({v.ano}) | Cor: {v.cor or 'N/A'}")
    print(f"\nTotal: {len(cliente.veiculos)} veículos\n")
    return cliente.veiculos


def listar_todos_funcionarios(db):
    """Busca todos os funcionários"""
    print("\n👷 TODOS OS FUNCIONÁRIOS:")
    print("-" * 60)
    funcionarios = db.query(Funcionario).all()
    for f in funcionarios:
        print(f"  ID: {f.id} | {f.nome} | {f.area} | {f.nivel} | €{f.salario:.2f}")
    print(f"\nTotal: {len(funcionarios)} funcionários\n")
    return funcionarios


def listar_todos_veiculos(db):
    """Busca todos os veículos com info do dono"""
    print("\n🚗 TODOS OS VEÍCULOS:")
    print("-" * 60)
    veiculos = db.query(Veiculo).all()
    for v in veiculos:
        dono_nome = v.dono.nome if v.dono else "Sem dono"
        print(f"  ID: {v.id} | {v.placa} | {v.marca} {v.modelo} ({v.ano}) | Dono: {dono_nome}")
    print(f"\nTotal: {len(veiculos)} veículos\n")
    return veiculos


# ══════════════════════════════════════════════════════════════════
# 4. ATUALIZAR DADOS (UPDATE)
# ══════════════════════════════════════════════════════════════════

def atualizar_email_cliente(db, cliente_id: int, novo_email: str):
    """Atualiza o email de um cliente"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        email_antigo = cliente.email
        cliente.email = novo_email
        db.commit()
        print(f"\n✏️  Email atualizado: '{email_antigo}' → '{novo_email}'")
    else:
        print(f"\n❌ Cliente ID {cliente_id} não encontrado!")
    return cliente


def atualizar_salario_funcionario(db, funcionario_id: int, novo_salario: float):
    """Atualiza o salário de um funcionário"""
    funcionario = db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
    if funcionario:
        salario_antigo = funcionario.salario
        funcionario.salario = novo_salario
        db.commit()
        print(f"\n✏️  Salário de {funcionario.nome}: €{salario_antigo:.2f} → €{novo_salario:.2f}")
    else:
        print(f"\n❌ Funcionário ID {funcionario_id} não encontrado!")
    return funcionario


# ══════════════════════════════════════════════════════════════════
# 5. DELETAR DADOS (DELETE)
# ══════════════════════════════════════════════════════════════════

def deletar_cliente(db, cliente_id: int):
    """Remove um cliente (atenção: pode falhar se tiver veículos associados)"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        nome = cliente.nome
        db.delete(cliente)
        db.commit()
        print(f"\n🗑️  Cliente '{nome}' (ID: {cliente_id}) removido!")
    else:
        print(f"\n❌ Cliente ID {cliente_id} não encontrado!")


def deletar_veiculo(db, veiculo_id: int):
    """Remove um veículo"""
    veiculo = db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
    if veiculo:
        placa = veiculo.placa
        db.delete(veiculo)
        db.commit()
        print(f"\n🗑️  Veículo '{placa}' (ID: {veiculo_id}) removido!")
    else:
        print(f"\n❌ Veículo ID {veiculo_id} não encontrado!")


# ══════════════════════════════════════════════════════════════════
# 6. CONSULTAS AVANÇADAS (para treinar!)
# ══════════════════════════════════════════════════════════════════

def funcionarios_full_time(db):
    """Filtra apenas funcionários Full Time"""
    resultado = db.query(Funcionario).filter(Funcionario.nivel == "Full Time").all()
    print("\n👷 Funcionários Full Time:")
    for f in resultado:
        print(f"  {f.nome} | {f.area} | €{f.salario:.2f}")
    return resultado


def veiculos_por_marca(db, marca: str):
    """Filtra veículos por marca"""
    resultado = db.query(Veiculo).filter(Veiculo.marca.ilike(f"%{marca}%")).all()
    print(f"\n🚗 Veículos da marca '{marca}':")
    for v in resultado:
        print(f"  {v.placa} | {v.marca} {v.modelo} ({v.ano})")
    return resultado


def clientes_ordenados_por_nome(db):
    """Lista clientes em ordem alfabética"""
    resultado = db.query(Cliente).order_by(Cliente.nome).all()
    print("\n📋 Clientes (A-Z):")
    for c in resultado:
        print(f"  {c.nome}")
    return resultado


def contar_veiculos_por_cliente(db):
    """Conta quantos veículos cada cliente tem"""
    from sqlalchemy import func
    resultado = (
        db.query(Cliente.nome, func.count(Veiculo.id).label("total_veiculos"))
        .join(Veiculo, Cliente.id == Veiculo.cliente_id)
        .group_by(Cliente.nome)
        .all()
    )
    print("\n📊 Veículos por cliente:")
    for nome, total in resultado:
        print(f"  {nome}: {total} veículo(s)")
    return resultado


# ══════════════════════════════════════════════════════════════════
# EXECUÇÃO PRINCIPAL
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("   AutoCare — Configuração do Banco de Dados")
    print("=" * 60)

    # Passo 1: Recriar tabelas (limpa tudo e começa do zero)
    apagar_tabelas()
    criar_tabelas()

    # Passo 2: Abrir sessão com o banco
    db = SessionLocal()

    try:
        # Passo 3: Popular com dados de exemplo
        print("\n📦 Inserindo dados de exemplo...")
        print("-" * 60)
        seed_clientes(db)
        seed_funcionarios(db)
        seed_veiculos(db)

        # Passo 4: Testar consultas
        print("\n" + "=" * 60)
        print("   Testando Consultas")
        print("=" * 60)

        listar_todos_clientes(db)
        listar_todos_funcionarios(db)
        listar_todos_veiculos(db)

        # Testar relacionamento
        listar_veiculos_do_cliente(db, 1)  # veículos do João

        # Testar busca
        buscar_cliente_por_nome(db, "Maria")

        # Testar consultas avançadas
        funcionarios_full_time(db)
        contar_veiculos_por_cliente(db)

        # Testar update
        atualizar_email_cliente(db, 1, "joao.novo@gmail.com")

        print("\n" + "=" * 60)
        print("   ✅ Banco de dados configurado com sucesso!")
        print("   📁 Arquivo: autocare.db")
        print("=" * 60)

    finally:
        db.close()

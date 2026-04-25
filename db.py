import sqlite3
from pathlib import Path
import pandas as pd

# Define a raiz do projeto dinamicamente
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "database" / "banco.db"
SCHEMA_PATH = BASE_DIR / "schemas" / "schema.sql"

def conectar():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_bd():
    if not SCHEMA_PATH.exists():
        print(f"[ERRO] Arquivo schema.sql não encontrado em: {SCHEMA_PATH}")
        return
    
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with conectar() as conn:
        conn.executescript(sql)

def criar_user(nome, email, serie, turma):
    with conectar() as conn:
        conn.execute(
            """
            INSERT INTO aluno (nome, email, serie, turma)
            VALUES (?, ?, ?, ?)
            """,
            (nome, email, serie, turma)
        )

def listar_alunos():
    with conectar() as conn:
        cursor = conn.execute(
            "SELECT matricula, nome, email, serie, turma FROM aluno ORDER BY serie, turma, matricula"
        )
        return cursor.fetchall()

def exportar_df(colunas=None, serie=None, turma=None):
    query = "SELECT matricula, nome, email, serie, turma FROM aluno"
    params = []
    filtros = []

    if serie is not None:
        filtros.append("serie = ?")
        params.append(serie)

    if turma is not None:
        filtros.append("turma = ?")
        params.append(turma)

    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    query += " ORDER BY serie, turma, matricula"

    with conectar() as conn:
        df = pd.read_sql_query(query, conn, params=params)

    if colunas:
        df = df[colunas]

    return df
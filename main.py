from db import criar_user, init_bd, listar_alunos, exportar_df
from datetime import datetime
from pathlib import Path
import pandas as pd
import unicodedata

# Inicializa o banco ao rodar o script
init_bd()
ano_atual = datetime.now().year
BASE_DIR = Path(__file__).parent

def tirar_acentos(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

def criar_email(nome: str) -> str:
    partes = nome.lower().split()
    if len(partes) < 2:
        primeiro = tirar_acentos(partes[0])
        return f"{primeiro}.aluno.{ano_atual}@etepd.com"
    
    primeiro = tirar_acentos(partes[0])
    ultimo = tirar_acentos(partes[-1])
    return f"{primeiro}.{ultimo}.{ano_atual}@etepd.com"

def cadastrar_turma():
    try:
        serie_input = int(input("Qual série? (1, 2 ou 3): ").strip())
        turma_input = input("Qual turma? (A, B ou C): ").strip().upper()
    except ValueError:
        print("Entrada inválida. Use números para a série.")
        return

    # Procura o arquivo na pasta 'sheets' dentro do projeto
    nome_arquivo = f"ENTURMAÇÃO - {serie_input} anos.xlsx"
    caminho_arquivo = BASE_DIR / "sheets" / nome_arquivo

    if not caminho_arquivo.exists():
        print(f"\n[ERRO] Arquivo não encontrado: {caminho_arquivo}")
        print("Certifique-se de que o arquivo está na pasta 'sheets' com o nome correto.")
        return

    # LÊ A PLANILHA (Agora de forma simples, sem pular linhas)
    try:
        # Tenta ler a aba com o nome da turma (ex: 1A)
        sheet_nome = f"{serie_input}{turma_input}"
        df = pd.read_excel(caminho_arquivo, sheet_name=sheet_nome)
    except Exception:
        # Se não achar a aba específica, tenta ler a primeira aba do arquivo
        print(f"Aba '{sheet_nome}' não encontrada. Lendo a primeira aba disponível...")
        df = pd.read_excel(caminho_arquivo)

    # Padroniza nomes das colunas (tira espaços e deixa maiúsculo)
    df.columns = [str(c).strip().upper() for c in df.columns]

    if 'NOME' not in df.columns:
        print("[ERRO] A coluna 'NOME' não foi encontrada na planilha.")
        return

    df = df.dropna(subset=['NOME'])
    
    cadastrados = 0
    falhas = 0

    print(f"\nImportando alunos para {serie_input}º {turma_input}...")
    
    for _, linha in df.iterrows():
        nome_original = str(linha['NOME']).strip()
        email = criar_email(nome_original)

        try:
            criar_user(nome_original, email, serie_input, turma_input)
            cadastrados += 1
        except Exception as e:
            falhas += 1
            print(f"  - Falha ao cadastrar {nome_original}: {e}")
    
    print(f"\nConcluído!")
    print(f"Sucesso: {cadastrados} | Falhas: {falhas}")

# As funções listar_menu, exportar_menu e main permanecem as mesmas logicamente, 
# apenas garanta que as pastas de exportação usem BASE_DIR / "exports"
def exportar_menu():
    print("\n1 - Exportar tudo")
    print("2 - Exportar só emails")
    opc = input("Escolha uma opção: ").strip()
    
    exports_dir = BASE_DIR / "exports"
    exports_dir.mkdir(exist_ok=True)
    
    df = exportar_df() # Exemplo simplificado
    caminho = exports_dir / "alunos_exportados.xlsx"
    df.to_excel(caminho, index=False)
    print(f"Exportado para: {caminho}")

def main():
    while True:
        print("\n--- SISTEMA ETEPD ---")
        print("1 - Cadastrar turma (via Excel)")
        print("2 - Listar alunos")
        print("3 - Exportar planilha")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1": cadastrar_turma()
        elif opcao == "2": 
            for a in listar_alunos(): print(a)
        elif opcao == "3": exportar_menu()
        elif opcao == "0": break
        else: print("Opção inválida.")

if __name__ == "__main__":
    main()
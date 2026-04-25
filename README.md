# AutoEmail ETEPD: Automação de Cadastros e E-mails Institucionais

## Sobre o Projeto
O AutoEmail ETEPD é uma ferramenta desenvolvida para solucionar um gargalo operacional crítico na secretaria escolar: o processamento manual de dados de novos alunos para a criação de contas institucionais. 

## Contexto e Impacto Real
Este projeto foi desenvolvido para resolver uma necessidade **real** da coordenação escolar: a geração em massa de e-mails institucionais para novos alunos. O sistema não é apenas um exercício de lógica; ele foi efetivamente implementado e utilizado para processar os dados e gerar as contas de todas as turmas ingressantes de 2026.

## O Problema
Antes da automação, a criação desses e-mails era um processo manual exaustivo. Com uma média de três turmas por série e 45 alunos por turma, a secretaria precisava processar centenas de nomes individualmente. Esse trabalho repetitivo levava tardes inteiras e era extremamente vulnerável a erros de digitação e duplicidade de dados.

A Solução em Produção
Com este script, o tempo de processamento dos dados de 2026 foi reduzido para poucos segundos. A automação garantiu que todos os alunos fossem cadastrados com e-mails padronizados, tratando automaticamente acentos e caracteres especiais, eliminando o erro humano e garantindo a integridade do banco de dados desde o primeiro dia de aulas.

É por isso qie este software automatiza todo o fluxo de ETL (Extração, Transformação e Carga), transformando o que levava horas de trabalho manual em uma execução de poucos segundos.

## Funcionalidades
- **Extração Automática:** Leitura de arquivos Excel (.xlsx) complexos.
- **Transformação de Dados:** Tratamento de nomes (remoção de acentos e caracteres especiais) e geração automática de e-mails no padrão `nome.sobrenome.ano@etepd.com`.
- **Persistência Relacional:** Armazenamento em banco de dados SQLite para garantir que cada matrícula seja única e consultável.
- **Exportação Estruturada:** Geração de novas planilhas com os dados processados para fácil importação em outros sistemas administrativos.

## Tecnologias Utilizadas
- **Python 3.10+**
- **Pandas:** Para manipulação e análise de dados.
- **SQLite3:** Para armazenamento e integridade referencial.
- **OpenPyXL:** Para suporte a leitura e escrita de arquivos Excel.
- **Pathlib:** Para gestão de caminhos de arquivos de forma independente de sistema operacional.

## Regras de Nomenclatura e Estrutura (Pasta /sheets)
O funcionamento do sistema depende da organização rigorosa dos arquivos de entrada. O código foi programado para localizar os arquivos na pasta `sheets/` seguindo um padrão fixo. 

**Nomes Obrigatórios dos Arquivos:**
- Para o 1º ano: `ENTURMAÇÃO - 1 anos.xlsx`
- Para o 2º ano: `ENTURMAÇÃO - 2 anos.xlsx`
- Para o 3º ano: `ENTURMAÇÃO - 3 anos.xlsx`

**Atenção:** Caso o usuário deseje alterar o nome dos arquivos físicos, será necessário realizar a alteração correspondente no código-fonte (`main.py`), pois o script busca exatamente essas cadeias de caracteres para montar o caminho de leitura.

**Padrão da Planilha:**
- O sistema espera encontrar as colunas **MATRICULA** e **NOME** na primeira linha da aba (sheet) correspondente.
- O nome da aba dentro do Excel deve ser a combinação da série e turma (ex: `1A`, `2B`, `3C`).

## Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone https://github.com/dev-KauhanMelo/School-Email-Generator
cd CRIADOR-DE-EMAILS
```

### 2. Instalar Dependências
O projeto utiliza um arquivo `requirements.txt` para garantir que todas as bibliotecas necessárias sejam instaladas nas versões corretas.
```bash
pip install -r requirements.txt
```

### 3. Execução
Para iniciar o gerenciador, execute:
```bash
python main.py
```

## Estrutura do Repositório
- `main.py`: Interface de linha de comando e lógica principal de fluxo.
- `db.py`: Funções de conexão, criação de tabelas e persistência no SQLite.
- `schemas/`: Contém o `schema.sql` para inicialização do banco de dados.
- `sheets/`: Pasta destinada aos arquivos Excel de entrada.
- `exports/`: Pasta onde os resultados processados são salvos.
- `database/`: Local onde o arquivo `banco.db` é mantido.

## Nota sobre Privacidade e LGPD
Este repositório contém apenas dados fictícios gerados para demonstração técnica. O arquivo `.gitignore` está configurado para não versionar o banco de dados real nem as planilhas contendo informações sensíveis de alunos, garantindo a conformidade com as boas práticas de proteção de dados.

---
*Este projeto é uma solução de backend focada em eficiência operacional e integridade de dados no ambiente escolar.*

# Hive 
instruções para instalação, configuração e execução da aplicação Hive, além dos scripts para criação e povoamento do banco de dados.

##Índice

Pré-requisitos

Instalação

Configuração do Banco de Dados

Scripts de Banco de Dados

Variáveis de Ambiente

Execução da Aplicação

Execução de Testes

Estrutura do Projeto

Pré-requisitos

Python 3.8+

PostgreSQL 12+

Git

#Instalação

1.Clone o repositório:
git clone https://github.com/seu-usuario/hive.git
cd hive
2. Crie e ative um ambiente virtual:
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
3.Instale as dependências:
pip install -r requirements.txt
Configuração do Banco de Dados
1.Crie o banco de dados no PostgreSQL:
2.Atualize as credenciais no arquivo .env (veja Variáveis de Ambiente).
Scripts de Banco de Dados

schema.sql: contém os comandos para criar as tabelas principais:

usuário

desenvolvedora

jogo

biblioteca_jogo

compra

item_compra

biblioteca

avaliação

# Execução da Aplicação

Com o ambiente virtual ativo e o banco configurado, execute: python app.python

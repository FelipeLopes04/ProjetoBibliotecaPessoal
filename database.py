"""Conexão com o banco de dados SQL Server (o banco é criado pelo script sql/criar_banco.sql)."""
import pyodbc

CONEXAO = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=localhost\SQLEXPRESS;"
    "DATABASE=BibliotecaPessoal;"
    "Trusted_Connection=yes;"
)


def conectar():
    """Abre uma conexão com o banco. As linhas permitem acessar as colunas pelo nome (livro.titulo)."""
    return pyodbc.connect(CONEXAO)

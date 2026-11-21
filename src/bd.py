import sqlite3

CAMINHO_BD = "libmanager.db"


def ligar():
    ligacao = sqlite3.connect(CAMINHO_BD)
    ligacao.row_factory = sqlite3.Row
    ligacao.execute("PRAGMA foreign_keys = ON")
    return ligacao


def criar_tabelas():
    ligacao = ligar()
    ligacao.executescript("""
        CREATE TABLE IF NOT EXISTS livros (
            isbn TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INTEGER,
            exemplares INTEGER NOT NULL 
                CHECK (exemplares >= 0)
        );
        CREATE TABLE IF NOT EXISTS socios (
            numero INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            contacto TEXT,
            palavra_passe TEXT NOT NULL,
            limite_livros INTEGER NOT NULL DEFAULT 3
        );
        CREATE TABLE IF NOT EXISTS bibliotecarios (
            numero INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            palavra_passe TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL REFERENCES livros (isbn),
            socio INTEGER NOT NULL REFERENCES socios (numero),
            data_emprestimo TEXT NOT NULL,
            data_prevista TEXT NOT NULL,
            data_devolucao TEXT,
            estado TEXT NOT NULL DEFAULT 'ativo'
                CHECK (estado IN ('ativo', 'devolvido', 'cancelado'))
        );
        CREATE TABLE IF NOT EXISTS pedidos_renovacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emprestimo INTEGER NOT NULL REFERENCES emprestimos (id),
            data_pedido TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'pendente'
                CHECK (estado IN ('pendente', 'aprovado', 'recusado'))
        );
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL REFERENCES livros (isbn),
            socio INTEGER NOT NULL REFERENCES socios (numero),
            data TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS multas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emprestimo INTEGER NOT NULL REFERENCES emprestimos (id),
            socio INTEGER NOT NULL REFERENCES socios (numero),
            valor REAL NOT NULL,
            paga INTEGER NOT NULL DEFAULT 0
        );
    """)
    ligacao.commit()
    ligacao.close()
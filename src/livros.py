from src.bd import ligar
from src.utils import pedir_texto, pedir_inteiro, mostrar_erro

def procurar_livro(isbn):
    ligacao = ligar()
    livro = ligacao.execute(
        "SELECT * FROM livros WHERE isbn = ?", (isbn,)
    ).fetchone()
    ligacao.close()
    return livro

def adicionar_livro():
    isbn = pedir_texto("ISBN: ")
    if procurar_livro(isbn) is not None:
        mostrar_erro("Já existe um livro com esse ISBN.")
        return
    titulo = pedir_texto("Título: ")
    autor = pedir_texto("Autor: ")
    genero = pedir_texto("Género: ")
    ano = pedir_inteiro("Ano: ")
    exemplares = pedir_inteiro("Exemplares: ")
    ligacao = ligar()
    ligacao.execute(
        "INSERT INTO livros (isbn, titulo, autor, genero, ano, exemplares) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (isbn, titulo, autor, genero, ano, exemplares)
    )
    ligacao.commit()
    ligacao.close()
    print("Livro adicionado com sucesso.")



# Gestão dos livros.

def menu_livros():
# Mostra o menu de livros do bibliotecário (ainda por implementar).
    print("Em desenvolvimento.")


def menu_pesquisa():
# Mostra o menu de pesquisa de livros do sócio (ainda por implementar).
    print("Em desenvolvimento.")
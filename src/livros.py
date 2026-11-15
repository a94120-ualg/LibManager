from src.bd import ligar
from src.utils import pedir_texto, pedir_texto_ou_manter , pedir_inteiro, mostrar_erro

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

def exemplares_disponiveis(isbn):
    ligacao = ligar()
    consulta = (
        "SELECT l.exemplares - COUNT(e.id) AS disponiveis "
        "FROM livros l LEFT JOIN emprestimos e "
        "ON e.isbn = l.isbn AND e.estado = 'ativo' "
        "WHERE l.isbn = ? GROUP BY l.isbn"
    )
    linha = ligacao.execute(consulta, (isbn,)).fetchone()
    ligacao.close()
    if linha is None:
        return 0
    return linha["disponiveis"]

def mostrar_livros(livros):
    if len(livros) == 0:
        print("Nenhum livro encontrado.")
        return
    print(f"{'ISBN':<16}{'Título':<26}{'Autor':<22}{'Género':<12}Disponíveis")
    for livro in livros:
        disponiveis = exemplares_disponiveis(livro["isbn"])
        print(f"{livro['isbn']:<16}{livro['titulo']:<26}"
              f"{livro['autor']:<22}{livro['genero']:<12}{disponiveis}")


def listar_livros():
    ligacao = ligar()
    livros = ligacao.execute("SELECT * FROM livros ORDER BY titulo").fetchall()
    ligacao.close()
    mostrar_livros(livros)

def editar_livro():
    isbn = pedir_texto("ISBN do livro a editar: ")
    livro = procurar_livro(isbn)
    if livro is None:
        mostrar_erro("Livro não encontrado.")
        return
    titulo = pedir_texto_ou_manter("Título", livro["titulo"])
    autor = pedir_texto_ou_manter("Autor", livro["autor"])
    genero = pedir_texto_ou_manter("Género", livro["genero"])
    ano = pedir_inteiro("Ano (atual " + str(livro["ano"]) + "): ")
    exemplares = pedir_inteiro(
        "Exemplares (atual " + str(livro["exemplares"]) + "): "
    )
    ligacao = ligar()
    ligacao.execute(
        "UPDATE livros SET titulo = ?, autor = ?, genero = ?, ano = ?, "
        "exemplares = ? WHERE isbn = ?",
        (titulo, autor, genero, ano, exemplares, isbn)
    )
    ligacao.commit()
    ligacao.close()
    print("Livro atualizado.")

    
# Gestão dos livros.

def menu_livros():
# Mostra o menu de livros do bibliotecário (ainda por implementar).
    print("Em desenvolvimento.")


def menu_pesquisa():
# Mostra o menu de pesquisa de livros do sócio (ainda por implementar).
    print("Em desenvolvimento.")
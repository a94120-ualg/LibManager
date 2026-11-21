from src.bd import ligar
from src.utils import pedir_texto, pedir_texto_ou_manter , pedir_inteiro, mostrar_erro
import sqlite3
from src.utils import confirmar

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



def remover_livro():
    isbn = pedir_texto("ISBN do livro a remover: ")
    livro = procurar_livro(isbn)
    if livro is None:
        mostrar_erro("Livro não encontrado.")
        return
    if not confirmar('Remover "' + livro["titulo"] + '"?'):
        return
    ligacao = ligar()
    try:
        ligacao.execute("DELETE FROM livros WHERE isbn = ?", (isbn,))
        ligacao.commit()
        print("Livro removido.")
    except sqlite3.IntegrityError:
        mostrar_erro("O livro tem empréstimos ou reservas e não pode ser removido.")
    ligacao.close()

def pesquisar_por_titulo():
    texto = pedir_texto("Título: ")
    ligacao = ligar()
    livros = ligacao.execute(
        "SELECT * FROM livros WHERE titulo LIKE ? ORDER BY titulo",
        ("%" + texto + "%",)
    ).fetchall()
    ligacao.close()
    mostrar_livros(livros)

def pesquisar_por_autor():
    texto = pedir_texto("Autor: ")
    ligacao = ligar()
    livros = ligacao.execute(
        "SELECT * FROM livros WHERE autor LIKE ? ORDER BY titulo",
        ("%" + texto + "%",)
    ).fetchall()
    ligacao.close()
    mostrar_livros(livros)


def filtrar_por_genero():
    texto = pedir_texto("Género: ")
    ligacao = ligar()
    livros = ligacao.execute(
        "SELECT * FROM livros WHERE genero LIKE ? ORDER BY titulo",
        ("%" + texto + "%",)
    ).fetchall()
    ligacao.close()
    mostrar_livros(livros)



# Gestão dos livros.

def menu_livros():
    opcao = -1
    while opcao != 0:
        print("\n=== Livros ===")
        print("1. Adicionar")
        print("2. Editar")
        print("3. Remover")
        print("4. Listar")
        print("5. Ver histórico")
        print("0. Voltar")
        opcao = pedir_inteiro("Opção: ")
        if opcao == 1:
            adicionar_livro()
        elif opcao == 2:
            editar_livro()
        elif opcao == 3:
            remover_livro()
        elif opcao == 4:
            listar_livros()
        elif opcao == 5:
            ver_historico_livro()
        elif opcao != 0:
            mostrar_erro("Opção inválida.")

def menu_pesquisa():
    opcao = -1
    while opcao != 0:
        print("\n=== Pesquisar livros ===")
        print("1. Por título")
        print("2. Por autor")
        print("3. Por género")
        print("0. Voltar")
        opcao = pedir_inteiro("Opção: ")
        if opcao == 1:
            pesquisar_por_titulo()
        elif opcao == 2:
            pesquisar_por_autor()
        elif opcao == 3:
            filtrar_por_genero()
        elif opcao != 0:
            mostrar_erro("Opção inválida.")



def ver_historico_livro():
    isbn = pedir_texto("ISBN do livro: ")
    livro = procurar_livro(isbn)
    if livro is None:
        mostrar_erro("livro não encontrado.")
        return
    ligacao = ligar()
    consulta = (
        "SELECT s.nome, e.data_emprestimo, e.data_devolucao, e.estado "
        "FROM emprestimos e JOIN socios s ON s.numero = e.socio "
        "WHERE e.isbn = ? ORDER BY e.data_emprestimo DESC"
    )
    historico = ligacao.execute(consulta, (isbn,)).fetchall()
    ligacao.close()
    if len(historico) == 0:
        print("Este livro ainda não tem empréstimos.")
        return
    print('Histórico de "' + livro["titulo"] + '":')
    for registo in historico:
        devolucao = registo["data_devolucao"]
        if devolucao is None:
            devolucao = "em curso"
        print(f"{registo['nome']:<20}{registo['data_emprestimo']} - "
              f"{devolucao} ({registo['estado']})")	



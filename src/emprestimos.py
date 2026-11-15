# Gestão de empréstimos e pedidos de renovação.
from src.base_dados import ligar

PRAZO_DIAS = 14

def contar_emprestimos_ativos(numero):
    ligacao = ligar()
    linha = ligacao.execute(
        "SELECT COUNT(*) AS total FROM emprestimos "
        "WHERE socio = ? AND estado = 'ativo'", (numero,)
    ).fetchone()
    ligacao.close()
    return linha["total"]


from src import livros, socios
from src.base_dados import ligar
from src.utils import pedir_texto, pedir_inteiro, hoje, somar_dias, mostrar_erro


def registar_emprestimo():
    numero = pedir_inteiro("Nº de sócio: ")
    socio = socios.procurar_socio(numero)
    if socio is None:
        mostrar_erro("Sócio não encontrado.")
        return
    isbn = pedir_texto("ISBN: ")
    if livros.procurar_livro(isbn) is None:
        mostrar_erro("Livro não encontrado.")
        return
    if livros.exemplares_disponiveis(isbn) == 0:
        mostrar_erro("Não há exemplares disponíveis.")
        return
    if contar_emprestimos_ativos(numero) >= socio["limite_livros"]:
        mostrar_erro("O sócio atingiu o limite de livros.")
        return
    data_emprestimo = hoje()
    data_prevista = somar_dias(data_emprestimo, PRAZO_DIAS)
    ligacao = ligar()
    ligacao.execute(
        "INSERT INTO emprestimos (isbn, socio, data_emprestimo, data_prevista) "
        "VALUES (?, ?, ?, ?)", (isbn, numero, data_emprestimo, data_prevista)
    )
    ligacao.commit()
    ligacao.close()
    print("Empréstimo registado. Devolução até " + data_prevista + ".")



def procurar_emprestimo_ativo(isbn, numero):
    ligacao = ligar()
    emprestimo = ligacao.execute(
        "SELECT * FROM emprestimos "
        "WHERE isbn = ? AND socio = ? AND estado = 'ativo'", (isbn, numero)
    ).fetchone()
    ligacao.close()
    return emprestimo


def registar_devolucao():
    isbn = pedir_texto("ISBN: ")
    numero = pedir_inteiro("Nº de sócio: ")
    emprestimo = procurar_emprestimo_ativo(isbn, numero)
    if emprestimo is None:
        mostrar_erro("Não existe um empréstimo ativo desse livro para esse sócio.")
        return
    ligacao = ligar()
    ligacao.execute(
        "UPDATE emprestimos SET estado = 'devolvido', data_devolucao = ? "
        "WHERE id = ?", (hoje(), emprestimo["id"])
    )
    ligacao.commit()
    ligacao.close()
    print("Devolução registada. O livro está novamente disponível.")

    
def menu_emprestimos():
# Mostra o menu de empréstimos do bibliotecário (ainda por implementar).
    print("Em desenvolvimento.")


def listar_emprestimos_ativos(numero):
# Lista os empréstimos ativos de um sócio (ainda por implementar).
    print("Em desenvolvimento.")


def pedir_renovacao(numero):
# Regista um pedido de renovação de um sócio (ainda por implementar).
    print("Em desenvolvimento.")


def ver_pedidos_socio(numero):
# Mostra o estado dos pedidos de renovação de um sócio (ainda por implementar).
    print("Em desenvolvimento.")
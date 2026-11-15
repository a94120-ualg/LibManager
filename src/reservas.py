from src import livros
from src.bd import ligar
from src.utils import pedir_texto, hoje, mostrar_erro


def reservar_livro(numero):
    isbn = pedir_texto("ISBN: ")
    if livros.procurar_livro(isbn) is None:
        mostrar_erro("Livro não encontrado.")
        return
    if livros.exemplares_disponiveis(isbn) > 0:
        mostrar_erro("O livro está disponível. Peça o empréstimo ao bibliotecário.")
        return
    ligacao = ligar()
    existente = ligacao.execute(
        "SELECT id FROM reservas WHERE isbn = ? AND socio = ?", (isbn, numero)
    ).fetchone()
    if existente is not None:
        ligacao.close()
        mostrar_erro("Já tem uma reserva deste livro.")
        return
    ligacao.execute(
        "INSERT INTO reservas (isbn, socio, data) VALUES (?, ?, ?)",
        (isbn, numero, hoje())
    )
    ligacao.commit()
    ligacao.close()
    print("Livro reservado.")

def cancelar_reserva(numero):
    isbn = pedir_texto("ISBN: ")
    ligacao = ligar()
    cursor = ligacao.execute(
        "DELETE FROM reservas WHERE isbn = ? AND socio = ?", (isbn, numero)
    )
    ligacao.commit()
    ligacao.close()
    if cursor.rowcount == 0:
        mostrar_erro("Não tem nenhuma reserva desse livro.")
    else:
        print("Reserva cancelada.")



def menu_reservas(numero):
# Mostra o menu de reservas de um sócio (ainda por implementar).
    print("Em desenvolvimento.")
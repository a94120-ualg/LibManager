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
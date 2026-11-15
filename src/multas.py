from src.bd import ligar
from src.utils import hoje, dias_entre

TAXA_DIARIA = 0.10


def calcular_multa(dias_atraso):
    return dias_atraso * TAXA_DIARIA


def procurar_atrasos():
    ligacao = ligar()
    consulta = (
        "SELECT e.id, e.socio, l.titulo, e.data_prevista "
        "FROM emprestimos e JOIN livros l ON l.isbn = e.isbn "
        "WHERE e.estado = 'ativo' AND e.data_prevista < ? "
        "ORDER BY e.data_prevista"
    )
    atrasos = ligacao.execute(consulta, (hoje(),)).fetchall()
    ligacao.close()
    return atrasos



def listar_atrasos():
    """Mostra os empréstimos em atraso."""
    atrasos = procurar_atrasos()
    if len(atrasos) == 0:
        print("Não há empréstimos em atraso.")
        return
    print(f"{'Sócio':<8}{'Livro':<26}{'Prazo':<12}Dias de atraso")
    for atraso in atrasos:
        dias = dias_entre(atraso["data_prevista"], hoje())
        print(f"{atraso['socio']:<8}{atraso['titulo']:<26}"
              f"{atraso['data_prevista']:<12}{dias}")


def menu_atrasos():
# Mostra o menu de atrasos e multas do bibliotecário (ainda por implementar).
    print("Em desenvolvimento.")


def consultar_multas_socio(numero):
# Mostra as multas pendentes de um sócio (ainda por implementar).
    print("Em desenvolvimento.")
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
    atrasos = procurar_atrasos()
    if len(atrasos) == 0:
        print("Não há empréstimos em atraso.")
        return
    print(f"{'Sócio':<8}{'Livro':<26}{'Prazo':<12}Dias de atraso")
    for atraso in atrasos:
        dias = dias_entre(atraso["data_prevista"], hoje())
        print(f"{atraso['socio']:<8}{atraso['titulo']:<26}"
              f"{atraso['data_prevista']:<12}{dias}")



def calcular_multas():
    atrasos = procurar_atrasos()
    if len(atrasos) == 0:
        print("Não há empréstimos em atraso.")
        return
    for atraso in atrasos:
        dias = dias_entre(atraso["data_prevista"], hoje())
        valor = calcular_multa(dias)
        print(f"Sócio {atraso['socio']}: {dias} dias x {TAXA_DIARIA:.2f} € "
              f"= {valor:.2f} €")
        
def gerar_multa(id_emprestimo):
    ligacao = ligar()
    emprestimo = ligacao.execute(
        "SELECT * FROM emprestimos WHERE id = ?", (id_emprestimo,)
    ).fetchone()
    dias = dias_entre(emprestimo["data_prevista"], emprestimo["data_devolucao"])
    if dias > 0:
        valor = calcular_multa(dias)
        ligacao.execute(
            "INSERT INTO multas (emprestimo, socio, valor) VALUES (?, ?, ?)",
            (id_emprestimo, emprestimo["socio"], valor)
        )
        ligacao.commit()
        print(f"Devolução com {dias} dias de atraso. Multa: {valor:.2f} €.")
    ligacao.close()



def menu_atrasos():
# Mostra o menu de atrasos e multas do bibliotecário (ainda por implementar).
    print("Em desenvolvimento.")


def consultar_multas_socio(numero):
# Mostra as multas pendentes de um sócio (ainda por implementar).
    print("Em desenvolvimento.")
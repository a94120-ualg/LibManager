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


def consultar_multas_socio(numero):
    ligacao = ligar()
    pendentes = ligacao.execute(
        "SELECT id, valor FROM multas WHERE socio = ? AND paga = 0", (numero,)
    ).fetchall()
    ligacao.close()
    if len(pendentes) == 0:
        print("Não tem multas pendentes.")
        return
    total = 0
    for multa in pendentes:
        print(f"Multa {multa['id']}: {multa['valor']:.2f} €")
        total = total + multa["valor"]
    print(f"Total pendente: {total:.2f} €")


def socio_tem_multas(numero):
    ligacao = ligar()
    linha = ligacao.execute(
        "SELECT COUNT(*) AS total FROM multas WHERE socio = ? AND paga = 0",
        (numero,)
    ).fetchone()
    ligacao.close()
    return linha["total"] > 0



def menu_atrasos():
# Mostra o menu de atrasos e multas do bibliotecário (ainda por implementar).
    print("Em desenvolvimento.")


def consultar_multas_socio(numero):
# Mostra as multas pendentes de um sócio (ainda por implementar).
    print("Em desenvolvimento.")
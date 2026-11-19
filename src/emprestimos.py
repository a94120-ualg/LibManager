# Gestão de empréstimos e pedidos de renovação.
from src import livros, socios, multas
from src.bd import ligar
from src.utils import pedir_texto, pedir_inteiro, hoje, somar_dias, mostrar_erro


PRAZO_DIAS = 14

def contar_emprestimos_ativos(numero):
    ligacao = ligar()
    linha = ligacao.execute(
        "SELECT COUNT(*) AS total FROM emprestimos "
        "WHERE socio = ? AND estado = 'ativo'", (numero,)
    ).fetchone()
    ligacao.close()
    return linha["total"]


def pedir_renovacao(numero):
    listar_emprestimos_ativos(numero)
    id_emprestimo = pedir_inteiro("Nº do empréstimo a renovar (0 para voltar): ")
    if id_emprestimo == 0:
        return
    ligacao = ligar()
    emprestimo = ligacao.execute(
        "SELECT id FROM emprestimos "
        "WHERE id = ? AND socio = ? AND estado = 'ativo'",
        (id_emprestimo, numero)
    ).fetchone()
    if emprestimo is None:
        ligacao.close()
        mostrar_erro("Empréstimo não encontrado.")
        return
    pendente = ligacao.execute(
        "SELECT id FROM pedidos_renovacao "
        "WHERE emprestimo = ? AND estado = 'pendente'", (id_emprestimo,)
    ).fetchone()
    if pendente is not None:
        ligacao.close()
        mostrar_erro("Já existe um pedido pendente para este empréstimo.")
        return
    ligacao.execute(
        "INSERT INTO pedidos_renovacao (emprestimo, data_pedido) VALUES (?, ?)",
        (id_emprestimo, hoje())
    )
    ligacao.commit()
    ligacao.close()
    print("Pedido enviado. Aguarde a resposta do bibliotecário.")



def registar_emprestimo():
    numero = pedir_inteiro("Nº de sócio: ")
    socio = socios.procurar_socio(numero)
    if socio is None:
        mostrar_erro("Sócio não encontrado.")
        return
    if multas.socio_tem_multas(numero):
        mostrar_erro("O sócio tem multas por pagar. Empréstimo não permitido.")
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
    multas.gerar_multa(emprestimo["id"])


def cancelar_emprestimo():
    isbn = pedir_texto("ISBN: ")
    numero = pedir_inteiro("Nº de sócio: ")
    emprestimo = procurar_emprestimo_ativo(isbn, numero)
    if emprestimo is None:
        mostrar_erro("Não existe um empréstimo ativo desse livro para esse sócio.")
        return
    ligacao = ligar()
    ligacao.execute(
        "UPDATE emprestimos SET estado = 'cancelado' WHERE id = ?",
        (emprestimo["id"],)
    )
    ligacao.commit()
    ligacao.close()
    print("Empréstimo cancelado.")


def menu_emprestimos():
    opcao = -1
    while opcao != 0:
        print("\n=== Empréstimos ===")
        print("1. Registar")
        print("2. Devolver")
        print("3. Cancelar")
        print("4. Definir limite por sócio")
        print("0. Voltar")
        opcao = pedir_inteiro("Opção: ")
        if opcao == 1:
            registar_emprestimo()
        elif opcao == 2:
            registar_devolucao()
        elif opcao == 3:
            cancelar_emprestimo()
        elif opcao == 4:
            definir_limite_socio()
        elif opcao != 0:
            mostrar_erro("Opção inválida.")


def listar_emprestimos_ativos(numero):
    ligacao = ligar()
    consulta = (
        "SELECT e.id, l.titulo, e.data_prevista "
        "FROM emprestimos e JOIN livros l ON l.isbn = e.isbn "
        "WHERE e.socio = ? AND e.estado = 'ativo' ORDER BY e.data_prevista"
    )
    ativos = ligacao.execute(consulta, (numero,)).fetchall()
    ligacao.close()
    if len(ativos) == 0:
        print("Não tem empréstimos ativos.")
        return
    for ativo in ativos:
        print(f"{ativo['id']:<6}{ativo['titulo']:<26}"
              f"devolver até {ativo['data_prevista']}")



def definir_limite_socio():
    numero = pedir_inteiro("Nº de sócio: ")
    socio = socios.procurar_socio(numero)
    if socio is None:
        mostrar_erro("Sócio não encontrado.")
        return
    print("Limite atual: " + str(socio["limite_livros"]))
    limite = pedir_inteiro("Novo limite: ")
    ligacao = ligar()
    ligacao.execute(
        "UPDATE socios SET limite_livros = ? WHERE numero = ?", (limite, numero)
    )
    ligacao.commit()
    ligacao.close()
    print("Limite atualizado.")


def ver_pedidos_socio(numero):
    ligacao = ligar()
    consulta = (
        "SELECT l.titulo, p.estado, e.data_prevista "
        "FROM pedidos_renovacao p "
        "JOIN emprestimos e ON e.id = p.emprestimo "
        "JOIN livros l ON l.isbn = e.isbn "
        "WHERE e.socio = ? ORDER BY p.id DESC"
    )
    pedidos = ligacao.execute(consulta, (numero,)).fetchall()
    ligacao.close()
    if len(pedidos) == 0:
        print("Não tem pedidos de renovação.")
        return
    for pedido in pedidos:
        texto = f"{pedido['titulo']:<26}{pedido['estado']}"
        if pedido["estado"] == "aprovado":
            texto = texto + " (nova data: " + pedido["data_prevista"] + ")"
        print(texto)


def listar_pedidos_pendentes():
    ligacao = ligar()
    consulta = (
        "SELECT p.id, s.nome, l.titulo, e.data_prevista "
        "FROM pedidos_renovacao p "
        "JOIN emprestimos e ON e.id = p.emprestimo "
        "JOIN socios s ON s.numero = e.socio "
        "JOIN livros l ON l.isbn = e.isbn "
        "WHERE p.estado = 'pendente' ORDER BY p.id"
    )
    pedidos = ligacao.execute(consulta).fetchall()
    ligacao.close()
    if len(pedidos) == 0:
        print("Não há pedidos pendentes.")
        return pedidos
    for pedido in pedidos:
        print(f"{pedido['id']:<6}{pedido['nome']:<20}{pedido['titulo']:<26}"
              f"prazo atual: {pedido['data_prevista']}")
    return pedidos


def decidir_pedido():
    pedidos = listar_pedidos_pendentes()
    if len(pedidos) == 0:
        return
    id_pedido = pedir_inteiro("Nº do pedido (0 para voltar): ")
    if id_pedido == 0:
        return
    ligacao = ligar()
    consulta = (
        "SELECT e.id AS emprestimo, e.isbn, e.socio, e.data_prevista "
        "FROM pedidos_renovacao p JOIN emprestimos e ON e.id = p.emprestimo "
        "WHERE p.id = ? AND p.estado = 'pendente'"
    )
    pedido = ligacao.execute(consulta, (id_pedido,)).fetchone()
    if pedido is None:
        ligacao.close()
        mostrar_erro("Pedido não encontrado.")
        return
    print("1. Aprovar")
    print("2. Recusar")
    decisao = pedir_inteiro("Opção: ")
    if decisao == 1:
        reservas = ligacao.execute(
            "SELECT COUNT(*) AS total FROM reservas "
            "WHERE isbn = ? AND socio != ?", (pedido["isbn"], pedido["socio"])
        ).fetchone()
        if reservas["total"] > 0:
            mostrar_erro("o livro tem reservas de outros sócios. Recuse o pedido.")
        else:
            nova_data = somar_dias(pedido["data_prevista"], PRAZO_DIAS)
            ligacao.execute(
                "UPDATE emprestimos SET data_prevista = ? WHERE id = ?",
                (nova_data, pedido["emprestimo"])
            )
            ligacao.execute(
                "UPDATE pedidos_renovacao SET estado = 'aprovado' WHERE id = ?",
                (id_pedido,)
            )
            ligacao.commit()
            print("Renovação aprovada. Nova data de devolução: " + nova_data + ".")
    elif decisao == 2:
        ligacao.execute(
            "UPDATE pedidos_renovacao SET estado = 'recusado' WHERE id = ?",
            (id_pedido,)
        )
        ligacao.commit()
        print("Renovação recusada.")
    else:
        mostrar_erro("Opção inválida.")
    ligacao.close()
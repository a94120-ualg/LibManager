from src.bd import ligar
from src.utils import pedir_texto
from src.utils import pedir_texto, pedir_texto_ou_manter, pedir_inteiro, mostrar_erro, confirmar
import sqlite3

def procurar_socio(numero):
    ligacao = ligar()
    socio = ligacao.execute(
        "SELECT * FROM socios WHERE numero = ?", (numero,)
    ).fetchone()
    ligacao.close()
    return socio


def registar_socio():
    nome = pedir_texto("Nome: ")
    contacto = pedir_texto("Contacto: ")
    palavra_passe = pedir_texto("Palavra-passe: ")
    ligacao = ligar()
    cursor = ligacao.execute(
        "INSERT INTO socios (nome, contacto, palavra_passe) VALUES (?, ?, ?)",
        (nome, contacto, palavra_passe)
    )
    ligacao.commit()
    numero = cursor.lastrowid
    ligacao.close()
    print("Sócio nº " + str(numero) + " registado.")


def mostrar_socios(socios):
    if len(socios) == 0:
        print("Nenhum sócio encontrado.")
        return
    print(f"{'Nº':<8}{'Nome':<26}Contacto")
    for socio in socios:
        print(f"{socio['numero']:<8}{socio['nome']:<26}{socio['contacto']}")


def listar_socios():
    ligacao = ligar()
    socios = ligacao.execute("SELECT * FROM socios ORDER BY nome").fetchall()
    ligacao.close()
    mostrar_socios(socios)


def editar_socio():
    numero = pedir_inteiro("Nº de sócio: ")
    socio = procurar_socio(numero)
    if socio is None:
        mostrar_erro("Sócio não encontrado.")
        return
    nome = pedir_texto_ou_manter("Nome", socio["nome"])
    contacto = pedir_texto_ou_manter("Contacto", socio["contacto"])
    ligacao = ligar()
    ligacao.execute(
        "UPDATE socios SET nome = ?, contacto = ? WHERE numero = ?",
        (nome, contacto, numero)
    )
    ligacao.commit()
    ligacao.close()
    print("Sócio atualizado.") 

def remover_socio():
    numero = pedir_inteiro("Nº de sócio: ")
    socio = procurar_socio(numero)
    if socio is None:
        mostrar_erro("Sócio não encontrado.")
        return
    if not confirmar('Remover "' + socio["nome"] + '"?'):
        return
    ligacao = ligar()
    try:
        ligacao.execute("DELETE FROM socios WHERE numero = ?", (numero,))
        ligacao.commit()
        print("Sócio removido.")
    except sqlite3.IntegrityError:
        mostrar_erro("O sócio tem empréstimos, reservas ou multas e não pode ser removido.")
    ligacao.close()  


def pesquisar_socio():
    texto = pedir_texto("Pesquisar (nome ou número): ")
    ligacao = ligar()
    socios = ligacao.execute(
        "SELECT * FROM socios WHERE nome LIKE ? OR CAST(numero AS TEXT) = ? "
        "ORDER BY nome",
        ("%" + texto + "%", texto)
    ).fetchall()
    ligacao.close()
    mostrar_socios(socios)         


def menu_socios():
    opcao = -1
    while opcao != 0:
        print("\n=== Sócios ===")
        print("1. Registar")
        print("2. Editar")
        print("3. Remover")
        print("4. Pesquisar")
        print("5. Listar")
        print("0. Voltar")
        opcao = pedir_inteiro("Opção: ")
        if opcao == 1:
            registar_socio()
        elif opcao == 2:
            editar_socio()
        elif opcao == 3:
            remover_socio()
        elif opcao == 4:
            pesquisar_socio()
        elif opcao == 5:
            listar_socios()
        elif opcao != 0:
            mostrar_erro("Opção inválida.")


def ver_historico_socio(numero):
    ligacao = ligar()
    consulta = (
        "SELECT l.titulo, e.data_emprestimo, e.data_devolucao, e.estado "
        "FROM emprestimos e JOIN livros l ON l.isbn = e.isbn "
        "WHERE e.socio = ? ORDER BY e.data_emprestimo DESC"
    )
    historico = ligacao.execute(consulta, (numero,)).fetchall()
    ligacao.close()
    if len(historico) == 0:
        print("Ainda não requisitou nenhum livro.")
        return
    for registo in historico:
        devolucao = registo["data_devolucao"]
        if devolucao is None:
            devolucao = "em curso"
        print(f"{registo['titulo']:<26}{registo['data_emprestimo']} - "
              f"{devolucao} ({registo['estado']})")
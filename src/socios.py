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


def menu_socios():
# Mostra o menu de sócios do bibliotecário (ainda por implementar).
    print("Em desenvolvimento.")


def ver_historico_socio(numero):
# Mostra o histórico de leituras de um sócio (ainda por implementar).

    print("Em desenvolvimento.")
from src.bd import ligar
from src.utils import pedir_texto

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


def menu_socios():
# Mostra o menu de sócios do bibliotecário (ainda por implementar).
    print("Em desenvolvimento.")


def ver_historico_socio(numero):
# Mostra o histórico de leituras de um sócio (ainda por implementar).

    print("Em desenvolvimento.")
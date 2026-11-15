#codigo ainda provisório
from src.utils import pedir_inteiro, mostrar_erro, pedir_texto
from src.bd import ligar


def iniciar_sessao():
    criar_bibliotecario_por_defeito()
    while True:
        print("\n=== LibManager ===")
        print("Entrar como:")
        print("1. Bibliotecário")
        print("2. Sócio")
        print("0. Sair")
        opcao = pedir_inteiro("Opção: ")
        if opcao == 0:
            return None
        if opcao == 1:
            perfil = "bibliotecario"
        elif opcao == 2:
            perfil = "socio"
        else:
            mostrar_erro("Opção inválida.")
            continue
        numero = pedir_inteiro("Número: ")
        palavra_passe = pedir_texto("Palavra-passe: ")
        if verificar_credenciais(perfil, numero, palavra_passe):
            return {"perfil": perfil, "numero": numero}
        mostrar_erro("Número ou palavra-passe incorretos.")



def criar_bibliotecario_por_defeito():
    ligacao = ligar()
    linha = ligacao.execute(
        "SELECT COUNT(*) AS total FROM bibliotecarios"
    ).fetchone()
    if linha["total"] == 0:
        ligacao.execute(
            "INSERT INTO bibliotecarios (numero, nome, palavra_passe) "
            "VALUES (1, 'Administrador', 'admin')"
        )
        ligacao.commit()
    ligacao.close()


def verificar_credenciais(perfil, numero, palavra_passe):
    ligacao = ligar()
    if perfil == "bibliotecario":
        utilizador = ligacao.execute(
            "SELECT numero FROM bibliotecarios "
            "WHERE numero = ? AND palavra_passe = ?", (numero, palavra_passe)
        ).fetchone()
    else:
        utilizador = ligacao.execute(
            "SELECT numero FROM socios WHERE numero = ? AND palavra_passe = ?",
            (numero, palavra_passe)
        ).fetchone()
    ligacao.close()
    return utilizador is not None
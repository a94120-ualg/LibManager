#codigo ainda provisório
from src.utils import pedir_inteiro, mostrar_erro
from src.bd import ligar


def iniciar_sessao():
    ligar()

    while True:
        print("\n=== LibManager ===")
        print("Entrar como:")
        print("1. Bibliotecário")
        print("2. Sócio")
        print("0. Sair")
        opcao = pedir_inteiro("Opção: ")
        if opcao == 1:
            return {"perfil": "bibliotecario", "numero": 1}
        elif opcao == 2:
            numero = pedir_inteiro("Nº de sócio: ")
            return {"perfil": "socio", "numero": numero}
        elif opcao == 0:
            return None
        mostrar_erro("Opção inválida.")



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
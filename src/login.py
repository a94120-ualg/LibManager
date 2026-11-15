#codigo ainda provisório
from src.utils import pedir_inteiro, mostrar_erro


def iniciar_sessao():

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
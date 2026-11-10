# codigo provisorio do main.py
from src import bd, login, livros, socios, emprestimos, multas, reservas
from src.utils import pedir_inteiro, mostrar_erro


def menu_bibliotecario():
    opcao = -1
    while opcao != 0:
        print("\n=== LibManager - Bibliotecário ===")
        print("1. Livros")
        print("2. Sócios")
        print("3. Empréstimos")
        print("4. Atrasos e multas")
        print("0. Terminar sessão")
        opcao = pedir_inteiro("Opção: ")
        if opcao == 1:
            livros.menu_livros()
        elif opcao == 2:
            socios.menu_socios()
        elif opcao == 3:
            emprestimos.menu_emprestimos()
        elif opcao == 4:
            multas.menu_atrasos()
        elif opcao != 0:
            mostrar_erro("opção inválida.")


def menu_socio(numero):
    opcao = -1
    while opcao != 0:
        print("\n=== LibManager - Sócio ===")
        print("1. Pesquisar livros")
        print("2. Os meus empréstimos")
        print("3. Pedir renovação")
        print("4. Os meus pedidos de renovação")
        print("5. As minhas multas")
        print("6. Reservas")
        print("7. O meu histórico")
        print("0. Terminar sessão")
        opcao = pedir_inteiro("Opção: ")
        if opcao == 1:
            livros.menu_pesquisa()
        elif opcao == 2:
            emprestimos.listar_emprestimos_ativos(numero)
        elif opcao == 3:
            emprestimos.pedir_renovacao(numero)
        elif opcao == 4:
            emprestimos.ver_pedidos_socio(numero)
        elif opcao == 5:
            multas.consultar_multas_socio(numero)
        elif opcao == 6:
            reservas.menu_reservas(numero)
        elif opcao == 7:
            socios.ver_historico_socio(numero)
        elif opcao != 0:
            mostrar_erro("opção inválida.")


def main():
    bd.criar_tabelas()
    sessao = login.iniciar_sessao()
    while sessao is not None:
        if sessao["perfil"] == "bibliotecario":
            menu_bibliotecario()
        else:
            menu_socio(sessao["numero"])
        sessao = login.iniciar_sessao()
    print("Até à próxima.")

if __name__ == "__main__":
    main()
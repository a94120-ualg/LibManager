from datetime import datetime, timedelta

FORMATO_DATA = "%Y-%m-%d"


def mostrar_erro(mensagem):
    print("Erro: " + mensagem)


def pedir_texto(mensagem):
    texto = input(mensagem).strip()
    while texto == "":
        mostrar_erro("O valor não pode estar vazio.")
        texto = input(mensagem).strip()
    return texto


def pedir_texto_ou_manter(mensagem, valor_atual):
    texto = input(mensagem + " [" + str(valor_atual) + "]: ").strip()
    if texto == "":
        return valor_atual
    return texto


def pedir_inteiro(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor.isdigit():
            return int(valor)
        mostrar_erro("Introduza um número inteiro.")


def pedir_data(mensagem):
    while True:
        texto = input(mensagem).strip()
        try:
            datetime.strptime(texto, FORMATO_DATA)
            return texto
        except ValueError:
            mostrar_erro("A data é inválida. Use o formato AAAA-MM-DD.")


def confirmar(mensagem):
    resposta = input(mensagem + " (s/n): ").strip().lower()
    while resposta != "s" and resposta != "n":
        mostrar_erro("Responda com s ou n.")
        resposta = input(mensagem + " (s/n): ").strip().lower()
    return resposta == "s"


def hoje():
    return datetime.now().strftime(FORMATO_DATA)


def somar_dias(data, dias):
    nova_data = datetime.strptime(data, FORMATO_DATA) + timedelta(days=dias)
    return nova_data.strftime(FORMATO_DATA)
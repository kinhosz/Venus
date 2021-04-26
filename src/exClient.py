import Venus
import time
from socket import *


def check(pkt):
    print("---------------------")
    if pkt["code"] == "408":
        print("Server Timeout")
    elif pkt["code"] == "701":
        print("Invalid SessionID")
    elif pkt["code"] == "702":
        print("Sessão fechada")
    elif pkt["code"] == "703":
        print("Sessão ainda não finalizada")
    elif pkt["code"] == "704":
        print("Opção inválida")
    elif pkt["code"] == "901":
        print("Sessão criada.")
        print("ID: ", pkt["sessionID"])
    elif pkt["code"] == "902":
        print("Voto registrado com sucesso!")
    elif pkt["code"] == "903":
        print("Resultados da sessão: ", pkt["sessionID"])
        print(pkt["description"])
        for e in pkt["result"].keys():
            print(e, "recebeu", pkt["result"][e], "votos")
        print("detalhes da votação:\n")
        print("Total de votos:", pkt["totalVotes"])
        if pkt["endingMode"] == 0:
            print("Modo: Tempo")
        else:
            print("Modo: Votos")
        print("Limite: ", pkt["limit"])
        print("Inicio da votação:", pkt["start"])
    else:
        print("Erro no pacote")
    print("---------------------")


def main():

    welcome = "Seja bem-vindo a urna.\n" + \
        "Digite 'CONNECT' para se conectar a um servidor\n" + \
        "Digite 'CREATE' para criar uma sessão.\n" + \
        "Digite 'VOTE' para votar em uma sessão.\n" + \
        "Digite 'CHECK' para checar os resultados de uma sessão\n" + \
        "Digite 'EXIT' para sair da urna\n" + \
        "Comando: "

    client = Venus.vClient()

    comando = input(welcome)
    addr = ("localHost", 12000)

    while comando != "EXIT":
        if comando == "CONNECT":
            welcome = "Digite o IP do server: "
            IP = input(welcome)
            welcome = "Digite a porta do server: "
            port = int(input(welcome))
            addr = (IP, port)
        elif comando == "CREATE":
            welcome = "Digite a descrição da votação: "
            descript = input(welcome)
            welcome = "Digite quantas opções existirão na votação: "
            total = int(input(welcome))
            options = []
            for i in range(1, total+1):
                welcome = "Opção " + str(i) + ": "
                opt = input(welcome)
                options.append(opt)
            welcome = "Qual o modo de fim de votação?\n" + \
                "Digite [0] para tempo\n" + \
                "Digite [1] para votos\n"
            mode = int(input(welcome))
            welcome = "Digite o limite de fim de votação em segundos (caso o modo seja 0) ou votos (caso o modo seja 1): "
            limit = int(input(welcome))
            pkt = client.createSession(addr, descript, options, mode, limit)
            check(pkt)
        elif comando == "VOTE":
            welcome = "Digite o ID da sessão: "
            ID = int(input(welcome))
            welcome = "Digite sua opção: "
            opt = input(welcome)
            pkt = client.vote(addr, ID, opt)
            check(pkt)
        elif comando == "CHECK":
            welcome = "Digite o ID da sessão: "
            ID = int(input(welcome))
            pkt = client.checkResult(addr, ID)
            check(pkt)
        else:
            print("Comando inválido")
        welcome = "Digite o comando: "
        comando = input(welcome)


if __name__ == "__main__":
    main()

import Venus


def main():

    welcome = "Bem-vindo a central de servidores\n" + \
        "Vamos criar um servidor.\n" + \
        "Digite o IP desta máquina: "
    IP = input(welcome)
    welcome = "Digite a porta que será associada a este servidor: "
    PORT = int(input(welcome))
    welcome = "Digite quanto tempo voce deseja que o servidor ficara ativos em segundos\n" + \
        "Digite [0] para tempo indefinido: "
    temp = int(input(welcome))

    server = Venus.vServer((IP, PORT))
    server.register()
    if temp == 0:
        server.listen(None)
    else:
        server.listen(temp)
    print("Server fechado")


if __name__ == "__main__":
    main()

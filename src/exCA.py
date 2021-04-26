import Venus


def main():

    welcome = "Bem-vindo ao CA.\n" + \
        "Caso queira o CA rodando por tempo indefinidido, digite 0.\n" + \
        "Caso contrário, digite quanto tempo em segundos o CA deve ficar funcional\n"

    t = int(input(welcome))
    CA = Venus.vCA()
    if t == 0:
        CA.listen(None)
    else:
        CA.listen(t)


if __name__ == "__main__":
    main()

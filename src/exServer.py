import Venus


def main():
    server = Venus.vServer()
    server.register()
    server.listen()


if __name__ == "__main__":
    main()

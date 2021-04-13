import Venus


def main():
    server = Venus.vServer()
    server.register()
    server.listen(60)


if __name__ == "__main__":
    main()

import Venus
from socket import *


def main():

    client = Venus.vClient()
    client.vote((gethostbyname("localhost"), 12000), 3, 3)


if __name__ == "__main__":
    main()

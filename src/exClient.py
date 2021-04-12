import Venus
from socket import *


def main():

    client = Venus.vClient()
    pubKey = client.getServerPK((gethostbyname("localHost"), 12000))
    if pubKey == None:
        print("None")
    else:
        print(pubKey)


if __name__ == "__main__":
    main()

import Venus
import time
from socket import *


def main():

    client = Venus.vClient()
    addr = (gethostbyname("localhost"), 12000)
    pkt = client.createSession(addr, "eleicao 2022", [
        "ambrosio", "kinho", "perazzo", "vivi"], endingMode=0, limit=30)
    sessionID = pkt["sessionID"]
    pkt = client.vote(addr, sessionID, "kinho")
    print(pkt)
    pkt = client.vote(addr, sessionID, "ambrosio")
    print(pkt)
    pkt = client.vote(addr, sessionID, "kinho")
    print(pkt)
    pkt = client.vote(addr, sessionID, "ambrosio")
    print(pkt)
    pkt = client.vote(addr, sessionID, "kinho")
    print(pkt)
    pkt = client.vote(addr, sessionID - 1, "kinho")
    print(pkt)
    pkt = client.checkResult(addr, sessionID)
    while pkt["code"] == "703":
        time.sleep(0.1)
        pkt = client.checkResult(addr, sessionID)
    print(pkt)


if __name__ == "__main__":
    main()

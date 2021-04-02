from client.Client import *

if __name__ == "__main__":

    s = vClient()
    s.createSession(("localhost", 12000), "fodase", ["amb", "kinho"])

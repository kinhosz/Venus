import rsa
import sys
import os
import json
import shutil
from socket import *


class vHost():

    def __init__(self, CAaddr=(gethostbyname("localhost"), 1234), owner="github.com/kinhosz/Venus"):
        self.__CAaddr = CAaddr
        (pubKey, privKey) = rsa.newkeys(1024)
        self.__CApubKey = pubKey
        self.__CAprivKey = privKey
        self.__owner = owner
        f = open("Venus/Host/LICENSE")
        self.__license = f.read()
        f.close()

    def run(self):
        self.__mkdir("dist")

        self.__distClient("dist")
        self.__distServer("dist")

    def __error(self):
        shutil.rmtree("dist", ignore_errors=True)
        sys.exit()

    def __mkdir(self, path):
        try:
            os.mkdir(path)
        except:
            print("An error occur during create the", path, "directory")
            self.__error()

    def __copyFile(self, orig, dest):
        try:
            f = open(orig, "r")
            txt = f.read()
            f.close()
        except:
            print("An error occur during read the", orig, "file")
            self.__error()
        try:
            f = open(dest, "w")
            f.write(txt)
            f.close()
        except:
            print("An error occur during write the", dest, "file")
            self.__error()

    def __distClient(self, path):
        path = path + "/CLIENT"
        self.__mkdir(path)
        f = open(path + "/README.md", "w")
        f.write("This package was distributed by " +
                str(self.__owner) + " for use on the client side.")
        f.close()
        f = open(path + "/LICENSE", "w")
        f.write(self.__license)
        f.close()
        path = path + "/Venus"
        self.__mkdir(path)
        self.__copyTCP(path)
        self.__copyCrypto(path)
        self.__copyclient(path)
        f = open(path + "/__init__.py", "w")
        text = "# PACKAGE VENUS" + "\n" + "from Venus.client.Client import *" + "\n"
        f.write(text)
        f.close()

    def __distServer(self, path):
        path = path + "/SERVER"
        self.__mkdir(path)
        f = open(path + "/README.md", "w")
        f.write("This package was distributed by " +
                str(self.__owner) + " for use on the server and CA sides.")
        f.close()
        f = open(path + "/LICENSE", "w")
        f.write(self.__license)
        f.close()
        path = path + "/Venus"
        self.__mkdir(path)
        self.__copyTCP(path)
        self.__copyCrypto(path)
        self.__copyserver(path)
        self.__copyCA(path)
        text = "# PACKAGE VENUS" + "\n" + "from Venus.CA.ca import *" + \
            "\n" + "from Venus.server.Server import *" + "\n"
        f = open(path + "/__init__.py", "w")
        f.write(text)
        f.close()

    def __copyCA(self, path):
        path = path + "/CA"
        self.__mkdir(path)
        self.__copyFile("Venus/CA/ca.py", path + "ca.py")
        path = path + "/data"
        self.__mkdir(path)
        pkt = {}
        txt = json.dumps(pkt)
        f = open(path + "/database.txt", "w")
        f.write(txt)
        f.close()
        pkt["privKey"] = {
            "n": self.__CAprivKey.n,
            "e": self.__CAprivKey.e,
            "d": self.__CAprivKey.d,
            "p": self.__CAprivKey.p,
            "q": self.__CAprivKey.q
        }
        pkt["addr"] = {
            "ip": self.__CAaddr[0],
            "port": self.__CAaddr[1]
        }
        txt = json.dumps(pkt)
        f = open(path + "/CAKey.txt", "w")
        f.write(txt)
        f.close()

    def __copyclient(self, path):
        path = path + "/client"
        self.__mkdir(path)
        self.__copyFile("Venus/client/Client.py", path + "/Client.py")
        path = path + "/data"
        self.__mkdir(path)
        pkt = {}
        pkt["pubKey"] = {
            "n": self.__CAprivKey.n,
            "e": self.__CAprivKey.e
        }
        pkt["addr"] = {
            "ip": self.__CAaddr[0],
            "port": self.__CAaddr[1]
        }
        txt = json.dumps(pkt)
        f = open(path + "/CAKey.txt", "w")
        f.write(txt)
        f.close()

    def __copyCrypto(self, path):
        path = path + "/Crypto"
        self.__mkdir(path)
        self.__copyFile("Venus/Crypto/crypto.py", path + "/crypto.py")

    def __copyserver(self, path):
        path = path + "/server"
        self.__mkdir(path)
        self.__copyFile("Venus/server/Server.py", path + "/Server.py")
        path = path + "/data"
        self.__mkdir(path)
        pkt = {}
        pkt["pubKey"] = {
            "n": self.__CAprivKey.n,
            "e": self.__CAprivKey.e
        }
        pkt["addr"] = {
            "ip": self.__CAaddr[0],
            "port": self.__CAaddr[1]
        }
        txt = json.dumps(pkt)
        f = open(path + "/CAKey.txt", "w")
        f.write(txt)
        f.close()

    def __copyTCP(self, path):
        path = path + "/TCP"
        self.__mkdir(path)
        self.__copyFile("Venus/TCP/callisto.py", path + "/callisto.py")

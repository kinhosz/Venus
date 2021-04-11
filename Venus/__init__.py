# DEPENDENCIES
import time
import random
import json
import rsa
import datetime
from socket import *
from threading import Thread
# PACKAGE VENUS
from Venus.CA.CA import vCA
from Venus.client.Client import vClient
from Venus.Crypto.crypto import decrypt
from Venus.Crypto.crypto import encrypt
from Venus.server.Server import vServer
from Venus.TCP.callisto import *

CAKEY = "Venus/CA/data/CAKey.txt"
CA_DATABASE = "Venus/CA/data/database.txt"

# DEPENDENCIES
import rsa


def encrypt(data, pubKey):
    response = bytes(0)
    block = rsa.common.byte_size(pubKey.n) - 11
    end = len(data)
    initial = 0
    while initial < end:
        finish = min(initial+block, end)
        response = response + rsa.encrypt(data[initial:finish], pubKey)
        initial = initial + block
    return response


def decrypt(data, privKey):
    response = bytes(0)
    block = rsa.common.byte_size(privKey.n)
    end = len(data)
    initial = 0
    while initial < end:
        finish = min(initial+block, end)
        response = response + rsa.decrypt(data[initial:finish], privKey)
        initial = initial + block
    return response

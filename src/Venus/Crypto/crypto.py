# DEPENDENCIES
import rsa


def encrypt(data, pubKey):
    try:
        response = bytes(0)
        block = rsa.common.byte_size(pubKey.n) - 11
        end = len(data)
        initial = 0
        while initial < end:
            finish = min(initial+block, end)
            response = response + rsa.encrypt(data[initial:finish], pubKey)
            initial = initial + block
        return response
    except:
        print("encrypt failed")
        return data


def decrypt(data, privKey):
    try:
        response = bytes(0)
        block = rsa.common.byte_size(privKey.n)
        end = len(data)
        initial = 0
        while initial < end:
            finish = min(initial+block, end)
            response = response + rsa.decrypt(data[initial:finish], privKey)
            initial = initial + block
        return response
    except:
        print("decrypt failed")
        return data

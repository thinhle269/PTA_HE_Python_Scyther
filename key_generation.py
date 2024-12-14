# This file handles key generation using TPM simulation.

from Crypto.PublicKey import RSA
import time


def generate_keys():
    start_time = time.time()
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    elapsed_time = time.time() - start_time
    return private_key, public_key, elapsed_time

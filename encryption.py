# This file handles encryption and decryption operations.

import seal as ps
import time


def encrypt_state(state, public_key):
    start_time = time.time()
    parms = ps.EncryptionParameters(ps.scheme_type.bfv)
    poly_modulus_degree = 4096
    parms.set_poly_modulus_degree(poly_modulus_degree)
    parms.set_coeff_modulus(ps.CoeffModulus.BFVDefault(poly_modulus_degree))
    # Higher state value requires higher plain modulus
    parms.set_plain_modulus(524288)

    context = ps.SEALContext(parms)
    keygen = ps.KeyGenerator(context)
    public_key = keygen.create_public_key()

    encryptor = ps.Encryptor(context, public_key)
    evaluator = ps.Evaluator(context)
    decryptor = ps.Decryptor(context, keygen.secret_key())

    plain_state = ps.Plaintext(str(state))
    encrypted_state = encryptor.encrypt(plain_state)
    elapsed_time = time.time() - start_time

    return encrypted_state, evaluator, decryptor, elapsed_time

# This file handles the homomorphic operations

import seal as ps


def homomorphic_evaluation(enc_state_1, enc_state_2, evaluator):
    result = ps.Ciphertext()
    result = evaluator.add(enc_state_1, enc_state_2)
    return result

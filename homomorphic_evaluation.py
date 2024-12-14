# This file handles the homomorphic operations

import seal as ps
import time


def homomorphic_evaluation(enc_state_1, enc_state_2, evaluator):
    start_time = time.time()
    result = evaluator.add(enc_state_1, enc_state_2)
    elapsed_time = time.time() - start_time
    return result, elapsed_time

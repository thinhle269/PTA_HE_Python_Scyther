# This file simulates the protocol using SimPy

import sys
import simpy
import time
from key_generation import generate_keys
from encryption import encrypt_state
from homomorphic_evaluation import homomorphic_evaluation


def protocol(env, results):
    total_latency = 0

    # Step 1: Key Generation
    sk, pk, key_gen_time = generate_keys()
    results['Key Gen (TPM)'] = key_gen_time
    total_latency += key_gen_time
    yield env.timeout(key_gen_time)

    # Step 2: Encryption
    enc_state_1, evaluator, decryptor, enc_time_1 = encrypt_state(12345, pk)
    enc_state_2, _, _, enc_time_2 = encrypt_state(67890, pk)
    results['Encryption (Device)'] = enc_time_1 + enc_time_2
    total_latency += enc_time_1 + enc_time_2
    yield env.timeout(enc_time_1 + enc_time_2)

    # Step 3: Homomorphic Evaluation
    result, eval_time = homomorphic_evaluation(
        enc_state_1, enc_state_2, evaluator)
    results['Homomorphic Eval (Verifier)'] = eval_time
    total_latency += eval_time
    yield env.timeout(eval_time)

    # Step 4: Decryption
    start_time = time.time()
    plain_result = decryptor.decrypt(result)
    decryption_time = time.time() - start_time
    results['Decryption (Verifier)'] = decryption_time
    total_latency += decryption_time
    yield env.timeout(decryption_time)

    # Total latency
    results['Total Latency'] = total_latency


def run_simulation():
    results = {}
    env = simpy.Environment()
    env.process(protocol(env, results))
    env.run()
    return results


def get_message_size(message):
    return sys.getsizeof(message)


if __name__ == '__main__':
    results = run_simulation()
    print(results)

# This file simulates the protocol using SimPy

import simpy
from key_generation import generate_keys
from encryption import encrypt_state
from homomorphic_evaluation import homomorphic_evaluation


def protocol(env):
    print(f'Time {env.now}: Mobile Device starts key generation')
    sk, pk = generate_keys()
    yield env.timeout(5)

    print(f'Time {env.now}: Mobile Device encrypts state')
    enc_state_1, evaluator, decryptor = encrypt_state(12345, pk)
    enc_state_2, _, _ = encrypt_state(67890, pk)
    yield env.timeout(8)

    print(f'Time {env.now}: Verifier performs homomorphic evaluation')
    result = homomorphic_evaluation(enc_state_1, enc_state_2, evaluator)
    yield env.timeout(45)

    print(f'Time {env.now}: Decrypting the result')
    plain_result = decryptor.decrypt(result)
    print(f'Result: {plain_result.to_string()}')


def run_simulation():
    env = simpy.Environment()
    env.process(protocol(env))
    env.run()


if __name__ == '__main__':
    run_simulation()

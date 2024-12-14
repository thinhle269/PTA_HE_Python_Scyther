# This file simulates the protocol using SimPy

import sys


def get_message_size(message):
    return sys.getsizeof(message)


def protocol(env, results):
    # Step 1: Key Generation
    sk, pk, key_gen_time = generate_keys()
    results['Key Gen (TPM)'] = key_gen_time
    yield env.timeout(key_gen_time)

    # Step 2: Encryption
    enc_state_1, evaluator, decryptor, enc_time_1 = encrypt_state(12345, pk)
    enc_state_2, _, _, enc_time_2 = encrypt_state(67890, pk)
    results['Encryption (Device)'] = enc_time_1 + enc_time_2
    yield env.timeout(enc_time_1 + enc_time_2)

    # Calculate communication overhead
    results['Initial Attestation Request'] = get_message_size(
        enc_state_1) + get_message_size(enc_state_2)

    # Step 3: Homomorphic Evaluation
    result, eval_time = homomorphic_evaluation(
        enc_state_1, enc_state_2, evaluator)
    results['Homomorphic Eval (Verifier)'] = eval_time
    yield env.timeout(eval_time)

    # Step 4: Decryption
    start_time = time.time()
    plain_result = decryptor.decrypt(result)
    decryption_time = time.time() - start_time
    results['Decryption (Verifier)'] = decryption_time
    yield env.timeout(decryption_time)
    results['Final Verification Result'] = get_message_size(result)

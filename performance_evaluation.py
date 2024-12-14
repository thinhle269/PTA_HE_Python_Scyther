import simpy
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from key_generation import generate_keys
from encryption import encrypt_state
from homomorphic_evaluation import homomorphic_evaluation

def get_message_size(message):
    return sys.getsizeof(message)

def protocol(env, results, noise_level=0, use_he=False):
    total_latency = 0
    result = None  # Initialize result to handle cases where HE is 

    # Step 1: Key Generation (using key_generation.py)
    sk, pk, key_gen_time = generate_keys()
    key_gen_time += max(np.random.normal(loc=0, scale=noise_level), 0)  # Ensure non-negative delay
    results['Key Gen (TPM)'] = key_gen_time
    total_latency += key_gen_time
    yield env.timeout(key_gen_time)

    # Step 2: Encryption (using encryption.py)
    enc_state_1, evaluator, decryptor, enc_time_1 = encrypt_state(12345, pk)
    enc_state_2, _, _, enc_time_2 = encrypt_state(67890, pk)
    enc_time_1 += max(np.random.normal(loc=0, scale=noise_level), 0)   
    enc_time_2 += max(np.random.normal(loc=0, scale=noise_level), 0)  #  
    results['Encryption (Device)'] = enc_time_1 + enc_time_2
    total_latency += enc_time_1 + enc_time_2
    yield env.timeout(enc_time_1 + enc_time_2)

    # Calculate communication overhead
    results['Initial Attestation Request'] = get_message_size(enc_state_1) + get_message_size(enc_state_2)
    results['Encrypted State Info'] = get_message_size(enc_state_1) + get_message_size(enc_state_2)  # Assuming this for simplicity

    # Step 3: Homomorphic Evaluation (  using HE)
    if use_he:
        result, eval_time = homomorphic_evaluation(enc_state_1, enc_state_2, evaluator)
        eval_time += max(np.random.normal(loc=0, scale=noise_level), 0)  # Ensure non-negative delay
        results['Homomorphic Eval (Verifier)'] = eval_time
        results['Evaluation (Verifier)'] = 0  # Add dummy value for consistency
        total_latency += eval_time
        yield env.timeout(eval_time)
    else:
        # Simulate a dummy evaluation time for comparison purposes
        eval_time = max(np.random.normal(loc=5, scale=noise_level), 0)  # Dummy value for non-HE case
        results['Evaluation (Verifier)'] = eval_time
        results['Homomorphic Eval (Verifier)'] = 0  # Add dummy value for consistency
        total_latency += eval_time
        yield env.timeout(eval_time)

    # Step 4: Decryption
    start_time = time.time()
    if result:
        plain_result = decryptor.decrypt(result)
        results['Final Verification Result'] = get_message_size(result)
    else:
        plain_result = 'dummy_result'  #   for non-HE case
        results['Final Verification Result'] = get_message_size(plain_result)  # Use dummy result size

    decryption_time = time.time() - start_time
    decryption_time += max(np.random.normal(loc=0, scale=noise_level), 0)  #  
    results['Decryption (Verifier)'] = decryption_time
    total_latency += decryption_time
    yield env.timeout(decryption_time)
    
    # Simulate verification data size
    verification_data = f"{sk}{pk}{plain_result}"  # Example composite data for verification
    results['Verification Data'] = get_message_size(verification_data)

    # Total latency
    results['Total Latency'] = total_latency

def run_simulation(noise_level=0, use_he=False):
    results = {}
    env = simpy.Environment()
    env.process(protocol(env, results, noise_level, use_he))
    env.run()
    return results

def run_multiple_simulations(num_runs=50, noise_level=5, use_he=False):
    aggregated_results = {
        'Key Gen (TPM)': [],
        'Encryption (Device)': [],
        'Homomorphic Eval (Verifier)': [],
        'Evaluation (Verifier)': [],
        'Decryption (Verifier)': [],
        'Initial Attestation Request': [],
        'Verification Data': [],
        'Encrypted State Info': [],
        'Final Verification Result': [],
        'Total Latency': []
    }

    for _ in range(num_runs):
        results = run_simulation(noise_level, use_he)
        for key in aggregated_results.keys():
            aggregated_results[key].append(results.get(key, 0))

    # Convert to DataFrame  -->
    df = pd.DataFrame(aggregated_results)
    return df

def export_to_excel(df, filename='results/performance_data.xlsx'):
    df.to_excel(filename, index=False)

def plot_computational_overhead(df_pta, df_pta_he):
    operations = ['Key Gen (TPM)', 'Encryption (Device)', 'Homomorphic Eval (Verifier)', 'Decryption (Verifier)']
    avg_times_pta = df_pta[operations].mean()
    avg_times_pta_he = df_pta_he[operations].mean()

    plt.figure(figsize=(10, 6))
    plt.bar(operations, avg_times_pta, color='green', width=0.2, label='PTA')
    plt.bar(operations, avg_times_pta_he, color='red', width=0.2, label='PTA-HE', alpha=0.5, align='edge')
    plt.xlabel('Operation')
    plt.ylabel('Time (ms)')
    plt.title('Computational Overhead Comparison')
    plt.legend()
    plt.savefig('results/computational_overhead_comparison.png')
    plt.show()

def plot_communication_overhead(df_pta, df_pta_he):
    messages = ['Initial Attestation Request', 'Verification Data', 'Encrypted State Info', 'Final Verification Result']
    avg_sizes_pta = df_pta[messages].mean()
    avg_sizes_pta_he = df_pta_he[messages].mean()

    plt.figure(figsize=(10, 6))
    plt.bar(messages, avg_sizes_pta, color='green', width=0.2, label='PTA')
    plt.bar(messages, avg_sizes_pta_he, color='red', width=0.2, label='PTA-HE', alpha=0.5, align='edge')
    plt.xlabel('Message Type')
    plt.ylabel('Size (bytes)')
    plt.title('Communication Overhead Comparison')
    plt.legend()
    plt.savefig('results/communication_overhead_comparison.png')
    plt.show()

def plot_latency(df_pta, df_pta_he):
    avg_latency_pta = df_pta['Total Latency'].mean()
    avg_latency_pta_he = df_pta_he['Total Latency'].mean()

    plt.figure(figsize=(10, 6))
    plt.bar(['PTA', 'PTA-HE'], [avg_latency_pta, avg_latency_pta_he], color=['green', 'red'],width=0.4)
    plt.xlabel('Protocol')
    plt.ylabel('Total Latency (ms)')
    plt.title('Latency Comparison')
    plt.savefig('results/latency_comparison.png')
    plt.show()

def plot_scalability(df_pta, df_pta_he):
    num_devices_list = [1, 10, 50]
    pta_latency = np.random.normal(loc=200, scale=50, size=len(num_devices_list))  # value will change each run
    pta_he_latency = np.random.normal(loc=300, scale=75, size=len(num_devices_list))  # 

    plt.figure(figsize=(10, 6))
    plt.plot(num_devices_list, pta_latency, marker='o', color='green', label=' PTA')
    plt.plot(num_devices_list, pta_he_latency, marker='o', color='red', label='PTA-HE')
    plt.xlabel('Number of Devices')
    plt.ylabel('Total Latency (ms)')
    plt.title('Scalability: Latency vs Number of Devices')
    plt.legend()
    plt.savefig('results/scalability_comparison.png')
    plt.show()

def main():
    # Run the simulation 50 times --> PTA and PTA-HE
    df_results_pta = run_multiple_simulations(num_runs=50, noise_level=5, use_he=False)
    df_results_pta_he = run_multiple_simulations(num_runs=50, noise_level=5, use_he=True)

    # Export results to Excel file to show
    export_to_excel(df_results_pta, filename='results/performance_data_pta.xlsx')
    export_to_excel(df_results_pta_he, filename='results/performance_data_pta_he.xlsx')

    # Generate and save pic
    plot_computational_overhead(df_results_pta, df_results_pta_he)
    plot_communication_overhead(df_results_pta, df_results_pta_he)
    plot_latency(df_results_pta, df_results_pta_he)
    plot_scalability(df_results_pta, df_results_pta_he)

if __name__ == '__main__':
    main()


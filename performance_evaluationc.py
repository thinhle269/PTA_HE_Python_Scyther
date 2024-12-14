import matplotlib.pyplot as plt

def plot_computational_overhead():
    operations = ['Key Gen (TPM)', 'Encryption (Device)', 'Homomorphic Eval (Verifier)', 'Decryption (Verifier)']
    pta_times = [5, 8, 0, 4]  # Replace with real data
    pta_he_times = [7, 12, 45, 9]  # Replace with real data

    plt.figure(figsize=(10, 6))
    plt.bar(operations, pta_times, color='green', width=0.2, label='Traditional PTA')
    plt.bar(operations, pta_he_times, color='red', width=0.2, label='PTA-HE', alpha=0.6, align='edge')
    plt.xlabel('Operation')
    plt.ylabel('Time (ms)')
    plt.title('Computational Overhead Comparison')
    plt.legend()
    plt.savefig('results/computational_overhead.png')
    plt.show()

def plot_communication_overhead():
    messages = ['Initial Attestation Request', 'Verification Data', 'Encrypted State Info', 'Final Verification Result']
    pta_sizes = [1.2, 1.8, 0, 0.9]  # Replace with real data
    pta_he_sizes = [1.8, 2.3, 4.5, 1.3]  # Replace with real data

    plt.figure(figsize=(10, 6))
    plt.bar(messages, pta_sizes, color='green', width=0.2, label='Traditional PTA')
    plt.bar(messages, pta_he_sizes, color='red', width=0.2, label='PTA-HE', alpha=0.6, align='edge')
    plt.xlabel('Message Type')
    plt.ylabel('Size (KB)')
    plt.title('Communication Overhead Comparison')
    plt.legend()
    plt.savefig('results/communication_overhead.png')
    plt.show()

def plot_latency():
    devices = ['1 Device', '10 Devices', '50 Devices']
    pta_latency = [50, 180, 950]  # Replace with real data
    pta_he_latency = [75, 300, 1600]  # Replace with real data

    plt.figure(figsize=(10, 6))
    plt.plot(devices, pta_latency, marker='o', color='green', label='Traditional PTA')
    plt.plot(devices, pta_he_latency, marker='o', color='red', label='PTA-HE')
    plt.xlabel('Number of Devices')
    plt.ylabel('Latency (ms)')
    plt.title('Latency Comparison')
    plt.legend()
    plt.savefig('results/latency_comparison.png')
    plt.show()

def plot_scalability():
    num_devices_list = [1, 10, 50]
    pta_latency = [50, 180, 950]  # Replace with real data
    pta_he_latency = [75, 300, 1600]  # Replace with real data

    plt.figure(figsize=(10, 6))
    plt.plot(num_devices_list, pta_latency, marker='o', color='green', label='Traditional PTA')
    plt.plot(num_devices_list, pta_he_latency, marker='o', color='red', label='PTA-HE')
    plt.xlabel('Number of Devices')
    plt.ylabel('Total Latency (ms)')
    plt.title('Scalability: Latency vs Number of Devices')
    plt.legend()
    plt.savefig('results/scalability.png')
    plt.show()

if __name__ == '__main__':
    plot_computational_overhead()
    plot_communication_overhead()
    plot_latency()
    plot_scalability()

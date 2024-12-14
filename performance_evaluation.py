# This file handles the performance evaluation and graph generation

import matplotlib.pyplot as plt


def plot_computational_overhead():
    operations = ['Key Gen (TPM)', 'Encryption (Device)',
                  'Homomorphic Eval (Verifier)', 'Decryption (Verifier)']
    pta_times = [5, 8, 0, 4]  # Replace with real data
    pta_he_times = [7, 12, 45, 9]  # Replace with real data

    plt.figure(figsize=(10, 6))
    plt.bar(operations, pta_times, color='blue',
            width=0.4, label='Traditional PTA')
    plt.bar(operations, pta_he_times, color='green',
            width=0.4, label='PTA-HE', alpha=0.7, align='edge')
    plt.xlabel('Operation')
    plt.ylabel('Time (ms)')
    plt.title('Computational Overhead Comparison')
    plt.legend()
    plt.savefig('results/computational_overhead.png')
    plt.show()


if __name__ == '__main__':
    plot_computational_overhead()

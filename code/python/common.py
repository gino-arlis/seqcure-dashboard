import argparse
import os
import csv
import math
import numpy as np
from qiskit import transpile, ClassicalRegister, QuantumCircuit, QuantumRegister

# launching job reference for later, getting results later
 
import qiskit.circuit.library as lib
from pathlib import Path

# this is mount
data_directory = '/media/seqcuredata/dailyjobs'
# create the folder if it doesn't exist 
if not os.path.exists(data_directory): 
    os.makedirs(data_directory)

# method to parse command line arguments 
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", "-t", default=None, help="Target (Hardware) Identifier", type=str)
    parser.add_argument("--qubits", "-q", default=None, help="Number of qubits", type=int)
    parser.add_argument("--shots", "-s", default=None, help="Number of shots", type=int)
    parser.add_argument('--swaps', dest='doswaps', action='store_true', help='Set the flag value to True.')
    parser.add_argument('--no-swaps', dest='doswaps', action='store_false', help='Set the flag value to False.')
    parser.add_argument("--inverse", dest='doinverse', action='store_true', help="Add 1 and append inverse circuit")
    parser.add_argument("--no-inverse", dest='doinverse', action='store_false', help="Do not append inverse circuit")
    return parser.parse_args()                    

def build_qft_circuit(num_qubits, backend, shots, use_swaps=True, apply_inverse=False, do_transpile=True):

    swaps_str = "swaps"
    inverse_str = "noinverse"
    if not use_swaps:
        swaps_str = "noswaps"
    if apply_inverse:
        inverse_str = "inverse"

    # reset random seed 
    np.random.seed(0)    

    # generate input string based on the number of qubits
    secret_int_list = np.random.choice(2**(num_qubits), 1, False)

    for secret_int in secret_int_list:
        # allocate qubits
        qr = QuantumRegister(num_qubits); cr = ClassicalRegister(num_qubits)
        qc = QuantumCircuit(qr, cr, name=f"qft-{num_qubits}-{secret_int}-{swaps_str}-{inverse_str}-{shots}")
        
        # Perform X on each qubit that matches a bit in secret string
        s = ('{0:0'+str(num_qubits)+'b}').format(secret_int)
        for i_qubit in range(num_qubits):
            if s[num_qubits-1-i_qubit]=='1':
                qc.x(qr[i_qubit])

        qc.barrier()

        qft_circuit = lib.QFT(num_qubits=num_qubits, do_swaps=use_swaps, inverse=False)

        qc.append(qft_circuit.to_instruction(), qr)

        qc.barrier()

        if apply_inverse:
            for i_q in range(0, num_qubits):
                divisor = 2**(i_q)
                qc.rz(1 * math.pi / divisor, qr[i_q])

            qc.barrier()

            iqft_circuit = lib.QFT(num_qubits=num_qubits, do_swaps=use_swaps, inverse=True)

            qc.append(iqft_circuit.to_instruction(), qr)

            qc.barrier()

        qc.measure_all()
    
        decomposed_ciruit = qc.decompose().decompose()
        common_basis_set_metrics = get_common_basis_set_metrics(decomposed_ciruit)

        if do_transpile:
            final_circuit = transpile(decomposed_ciruit, backend)
        else:
            final_circuit = decomposed_ciruit

        transpiled_for_backend_metrics = get_circuit_metrics(transpile(decomposed_ciruit, backend))
        return final_circuit, common_basis_set_metrics, transpiled_for_backend_metrics    
 
def write_results_to_csv(filename, results, header):
    #check if file exists
    exists = os.path.isfile(filename)
    if not exists:
         # dataframe will read this
        #then write this to csv
        with open(filename, "w") as file:
            writer = csv.writer(file)
            writer.writerow(header)

    #now append results to csv
    with open(filename, "a") as file:
        writer = csv.writer(file)
        writer.writerow(results)


def get_circuit_metrics(qc):    
    # obtain initial circuit size metrics
    qc_depth = qc.depth()
    qc_size = qc.size()
    qc_count_ops = qc.count_ops()
    qc_xi = 0
    qc_n2q = 0
    qc_n1q = 0 
    
    # iterate over the ordereddict to determine xi (ratio of 2 qubit gates to one qubit gates)
    n1q = 0; n2q = 0
    if qc_count_ops != None:
        for key, value in qc_count_ops.items():
            if key == "measure": continue
            if key == "barrier": continue
            if key.startswith("c") or key.startswith("mc"):
                n2q += value
            else:
                n1q += value
        qc_xi = n2q / (n1q + n2q)
        qc_n2q = n2q
        qc_n1q = n1q

    return (qc_depth, qc_size, qc_xi, qc_n1q, qc_n2q)

def get_common_basis_set_metrics(qc):
    # Selection of basis gate set for transpilation
    # Note: selector 1 is a hardware agnostic gate set
    basis_selector = 1
    basis_gates_array = [
        [],
        ['rx', 'ry', 'rz', 'cx'],       # a common basis set, default
        ['cx', 'rz', 'sx', 'x'],        # IBM default basis set
        ['rx', 'ry', 'rxx'],            # IonQ default basis set
        ['h', 'p', 'cx'],               # another common basis set
        ['u', 'cx']                     # general unitaries basis gates
    ]

    basis_gates = basis_gates_array[basis_selector]
    qc = transpile(qc, basis_gates=basis_gates, seed_transpiler=0)

    return get_circuit_metrics(qc)
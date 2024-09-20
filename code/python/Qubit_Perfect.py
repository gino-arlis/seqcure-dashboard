import common
from qiskit_aer import Aer
from icecream import ic
from qiskit.quantum_info.analysis import hellinger_fidelity
import json

# Setup simulator backend
#provider = BraketProvider()
target_name = 'aer_simulator' # this is a noise-free simulator
provider = Aer
backend = provider.get_backend(target_name)

# build and transpile the qft circuit
num_qubits8 = 8
num_qubits10 = 10
num_qubits12 = 12
circuit1 = common.build_qft_circuit(num_qubits8, backend)
circuit2 = common.build_qft_circuit(num_qubits10, backend)
circuit3 = common.build_qft_circuit(num_qubits12, backend)

# Run the simulation
result1 = backend.run(circuit1).result()
result2 = backend.run(circuit2).result()
result3 = backend.run(circuit3).result()


# Get the results
#ic.disable()
counts_8_qubit = ic(result1.get_counts(circuit1))
counts_10_qubit = ic(result2.get_counts(circuit2))
counts_12_qubit = ic(result3.get_counts(circuit3))

with open("Qubit_8_Data.json", "w") as outfile: 
    json.dump(counts_8_qubit, outfile)

with open("Qubit_10_Data.json", "w") as outfile: 
    json.dump(counts_10_qubit, outfile)

with open("Qubit_12_Data.json", "w") as outfile: 
    json.dump(counts_12_qubit, outfile)

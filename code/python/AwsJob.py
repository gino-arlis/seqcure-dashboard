
import os, boto3
import datetime as dt
import common
from qiskit_braket_provider import BraketProvider
 
# launching job reference for later, getting results later

header = ["Current Time", "Job ID", "Circuit", "Target", "Target Status", "Number of Qubits", "Submission Time", "Submission Status", "Queue Depth", "Position in Queue"
          "Common Basis Depth", "Common Basis Size", "Common Basis Xi", "Common Basis n1q", "Common Basis n2q",
          "Depth", "Size", "Xi", "n1q", "n2q"]  #add others

session = boto3.Session(profile_name="992382759470_BraketQuantumAdmin")
    
# method to submit a quantum job and log data for later retrieving the results 
def runJob(target_name, num_qubits, use_swaps, apply_inverse, shots):
    try: 
        #clean up target name for use in filename
        target_name_formatted = target_name.replace(" ", "_")
        results_filename = f'aws_{target_name_formatted}.csv'
        error_filename = f'aws_{target_name_formatted}_errors.txt'
        results_path = os.path.join(common.data_directory, results_filename) 
        error_path = os.path.join(common.data_directory, error_filename) 

        provider = BraketProvider()
        backend = provider.get_backend(target_name)
        device = backend._aws_device

        # build and transpile the qft circuit
        # aws code will transpile the circuit
        circuit, common_basis_set_metrics, transpiled_for_backend_metrics = common.build_qft_circuit(num_qubits=num_qubits, backend=backend, shots=shots, do_transpile=False, use_swaps=use_swaps, apply_inverse=apply_inverse)

        job_id=None
        submission_date=None
        queue_depth=None
        queue_position=None

        if device.status.lower() == "offline":
            status = "Unavailable"
        else:
            status = "Submitted"
            job = backend.run(circuit, shots=shots)
            job_id = job._job_id
            submission_date = job._date_of_creation
            queue_depth = device.queue_depth().quantum_tasks
            queue_position = job.queue_position().queue_position

        results = [dt.datetime.now(tz=dt.timezone.utc), 
                   job_id, 
                   circuit.name, 
                   target_name, 
                   device.status, 
                   num_qubits, 
                   submission_date, 
                   status, 
                   queue_depth, 
                   queue_position]
        results += common_basis_set_metrics
        results += transpiled_for_backend_metrics
        common.write_results_to_csv(results_path, results, header)
    except Exception as e:
        with open(error_path, "a+") as file:
            file.write(f'{dt.datetime.now(tz=dt.timezone.utc)} {e} \n')
            # f formats the string
 
 
if __name__ == '__main__':
    args = common.get_args()
    runJob(target_name=args.target, num_qubits=args.qubits, use_swaps=args.doswaps, apply_inverse=args.doinverse, shots=args.shots)

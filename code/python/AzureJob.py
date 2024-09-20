import os
import datetime as dt
import common
from azure.identity import DefaultAzureCredential

# launching job reference for later, getting results later
 
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider 

token = DefaultAzureCredential()

header = ["Current Time", "Job ID", "Circuit", "Target", "Target Status", "Number of Qubits", "Submission Time", "Submission Status", "Average Queue Time",
          "Common Basis Depth", "Common Basis Size", "Common Basis Xi","Common Basis n1q", "Common Basis n2q", 
          "Depth", "Size", "Xi", "n1q", "n2q"]  #add others

quantinuum_id = os.getenv("AZURE_QUANTUM_RESOURCE_ID_QUANTINUUM") 
seqcure_id = os.getenv("AZURE_QUANTUM_RESOURCE_ID")
location = os.getenv("AZURE_QUANTUM_LOCATION") 


# method to submit a quantum job and log data for later retrieving the results 
def runJob(target_name, num_qubits, shots, use_swaps, apply_inverse):


    try: 
        #clean up target name for use in filename
        target_name_formatted = target_name.replace(" ", "_")
        results_filename = f'azure_{target_name_formatted}.csv'
        error_filename = f'azure_{target_name_formatted}_errors.txt'
        results_path = os.path.join(common.data_directory, results_filename) 
        error_path = os.path.join(common.data_directory, error_filename) 

        # create Azure Quantum Provider 
        resource_id = quantinuum_id if "quantinuum".lower() in target_name.lower() else seqcure_id
        workspace = Workspace(  
            resource_id = resource_id,
            location = location 
        )
        provider = AzureQuantumProvider(workspace)
        backend = provider.get_backend(target_name)

        # if ionq simulator - enable araia noise model
        if "ionq.simulator" in target_name.lower():
            option_params = {
                "noise": {
                    "model": "aria-1",   # targets the Aria quantum computer
                }
            }
            backend.options.update_options(**option_params)


        # build and transpile the qft circuit
        circuit, common_basis_set_metrics, transpiled_for_backend_metrics = common.build_qft_circuit(num_qubits=num_qubits, shots=shots, backend=backend, use_swaps=use_swaps, apply_inverse=apply_inverse, do_transpile=True)

        # get availability info and queue time for this target
        workspace_targets = provider.get_workspace().get_targets()
        azure_target = next((x for x in workspace_targets if x.name == target_name), None)
        availability = azure_target.current_availability
        avg_queue_time = azure_target.average_queue_time

        job_id=None
        submission_date=None
        if not backend.status().operational or availability.lower() == "unavailable":
            status = "Unavailable"
        else:
            status = "Submitted"
            job = backend.run(circuit, shots=shots)
            job_id = job.id()
            submission_date = job._azure_job._details.creation_time,

        results = [dt.datetime.now(tz=dt.timezone.utc), 
                   job_id, 
                   circuit.name,
                   target_name, 
                   availability, 
                   num_qubits, 
                   submission_date, 
                   status, 
                   avg_queue_time]
        results += common_basis_set_metrics
        results += transpiled_for_backend_metrics
        common.write_results_to_csv(results_path, results, header)
    except Exception as e:
        with open(error_path, "a+") as file:
            file.write(f'{dt.datetime.now(tz=dt.timezone.utc)} {e} \n')
            # f formats the string
 
 
if __name__ == '__main__':
    args = common.get_args()
    runJob(target_name=args.target, num_qubits=args.qubits, shots=args.shots, use_swaps=args.doswaps, apply_inverse=args.doinverse)

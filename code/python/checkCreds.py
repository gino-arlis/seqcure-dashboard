from qiskit_braket_provider import BraketProvider
from pathlib import Path
import os, boto3
import datetime as dt
from azure.identity import DefaultAzureCredential

from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider 

session = boto3.Session(profile_name="992382759470_BraketQuantumAdmin")
token = DefaultAzureCredential()

quantinuum_id = os.getenv("AZURE_QUANTUM_RESOURCE_ID_QUANTINUUM") 
seqcure_id = os.getenv("AZURE_QUANTUM_RESOURCE_ID")
location = os.getenv("AZURE_QUANTUM_LOCATION") 


data_directory = '/media/seqcuredata/dailyjobs'
# create the folder if it doesn't exist 
if not os.path.exists(data_directory): 
    os.makedirs(data_directory)

def credentials_check():
    # aws provider
    aws_provider = BraketProvider()

    # quantinuum  provider 
    q_workspace = Workspace(  
        resource_id = quantinuum_id,
        location = location 
    )
    q_provider = AzureQuantumProvider(q_workspace)


    # seqcure provider
    s_workspace = Workspace(  
        resource_id = seqcure_id,
        location = location 
    )
    s_provider = AzureQuantumProvider(s_workspace)

    credentials_error_filename = f'credentials_errors.txt'
    error_path = os.path.join(data_directory, credentials_error_filename) 

    for p in [aws_provider, q_provider, s_provider]:
        try:
            print(p.backends())
        except Exception as e:
            with open(error_path, "a+") as file:
                file.write(f'{dt.datetime.now(tz=dt.timezone.utc)} {e} \n')
                # f formats the string

if __name__ == '__main__':
    credentials_check()
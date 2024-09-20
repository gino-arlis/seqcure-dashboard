
import os 
import csv 
from pathlib import Path
import common
import glob
import pandas as pd
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider 
import datetime as dt


"""
for each file in folder, open and read 
go though each variable

#how to pull data that we dont have ex. probability

pull files from this new directory 
/media/seqcuredata/dailyjobs  appending to those files a few times a day 


start w csv files , load into data frame do something like azure and was job script and get backend 
should be get_job_by_id 
may need to look at api documents
google azure function that can retrieve job by id 
look at debug for job and see whats avail 
 
 
plan for what we both can work on, stuff thats common, put in a separate file,



"""
quantinuum_id = os.getenv("AZURE_QUANTUM_RESOURCE_ID_QUANTINUUM") 
seqcure_id = os.getenv("AZURE_QUANTUM_RESOURCE_ID")
location = os.getenv("AZURE_QUANTUM_LOCATION") 



# launching job reference for later, getting results later
 


data_directory = f'{str(Path.home())}/media/seqcuredata/dailyjobs

#backend for azure 

 resource_id = quantinuum_id if "quantinuum".lower() in target_name.lower() else seqcure_id
        workspace = Workspace(  
            resource_id = resource_id,
            location = location 
        )
        provider = AzureQuantumProvider(workspace)
        backend = provider.get_backend(target_name)

filenames = glob.glob(os.)
        

 def read_csv()




    

'


        
        

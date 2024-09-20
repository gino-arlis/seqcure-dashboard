import csv
import os
from pathlib import Path
import pandas as pd 
import common
import glob
from os import listdir
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from qiskit_braket_provider import BraketProvider
from braket.aws import AwsDevice
import datetime as dt
from datetime import datetime, timedelta, date

"""
1. Created the data directory with all the files
2. Get the imports necessary for setting up the provider for AWS and Azure
3. Set up the provider and get the backend for each, by making two separate functions.
Create two read_from_csv functions. 
4. Retrieve the job id with a function such as getjobbyID, etc. May need to research
the API Docs using backend stuff
5. Do additional research on getting results, the count of qubits, probabilities. 
Determining approximate queue time will require some math, as well as determing the success rate 
of all jobs completed. As for availability, find a way to reprsent the jobs that failed, or could 
not submit. Can potentially use views or visualization.
6. Maybe to avoid repeats or old ones, we just have an if statement being like "if not read from csv, then do x"
This all would be done in the individual read_from_csv functions for both AWS and Azure.
SOME ADDITIONAL NOTES:
The Cron scripts append to these files on the schedule. While working on each function, need to note
that the providers and fields of the files of the results are different.
Both will read into separate dataframes, adding name of the file in the beginning and concating dataframes? This can be something to tackle later...such as how to access with
plotlib or using glob to list files...can also maybe make it in the multipage app.
Another issue to tackle later would be only loading the files that are new. We can also find a way 
to access the date of when the file was created, and somehow configure the script to only pull results
from the newest and most recent jobs created. 
After retrieving jobs from backend, we should test it out by debugging to see the job and 
what is in there.
Let's start with the .csv files and then work on the .txt ones later...
We are no longer modifiying the AzureJob and AwsJob scripts."""
"""This goes along with what we were discussing yesterday.  Right now we will "pull the job" for all the ids we have every time it runs.  This is what I meant by wasting time reprocessing. Then based on it's status look at specific data for that job.  examples of items of interest:
if waiting or executing skip to next one - no data to do anything with yet
if done --- get the results (counts and or probabilities), determine approximate queue time, get execution time, etc
if failed -- why?  out of quota, invalid input?  
determine success % of jobs that have completed (not waiting or executing)
availability - how do we show the data for all the jobs that we could not submit"""
# Path to our CSV Files
#data_directory1 = f'{str(Path.home())}/media/seqcuredata/dailyjobs'     # not using 
data_directory= f'/media/seqcuredata/dailyjobs'  
 
#on our VMS the daily jobs file is not from our home directory, its in  "other locations "
#path might be incorrect because we are getting a filenot found error
print(os.listdir(data_directory))
# Environment variables for our workspaces 
quantinuum_id = os.getenv("AZURE_QUANTUM_RESOURCE_ID_QUANTINUUM") 
seqcure_id = os.getenv("AZURE_QUANTUM_RESOURCE_ID")
location = os.getenv("AZURE_QUANTUM_LOCATION")
# Workspaces initially set up for both targets in Azure
workspaceQ = Workspace(  
            resource_id = quantinuum_id,
            location = location 
        )
workspaceS = Workspace(  
            resource_id = seqcure_id,
            location = location 
        )
dataframes_list_azure = []
dataframes_list_aws = []
# filenames gets the list of all the CSV files in this directory
"""filenames_azure = glob.glob(os.path.join(data_directory, '*.csv'))
filenames_aws = glob.glob(os.path.join(data_directory, 'aws*.csv'))
 
print(filenames_azure) #list is empty"""
 
 
os.listdir(data_directory)
 
 
def find_csv_files_with_word(data_directory, suffix = ".csv"):
    filenames =os.listdir(data_directory)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
print(find_csv_files_with_word(data_directory, suffix=".csv"))
csv_files = find_csv_files_with_word(data_directory, suffix=".csv")
 
 
#checking if file is aws or azure 
"""   result1 = []
    for file in csv_files:
        with open(file, 'r') as f:
            content = f.read()
            if word1 in content:
                result1.append(file)"""
 
def get_azure_file(csv_files, word1):
    azure_files = []
    word1= "azure"
    for file in csv_files:
        if word1 in file: 
            azure_files.append(file)
    return azure_files
print("AZURE FILES------------")
print(get_azure_file(csv_files, "azure"))
 
 
def get_aws_file(csv_files, word1):
    aws_files = []
    word1= "aws"
    for file in csv_files:
        if word1 in file: 
            aws_files.append(file)
    return aws_files        

print("AWS FILES------------")
print(get_aws_file(csv_files, "aws"))
 
 
    #return[filename for filename in csv_files if filename in word1

 
     
    #[file for file in data_directory if file.endswith('.csv')]
 
    
    #return result1
#result1 = find_csv_files_with_word(data_directory,"azure")
#print(result1)
 
#another func checking for quant in file loop
def create_azure_dataframe():
    result = get_azure_file(csv_files, "azure") 
    for file in result:
        with open(file, "r") as fileB:
            df = pd.read_csv(fileB)
            for column in df.columns:
                   if "Unavailable" in df.columns.values:
                        df=df.drop(columns=column)
    return df
   # just need to make it, not call it                


# write it inside an exception stuff and find the qiskitbackendfound error, try/catch it 
def read_results_from_csv_azure():
      result1 = get_azure_file(csv_files, "azure")
      #provider = AzureQuantumProvider(workspaceS) #inside , switch workspace , if filename contains "q//" use that workspace, else use seqcure
      for file in result1:
            if "quantinuum" in file:
                 provider =  AzureQuantumProvider(workspaceQ)
            else:
                 provider = AzureQuantumProvider(workspaceS)
            with open(data_directory + "/" + file, "r") as fileA:
         
                print("SUBMISSION STATUS----")
                temp_df_azure = pd.read_csv(fileA)
                submission_status = temp_df_azure["Submission Status"]
                submission_status = list(submission_status)
                print(submission_status)
                job_ids = temp_df_azure['Job ID']
                print("JOB IDS-----")
                print(job_ids)

                     #retrieve job code 
                     # job._azure_job.details to get all the data
                     #time submitted, time executed will give queue time
                     # find the probability ,then the counts, fidelity rate function provided

                dataframes_list_azure.append(temp_df_azure) 
                    # appends into separate dataframe 

            
                target= temp_df_azure.at[0, 'Target']
                backend = provider.get_backend(target) 
              
                job_ids = list(job_ids)
                for job_id in job_ids:
                    job_id = str(job_id)  
                    if len(job_id) > 10:
                        job = backend.retrieve_job(job_id)
                        creation_time = job._azure_job.details.creation_time
                        begin_time = job._azure_job.details.begin_execution_time
                        end_time = job._azure_job.details.end_execution_time
                        # put this code in the try/catch
                        if type(begin_time) is dt.datetime: 
                             queue_time = begin_time - creation_time
                             execution_time = end_time - begin_time

                             temp_df_azure["How Long in Queue"] = queue_time
                             temp_df_azure["Execution Time"] = execution_time
                             # fidelity line here, then add to the dataframe
                        
            for status in submission_status:
                temp_df_azure.drop(temp_df_azure.loc[temp_df_azure["Submission Status"]=="Unavailable"].index, inplace=True)
                        #job.result().get_counts()
                        #print("JOB RESULTS------")
                        #print(job._azure_job.details)
            
                 # all job ids from csv
                #print("-------")
                #print(job_ids)
      final_list_azure = list(dataframes_list_azure)
      final_azure_dataframe = pd.concat(final_list_azure)
      current_time_sorted = final_azure_dataframe.sort_values(by='Current Time', ascending=False)
      
      final_csv_azure = current_time_sorted.to_csv(data_directory + '/' + 'Dashboard_Dataframe_AZURE.csv')
      
      
      print("FINAL LIST-----")
      print(final_list_azure)
   


read_results_from_csv_azure()
 
def read_results_from_csv_aws():
     # differentiate between job and task (submit as quantum task, not as job...)
     result2 = get_aws_file(csv_files, "aws")
     for file in result2: 
        #file_string = str(file)
            provider = BraketProvider()
            #backends = provider.backends()
            #print("BACKENDS------")
            #print(backends)
            with open(data_directory + "/" + file, "r") as fileA:
                temp_df_aws = pd.read_csv(fileA)
                dataframes_list_aws.append(temp_df_aws) # appends into separate dataframe 
                target= temp_df_aws.at[0, 'Target']
                job_ids = temp_df_aws['Job ID'] # all job ids from csv 
                backend = provider.get_backend(target)  # helps us access job_id and other fields
     final_list_aws = list(dataframes_list_aws)
     final_aws_dataframe = pd.concat(final_list_aws)
     current_time_sorted = final_aws_dataframe.sort_values(by='Current Time', ascending=False)
     final_csv_aws = current_time_sorted.to_csv(data_directory + '/' + 'Final_Dataframe_AWS.csv')
     print("FINAL LIST-----")
     print(final_list_aws)  

#read_results_from_csv_aws()    

 



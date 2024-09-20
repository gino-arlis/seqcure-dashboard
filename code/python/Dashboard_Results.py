import csv
import os
from pathlib import Path
import pandas as pd 
import numpy as np
import common
import glob
from os import listdir
import datetime as dt
from datetime import timedelta
import requests
import json
from urllib.request import urlopen
import urllib.request
from qiskit.providers.jobstatus import JobStatus
#from sklearn.linear_model import LinearRegression
#from sklearn.metrics import r2_score
import boto3
from azure.identity import DefaultAzureCredential

from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider

from qiskit.quantum_info.analysis import hellinger_fidelity # for the both of them
 
from qiskit_braket_provider import BraketProvider
 
from braket.aws import AwsDevice, AwsSession, AwsQuantumTask


session = boto3.Session(profile_name="992382759470_BraketQuantumAdmin")
token = DefaultAzureCredential()
 
# Path to our CSV Files
#data_directory1 = f'{str(Path.home())}/media/seqcuredata/dailyjobs'     # not using 
data_directory= f'/media/seqcuredata/dailyjobs'  

#on our VMS the daily jobs file is not from our home directory, its in  "other locations "
#path might be incorrect because we are getting a filenot found error
#print(os.listdir(data_directory))
 
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

# LOADING IDEAL, PERFECT CIRCUIT RESULTS IN JSON FILES. THIS IS THE PATH
#data_path = Path()/'..'/'risc2024'/'Qubit_8_Data.json'
with open('/media/seqcuredata/dailyjobs/Qubit_8_Data.json') as file:
    counts_8 = json.load(file)

with open('/media/seqcuredata/dailyjobs/Qubit_10_Data.json') as file:
    counts_10 = json.load(file)

with open('/media/seqcuredata/dailyjobs/Qubit_12_Data.json') as file:
    counts_12 = json.load(file)

qubit_range = [8,10,12,14,16,18,20,22,24,25,26,28]
inverse_ideal_files = {}
for i in qubit_range:
    with open(f'/media/seqcuredata/dailyjobs/Qubit_{i}_Data_With_Inverse.json') as file:
        inverse_ideal_files[i] =json.load(file)
   
def find_csv_files_with_word(data_directory, suffix = ".csv"):
    filenames =os.listdir(data_directory)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
    

csv_files = find_csv_files_with_word(data_directory, suffix=".csv")


#checking if file is aws or azure 


def get_azure_file(csv_files, word1):
    azure_files = []
    word1= "azure"
    for file in csv_files:
        if word1 in file: 
            azure_files.append(file)
    return azure_files



def get_aws_file(csv_files, word1):
    #add docstring
    aws_files = []
    word1= "aws"
    for file in csv_files:
        if word1 in file: 
            aws_files.append(file)
    return aws_files              


#not using 
def create_azure_dataframe():
    result = get_azure_file(csv_files, "azure") 
    for file in result:
        with open(file, "r") as fileB:
            df = pd.read_csv(fileB)
            for column in df.columns:
                   if "Unavailable" in df.columns.values:
                        df=df.drop(columns=column)
    return df



#azure data is only returining rigetti data because it is the last file for azure.
# the other file data is not being stpred in azuredata
            
def read_results_from_csv_azure():
    #azure_status = pd.DataFrame(columns =["Target Status", "Target", "Job ID"])
    azure_df = pd.DataFrame(columns=[ "Job ID", "Target", 
                             "Number of Qubits","Fidelity", 
                              "Average Queue Time", "Time in Queue",  "Run Time","Execution Time" ,"End Time", "Name"])
    azure_df_fail = pd.DataFrame(columns=["Job ID", "Target", "Submission Time",
                             "Job Status", "Failure Message"])
    azure_df_cost = pd.DataFrame(columns=["Job ID", "Target", "Job Status", "Cost Estimate", "Cost Units", "Fidelity", "Number of Qubits"])

    #making new csv, adding header with the data we want
   
    result1 = get_azure_file(csv_files, "azure")
    for file in result1:
        if "quantinuum" in file:
                 provider = AzureQuantumProvider(workspaceQ)
        else:
                 provider = AzureQuantumProvider(workspaceS)
     
        with open(data_directory + "/" + file, "r") as fileA:
             
            #job id , fidel, target, number of qb, execution, queue time, submission time (time for graphs later), current time
            
            azure_submitted_data = pd.read_csv(fileA)

            #azure_submitted_data.insert(0, "Fidelity Rate", 0) #, pd.Series([0], index=[index]))
            #azure_submitted_data.insert(1, "Execution Time", 0)
            #azure_submitted_data.insert(2, "How Long in Queue", 0)

            target= azure_submitted_data.at[0, 'Target']
           
            backend = provider.get_backend(target) 

            #qpu_status = azure_submitted_data["Target Status"].reset_index()  #add this to failed 

            #dataframes_list_azure.append(azure_submitted_data) 
            for index, row in azure_submitted_data.iterrows():

                submission_status = row["Submission Status"]
                job_id = row['Job ID']
                avg_queue_time = row["Average Queue Time"]
                number_of_qubit = row['Number of Qubits']
                submission_time = row['Submission Time']
                target_status = row['Target Status']
                azure_submitted_data = azure_submitted_data[azure_submitted_data['Submission Status'] == 'Submitted']
                name = row["Circuit"]
            #make csv
            #azure_status.loc[len(azure_status.index)] = [target_status, target, job_id]
            #azure_status_CSV = azure_status.to_csv(data_directory + '/' + 'AZURE_Target_Status.csv')

            #for index, row in azure_submitted_data.iterrows():
                #azure_submitted_data = azure_submitted_data[azure_submitted_data['Submission Status'] == 'Submitted']

                """for status in submission_status:
                    azure_submitted_data.drop(azure_submitted_data.loc[azure_submitted_data['Submission Status']=="Unavailable"].index, inplace=True)"""
            
                #submission_time = dt.datetime(submission_time)
            #calculations  
            #job_ids = list(job_ids)
            #print("job ids =====--" 
                job_id = str(job_id)
                if len(job_id) > 10: 

                    job = backend.retrieve_job(job_id)
                    error = "N/A"
                                #status = str(status)
                    #print(f' The status is {status} for file {file}')
                    if job.status() == JobStatus.DONE:
                        status = job.status()
                        creation_time = job._azure_job.details.creation_time
                        begin_time = job._azure_job.details.begin_execution_time
                        end_time = job._azure_job.details.end_execution_time
                        cost = job._azure_job.details.cost_estimate.estimated_total
                        cost_units = job._azure_job.details.cost_estimate.currency_code
                        if "quantinuum" in target:
                            cost = job._azure_job.details.cost_estimate.events[0].amount_billed * 10.88
                            cost_units = job._azure_job.details.cost_estimate.currency_code
                        if type(begin_time) is dt.datetime and type(end_time) is dt.datetime and type(creation_time) is dt.datetime:
                            execution_time = end_time - begin_time
                           
                            #azure_submitted_data.at[index, 'Execution Time']  = execution_time
                                        #execution_time = list(execution_time)
                            queue_time = begin_time - creation_time
                            timedelta_queue = pd.Timedelta(queue_time)
                            seconds_queue = timedelta_queue.total_seconds()
                            queue_time_hours = seconds_queue / 3600
                            #print(seconds_queue)
                            avg_queue_time_hours = avg_queue_time / 3600
                            #print("AVG QUEUE TIME-----")
                            #print(avg_queue_time_hours)
                            #column_actual_to_numpy = azure_submitted_data['How Long in Queue'].to_numpy()
                            #column_avg_to_numpy = azure_submitted_data['Average Queue Time'].to_numpy()
                            
                            #azure_submitted_data.at[index, 'How Long in Queue']  = queue_time
                                        #queue_time = list(queue_time)
                            run_time = end_time -  creation_time 
                            timedelta_run = pd.Timedelta(run_time)
                            #print(timedelta_run)
                            seconds_run = timedelta_run.total_seconds()
                            run_time_hours = seconds_run / 3600
                            
                            #run_time = end_time - submission_time
                            #azure_submitted_data = azure_submitted_data[azure_submitted_data['Execution Time'] != 0]
                                        #appending new columns. follow fidelity
                            """azure_submitted_data["How Long In Queue"] = queue_time
                                        azure_submitted_data["Execution Time"] = execution_time"""
                                        #check if job has processed, then append only that row 
                            counts_azure = job.result().get_counts()
                                    # if number of qubits[] == 8
                            # ensure that all keys in counts are zero padded to this length
                            padded_counts = {k.zfill(number_of_qubit): v for k, v in counts_azure.items()}   

                        
                            # if "noinverse" in name:
                            #     fidelity = hellinger_fidelity(padded_counts, counts_8)
                            # else:
                            fidelity = hellinger_fidelity(padded_counts, inverse_ideal_files[number_of_qubit])
                          
                            #azure_submitted_data.at[index, 'Fidelity Rate'] = fidelity_8
                            """print("FIDELITY 8 COUNT")
                                        print(fidelity_8)
                                        print("JOB ID----")
                                        print(job_id)
                                        print("FILENAME-----")
                                        print({file})"""
                        # if 10 == number_of_qubit:
                        #     if "noinverse" in name:
                        #         fidelity = hellinger_fidelity(padded_counts, counts_10)
                        #     else:
                        #         fidelity = hellinger_fidelity(padded_counts, counts_10_secret_int_plus_one)
                            #fidelity_10= str(fidelity_10)
                            #azure_submitted_data.at[index, 'Fidelity Rate'] = fidelity_10
                                        #temp_df_azure.insert(0, "Fidelity Rate", pd.Series([fidelity_10], index=[index]))
                            """print("FIDELITY 10 COUNT")
                                        print(fidelity_10)
                                        print("JOB ID----")
                                        print(job_id)
                                        print("FILENAME-----")
                                        print({file})"""
                        # if 12 == number_of_qubit:
                        #     if "noinverse" in name:
                        #         fidelity = hellinger_fidelity(padded_counts, counts_12)
                        #     else:
                        #         fidelity = hellinger_fidelity(padded_counts, counts_12_secret_int_plus_one)
                            #fidelity_12 = str(fidelity_12)
                            #print(type(fidelity_12))
                    
                            #azure_submitted_data.at[index, 'Fidelity Rate'] = fidelity_12
                                        #temp_df_azure.insert(0, "Fidelity Rate", pd.Series([fidelity_12], index=[index]))
                                        #temp_df_azure["Fidelity Rate"] = fidelity_12
                            """  print("FIDELITY 12 COUNT")
                                        print(fidelity_12)
                                        print("JOB ID----")
                                        print(job_id)
                                        print("FILENAME-----")
                                        print({file})"""
                            """ temp_df_azure["Fidelity Rate"] = fidelity_8
                                    temp_df_azure["Fidelity Rate"] = fidelity_10
                                    temp_df_azure["Fidelity Rate"] = fidelity_12"""
                            #sort and write everything to new dataframe
                                    #drop rows where fidelity  = to 0
                #azure_submitted_data.loc[~(azure_submitted_data==0).all(axis=1)]
                                #azure_submitted_data = azure_submitted_data.query("Execution Time == 0 and Fidelity Rate == 0.0" )
                                #if 0 in azure_submitted_data['Execution Time'] and 0.0 in azure_submitted_data["Fidelity Rate"]:
           #   Submission Time", "Job ID", "Target", 
                             #"Number of Qubits","Fidelity", "Execution Time" , 
                        #      "Average Queue Time", "How Long in Queue"
                        
                        azure_df.loc[len(azure_df.index)] = [job_id, 
                                             target, number_of_qubit, fidelity,
                                              avg_queue_time_hours, queue_time_hours,run_time_hours, execution_time, end_time, name]
                        azure_df_fail.loc[len(azure_df_fail.index)] = [job_id, 
                                             target, submission_time, status, error]
                        azure_df_cost.loc[len(azure_df_cost.index)] = [job_id, target, status, cost, cost_units, fidelity, number_of_qubit] 
                    elif job.status() == JobStatus.ERROR:
                            status = job.status()
                            error = job._azure_job.details.error_data
                            azure_df_fail.loc[len(azure_df_fail.index)] = [job_id, 
                                             target, submission_time, status, error]
                            azure_df_cost.loc[len(azure_df_cost.index)] = [job_id, target, status, cost, cost_units, fidelity, number_of_qubit] 
                      
                            
                        

 
        dataframes_list_azure.append(azure_submitted_data) 
        #need this list so azure_submitted_data wouldnt be overwritten each time
    current_time_sorted = azure_df.sort_values(by='End Time', ascending=False)
    final_csv_azure = current_time_sorted.to_csv(data_directory + '/' + 'New_Dashboard_Dataframe_AZURE.csv')

    current_time_sorted_fail = azure_df_fail.sort_values(by='Submission Time', ascending=False)
    final_csv_azure_fail = current_time_sorted_fail.to_csv(data_directory + '/' + 'FAILED_Dashboard_Dataframe_AZURE.csv')
    
    final_csv_azure_cost = azure_df_cost.to_csv(data_directory + '/' + 'COST_Dashboard_Dataframe_AZURE.csv')
   
    #final_azure_dataframe = pd.concat(azure_submitted_data)
    #only showing the last file
    #azure_submitted_data = azure_submitted_data[azure_submitted_data['Execution Time'] != dt.timedelta(0)]
    #azure_submitted_data = azure_submitted_data.dropna(subset=["Execution Time"])
    #print(azure_submitted_data)
                            
                #azure_submitted_data.drop(azure_submitted_data.loc[azure_submitted_data['Fidelity Rate']== 0.0].index, inplace=True)
                               # azure_submitted_data.drop(azure_submitted_data.loc[azure_submitted_data['Execution Time']== 0].index, inplace=True)

    #current_time_sorted = final_azure_dataframe.sort_values(by='Current Time', ascending=False)  
    #df = current_time_sorted[current_time_sorted['Fidelity Rate'] != '0.0'] 
     
    #df2 =  current_time_sorted[current_time_sorted['Execution Time'] != '0']                       
    #current_time_sorted = azure_submitted_data.sort_values(by='Current Time', ascending=False)
    #new_row = current_time_sorted['Current Time'].iloc[0]
    """print("NEW ROW----")
    print(new_row)"""
    #final_csv_azure = df.to_csv(data_directory + '/' + 'Dashboard_Dataframe_AZURE.csv') 
                
           
                
      #provider = AzureQuantumProvider(workspaceS) #inside , switch workspace , if filename contains "q//" use that workspace, else use seqcure
      
#put in outside func
    
    #final_list_azure = list(dataframes_list_azure)
    #final_azure_dataframe = pd.concat(azure_submitted_data)
    # appending new jobs 
    """ if new_row in current_time_sorted['Current Time']:
        new_df = pd.DataFrame([current_time_sorted.iloc[0]])
        current_time_sorted = pd.concat([current_time_sorted, new_df], axis=0, ignore_index=True)"""
    # - 1 thing pulls the first item on the csv with the most current date
    # check if that date matches any other rows in the column...if so then those rows
    # are concatendated 
    # new df could be rows with the same
    # concatendate a new one based on the date 
    
     
read_results_from_csv_azure()

"""def read_azure_csv(path):
     pd.read_csv('/media/seqcuredata/dailyjobs/Dashboard_Dataframe_AZURE.csv')

"""
def read_results_from_csv_aws():
     #new df
     #aws_status = pd.DataFrame(columns =["Target Status", "Target", "Job ID"])
     aws_df = pd.DataFrame(columns=["Job ID", "Target", 
                             "Number of Qubits","Fidelity", "Creation Time", "End Time", "Run Time" , "Name"
                              ])
     aws_df_fail = pd.DataFrame(columns=["Job ID", "Target", 
                             "End Time", "Job Status"
                              ])
     aws_df_cost = pd.DataFrame(columns=["Job ID", "Target", "Job Status", "Cost Estimate", "Cost Units", "Fidelity", "Number of Qubits"])
     result2 = get_aws_file(csv_files, "aws")
     for file in result2: 
        #file_string = str(file)
            provider = BraketProvider()
            #backends = provider.backends()
            #print("BACKENDS------")
            #print(backends)
            with open(data_directory + "/" + file, "r") as fileA:
                temp_df_aws = pd.read_csv(fileA)
                target= temp_df_aws.at[0, 'Target']
                backend = provider.get_backend(target)

                
                for index, row in temp_df_aws.iterrows():
                    submission_status = row["Submission Status"]
                    job_id = row['Job ID']
                    number_of_qubit = row['Number of Qubits']
                    target_status = row['Target Status']
                    temp_df_aws = temp_df_aws[temp_df_aws['Submission Status'] == 'Submitted']
                    name = row["Circuit"]
                #aws_status.loc[len(aws_status.index)] = [target_status, target, job_id]
                #aws_status_CSV = aws_status.to_csv(data_directory + '/' + 'AWS_Target_Status.csv')
                
                #for index, row in temp_df_aws.iterrows():
                    #temp_df_aws = temp_df_aws[temp_df_aws['Submission Status'] == 'Submitted']


                #submission_status = temp_df_aws["Submission Status"]
                
                    dataframes_list_aws.append(temp_df_aws) # appends into separate dataframe 
                
                    job_id = str(job_id)
                    if len(job_id) > 10 and job_id != "nan":
                            
                        job = backend.retrieve_job(job_id)
                        if "DONE" in str(job.status()): 
                                status_job = job.status()
                                #metadata = job.metadata()
                                shots = job._tasks[0]._metadata['shots']
                                cost_units = "USD"
                                if "Aria" in target:
                                    cost_estimate = (shots * 0.03) + 0.30
                                if "Harmony" in target:
                                    cost_estimate = (shots * 0.01) + 0.30
                                if "Garnet" in target:
                                    cost_estimate = (shots * 0.00145) + 0.30
                                if "Ankaa-2" in target:
                                    cost_estimate = (shots * 0.00090) + 0.30    
                                #print("STATUS OF JOB")
                                #print(status_job)
                                #print("JOB") 
                                #print(job)
                                counts_aws = job.result().get_counts()
                                #print("COUNTS")
                                #print(counts_aws)
                                creation_time = job._tasks[0]._metadata["createdAt"] #submission time is same
                               #print("CREATION TIME")
                                #print(creation_time)
                                end_time = job._tasks[0]._metadata["endedAt"]
                                run_time = end_time - creation_time
                                timedelta_run = pd.Timedelta(run_time)
                                #print(timedelta_run)
                                seconds = timedelta_run.total_seconds()
                                run_time_hours = seconds / 3600
                                #print("RUN TIME")
                                #print(run_time)
                               # temp_df_aws["Creation Time"] = creation_time
                                #temp_df_aws["End Time"] = end_time
                                
    
                                # ensure that all keys in counts are zero padded to this length
                                padded_counts = {k.zfill(number_of_qubit): v for k, v in counts_aws.items()}
                                # if 8 == number_of_qubit:
                                #     if "noinverse" in name:
                                #         fidelity = hellinger_fidelity(padded_counts, counts_8)
                                #     else:
                                fidelity = hellinger_fidelity(padded_counts, inverse_ideal_files[number_of_qubit])
                                        # #temp_df_aws["Fidelity Rate"] = fidelity_8
                                
                                        # """
                                        # print("FIDELITY 8 COUNT")
                                        # print(fidelity_8)
                                        # print("JOB ID----")
                                        # print(job_id)
                                        # print("FILENAME-----")
                                        # print({file})"""
                                # elif 10 == number_of_qubit:
                                #     if "noinverse" in name:
                                #         fidelity = hellinger_fidelity(padded_counts, counts_10)
                                #     else:
                                #         fidelity = hellinger_fidelity(padded_counts, counts_10_secret_int_plus_one)
                                #         #temp_df_aws["Fidelity Rate"] = fidelity_10
                                #         """   print("FIDELITY 10 COUNT")
                                #         print(fidelity_10)
                                #         print("JOB ID----")
                                #         print(job_id)
                                #         print("FILENAME-----")
                                #         print({file})"""
                                # elif 12 == number_of_qubit:
                                #     if "noinverse" in name:
                                #         fidelity = hellinger_fidelity(padded_counts, counts_12)
                                #     else:
                                #         fidelity = hellinger_fidelity(padded_counts, counts_12_secret_int_plus_one)
                                #         #temp_df_aws["Fidelity Rate"] = fidelity_12
                                #         """ print("FIDELITY 12 COUNT")
                                #         print(fidelity_12)
                                #         print("JOB ID----")
                                #         print(job_id)
                                #         print("FILENAME-----")
                                #         print({file})"""
                        #temp_df_aws["Counts"] = counts
                        #fidelity stuff 
                                aws_df.loc[len(aws_df.index)] = [job_id, 
                                             target, number_of_qubit, fidelity, creation_time, end_time, run_time_hours, name]
                                aws_df_fail.loc[len(aws_df_fail.index)] = [job_id, 
                                             target, end_time, status_job]
                                
                                aws_df_cost.loc[len(aws_df_cost.index)] = [job_id, target, status_job, cost_estimate, cost_units, fidelity, number_of_qubit] 
                        elif "FAILED" in str(job.status()):
                            status_job = job.status()
                            cost_units = "USD"
                            aws_df_fail.loc[len(aws_df_fail.index)] = [job_id, 
                                             target, end_time, status_job]
                            aws_df_cost.loc[len(aws_df_cost.index)] = [job_id, target, status_job, cost_estimate, cost_units, fidelity, number_of_qubit] 
                                                                      
                     
                                
     
     
   
     #final_list_aws = list(dataframes_list_aws)
     #final_aws_dataframe = pd.concat(final_list_aws)
     current_time_sorted = aws_df.sort_values(by='End Time', ascending=False)
     #new_row = current_time_sorted['Current Time'].iloc[0]
     #print("NEW ROW----")
     #print(new_row)
     """ if new_row in current_time_sorted['Current Time']:
        new_df = pd.DataFrame([current_time_sorted.iloc[0]])
        current_time_sorted = pd.concat([current_time_sorted, new_df], axis=0, ignore_index=True)"""
     final_csv_aws = current_time_sorted.to_csv(data_directory + '/' + 'New_Dashboard_Dataframe_AWS.csv')
    
     current_time_sorted_fail = aws_df_fail.sort_values(by='End Time', ascending=False)
     final_csv_aws_fail = current_time_sorted_fail.to_csv(data_directory + '/' + 'FAILED_Dashboard_Dataframe_AWS.csv')

     final_csv_aws_cost = aws_df_cost.to_csv(data_directory + '/' + 'COST_Dashboard_Dataframe_AWS.csv')

read_results_from_csv_aws()
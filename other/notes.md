


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
Let's start with the .csv files and then work on the .txt ones later
We are no longer modifiying the AzureJob and AwsJob scripts
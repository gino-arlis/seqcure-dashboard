
# Real Time Dashboard For Quantum Information


## Project Description

### This is a real time dashboard that provides information and an analysis on quantum jobs ran on different QPUs through Cloud Providers. This dashboard includes visualizations that help the user analyze trends in quantum information science, such as a fidelity and cost estimates. Using Streamlit, an open-source Python framework, we developed a front-end prototype which acts as an interactive web app.

Using Python and Qiskit, we created a backend script to execute quantum jobs on the QFT Circuit and store the results.

Future work includes implementing HTML and CSS to increase front-end formatting options, and using MongoDB to store results.

Description of Scripts:
AwsJob.py and AzureJob.py build and transpile the QFT Circuit, and write the results to a CSV for each QPU

Dashboard_Results.py retrieves job information from each CSV, calculates additional variables, and stores the combined data to a CSV

Streamlit_Dashboard_Final.py creates the web application with data from Dashboard_Results.py

Qubit JSON files store the counts for each qubit size (8,10,12) for the ideal circuit

## Prerequisites
** Have access to a Virtual Machine that contains the shared drive: /media/seqcuredata/dailyjobs **
1. Install Qiskit, Streamlit, streamlit_option_menu, Plotly Express, Pandas 
2. Activate conda environment by the following command: 
        conda activate qiskitv1

## How to run 

1. Navigate to your working directory
2. Run the app: 
        streamlit run Streamlit_Dashboard_Final.py


## Credits 

Thank you to our faculty mentors Allison Casey, Darrell Teegarden, and Gino Serpa for their assistance on this project.

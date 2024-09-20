#Final streamlit dashboard

import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
#import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import time 
#import matplotlib.pyplot as plt 
import plotly.io as pio
import altair as alt
import statsmodels
#from qiskit import  QuantumRegister, ClassicalRegister, QuantumCircuit
#from babel.numbers import format_currency
#import Dashboard_Results_Azure
# st.selectbox() can be used to select specific vars, col1, col2= st.columns(2) for views  


#import dashboard results azure after finishing 

#page layout 
st.set_page_config(layout="wide", page_title= "SEQCURE Dashboard")


alt.themes.enable("dark") #this is not working

backgroundColor = "#0E1117"

#tab title

col1,col2=st.columns([2,2])
# title between the 2 images 
with col1:
    st.image('/media/seqcuredata/dailyjobs/ARLIS_UMD_PIC.png',width=300,use_column_width='never')
with col2:
    col1, col2, col3 = st.columns(3)   
    with col1:
       st.write(' ')  # Empty placeholder
    with col2:
        st.image('/media/seqcuredata/dailyjobs/seqcure_logo.png',width=200,use_column_width='never')
    with col3:
        st.write(' ')
st.markdown("<h1 style='text-align: center; color: white; white-space: nowrap; margin-top: -130px'>SEQCURE Dashboard</h1>", unsafe_allow_html=True) 
    
#images = ['/media/seqcuredata/dailyjobs/ARLIS_UMD_PIC.png', '/media/seqcuredata/dailyjobs/seqcure_logo.png']
#st.image(images, width = 200)
#st.image('/media/seqcuredata/dailyjobs/ARLIS_UMD_PIC.png', '/media/seqcuredata/dailyjobs/seqcure_logo.png', width = 300)
#st.image('/media/seqcuredata/dailyjobs/seqcure_logo.png', width = 300)
#st.title("SEQCURE Dashboard")
#st.markdown("<h1 style='text-align: center; color: white;'>SEQCURE Dashboard</h1>", unsafe_allow_html=True)




#sidebar menu 

#home - guiding user 
#with st.sidebar:
choice = option_menu( menu_title= None, 
                          options=["Home", "Azure","AWS"], 
                          orientation="horizontal",styles={

"nav-link-selected": {"background-color": "#43a2ca"}, 
   }
)

#LOAD DATA HERE----- 

#azure_data = Dashboard_Results_Azure.read_azure_csv('/media/seqcuredata/dailyjobs/Dashboard_Dataframe_AZURE.csv')
azure_data = pd.read_csv('/media/seqcuredata/dailyjobs/New_Dashboard_Dataframe_AZURE.csv') 
aws_data = pd.read_csv('/media/seqcuredata/dailyjobs/New_Dashboard_Dataframe_AWS.csv')
azure_data_fail = pd.read_csv('/media/seqcuredata/dailyjobs/FAILED_Dashboard_Dataframe_AZURE.csv')
aws_data_fail = pd.read_csv('/media/seqcuredata/dailyjobs/FAILED_Dashboard_Dataframe_AWS.csv')
azure_data_cost = pd.read_csv('/media/seqcuredata/dailyjobs/COST_Dashboard_Dataframe_AZURE.csv')
aws_data_cost = pd.read_csv('/media/seqcuredata/dailyjobs/COST_Dashboard_Dataframe_AWS.csv')
#removing column with the index number from each file
removed_column = azure_data.columns[0]
azure_data = azure_data.drop(columns=[removed_column])

removed_column2 = aws_data.columns[0]
aws_data = aws_data.drop(columns=[removed_column2])
#  #for now , circuit qft is same , can add caption can put link to qedc , info on cron

for index, row in azure_data_cost.iterrows():
    azure_data_cost = azure_data_cost[azure_data_cost['Job Status'] == 'JobStatus.DONE']

for index, row in aws_data_cost.iterrows():
    aws_data_cost = aws_data_cost[aws_data_cost['Job Status'] == 'JobStatus.DONE']



if choice == "Home":
    col1, col2, col3 = st.columns(3)
    #maybe an about section?
    with col1:
        with st.container(border=True):
            st.header('Information on QPUs')
            st.image('/media/seqcuredata/dailyjobs/Slide1(2).PNG', width = 350)
            status_azure = pd.read_csv('/media/seqcuredata/dailyjobs/AZURE_Target_Status.csv')
            status_aws = pd.read_csv('/media/seqcuredata/dailyjobs/AWS_Target_Status.csv')
            frames = [status_azure, status_aws]
            both_provider_status = pd.concat(frames)

            both_provider_status = both_provider_status[["Target", "Target Status"]]
            both_provider_status.rename(columns = {"Target": "QPU", "Target Status": "QPU Status"}, inplace = True)
            both_provider_status["Number of Qubits QPU"] = ["25", "25", "11", "29", "20", "56", "84", "25", "25", "80", "20", "11"]
            both_provider_status["Provider"]= ["Azure", "Azure", "Azure", "Azure", "Azure", "Azure", "Azure", "AWS", "AWS", "AWS", "AWS", "AWS"]
            #st.header("Current QPU Status")
            st.dataframe(both_provider_status, hide_index = True, use_container_width = True)

        # Create a DataFrame
       

        


      

    with col2:
        # with st.container(border=True):
            # st.header('Failure Rate VS QPUs')
            # azure_data_fail['Failure Message'] = azure_data_fail['Failure Message'].str.split('orthogonal').str[0]
            # azure_data_fail['Failure Message'] = azure_data_fail['Failure Message'].str.split('{},').str[1]
            # count_df = azure_data_fail.groupby("Target")["Job ID"].count().reset_index().rename(mapper = {"Job ID":"num_total_jobs"}, axis  = 1)
            # #counts of total failures
            # failure_df = azure_data_fail.groupby("Target")["Job Status"].apply(lambda x: (x == "JobStatus.ERROR").sum()).reset_index().rename(mapper = {"Job Status":"num_failed_jobs"}, axis  = 1)
            # # counts of failures by type
            # error_df = azure_data_fail.groupby(["Target", "Failure Message"])["Job ID"].count().reset_index().rename(mapper = {"Job ID":"error_count"}, axis  = 1)
            # merged_df = error_df.merge(count_df).merge(failure_df)
    
            # #get proportions
            # merged_df["failure_rate"] = (merged_df["num_failed_jobs"] / merged_df["num_total_jobs"])*100
            # #use this  for y 
            # merged_df["error_rate"] = merged_df["failure_rate"] * (merged_df["error_count"] / merged_df["num_failed_jobs"])
            # merged_df["Failure Message"] = merged_df["Failure Message"].astype(str)
            # substring = 'NotEnoughQuota'
            # filter = merged_df['Failure Message'].str.contains(substring)
            # merged_df = merged_df[~filter]
            
            # #plotting --------
            # merged_df.loc[merged_df['Failure Message'].str.contains("'400', 'message': '81 - Duplicate job id'", na=False), 'Failure Message'] = 'Duplicate Job ID'
            # merged_df.loc[merged_df['Failure Message'].str.contains("'InvalidInputData'", na=False), 'Failure Message'] = 'Invalid Input Data'
            # merged_df.loc[merged_df['Failure Message'].str.contains("'TransientFailure'", na=False), 'Failure Message'] = 'Transient Failure'


            # fig = px.bar(merged_df, x= "Target", y="error_rate", color = "Failure Message", barmode= "stack",
            #              color_discrete_sequence=px.colors.qualitative.D3)
            # fig.update_layout(showlegend =True, yaxis_title = "Failure Rate (%)", xaxis_title = "QPUs With Failed Runs", legend_title_text = "Error") 

            # merged_df["Failure Message"] = merged_df['Failure Message'].astype(str)
            #cutting out the message after
            # legend_labels = {subcategory: subcategory.split(", '")[0] for subcategory in merged_df['Failure Message'].unique()}
            
            # # Update the legend 
            # for trace in fig.data:
            #     trace.name = legend_labels.get(trace.name, trace.name)

            # fig
    #time plot here, choose the provider 
        with st.container(border= True):
            azure_tomerge = azure_data [["Job ID", "Target", "Number of Qubits", "Fidelity", "End Time", "Name"]]

            aws_tomerge = aws_data[["Job ID", "Target", "Number of Qubits", "Fidelity", "End Time", "Name"]]


            frames = [azure_tomerge, aws_tomerge]
            both_provider_data = pd.concat(frames)
            both_provider_data["Target"] = both_provider_data["Target"].astype(str)
            
            st.header("QFT Fidelity VS Date")
            # option = st.selectbox( "QPU",
            #                         ('ionq.qpu', 'rigetti.qpu.ankaa-2' ,'quantinuum.qpu.h2-1', 'ionq.qpu.aria-2',
            # 'quantinuum.qpu.h1-1', 'Harmony', 'Garnet', 'Aria 2'))
            option = st.selectbox("QPU",
                                    (both_provider_data["Target"].unique()))
            # option2 = st.selectbox("Cicuit",
            #                         (both_provider_data["Name"].unique()))
            option3 = st.selectbox("Number of Qubits",
                                    (both_provider_data["Number of Qubits"].unique()))
    
            # both_filtered = both_provider_data.loc[both_provider_data['Target'].str.contains(option) &
            #                                        both_provider_data['Name'].str.contains(option2) &
            #                                        both_provider_data['Number of Qubits'] == option3]
            # if option == "ionq.qpu":  
            both_filtered = both_provider_data[both_provider_data['Target'].str.contains(option)]
            print(both_filtered)
            # both_filtered = both_filtered[both_filtered['Name'].str.contains(option2)]
            both_filtered = both_filtered[both_filtered['Number of Qubits'] == option3]
            print(both_filtered)
            fig= px.scatter(both_filtered, x = "End Time", y ="Fidelity", color = "Number of Qubits",facet_col="Number of Qubits")
            fig.update_layout(xaxis_title = "Date")
            fig.update_layout(showlegend = False)
            fig
            # if option == 'rigetti.qpu.ankaa-2':  
            #         both_filtered = both_provider_data[both_provider_data['Target'].str.contains('rigetti.qpu.ankaa-2')]
            #         fig= px.line(both_filtered, x = "End Time", y ="Fidelity",
                    
            #         color = "Number of Qubits",facet_col="Number of Qubits")
            #         fig.update_layout(xaxis_title = "Date")
            #         fig.update_layout(showlegend = False)
            #         fig
            # if option == 'quantinuum.qpu.h2-1':  
            #         both_filtered = both_provider_data[both_provider_data['Target'].str.contains('quantinuum.qpu.h2-1')]
            #         fig= px.line(both_filtered, x = "End Time", y ="Fidelity",
                    
            #         color = "Number of Qubits",facet_col="Number of Qubits")
            #         fig.update_layout(xaxis_title = "Date")
            #         fig.update_layout(showlegend = False)
            #         fig 
            # if option == 'ionq.qpu.aria-2':  
            #         both_filtered = both_provider_data[both_provider_data['Target'].str.contains('ionq.qpu.aria-2')]
            #         fig= px.line(both_filtered, x = "End Time", y ="Fidelity",
                    
            #         color = "Number of Qubits",facet_col="Number of Qubits")
            #         fig.update_layout(xaxis_title = "Date")
            #         fig.update_layout(showlegend = False)
            #         fig
            # if option == 'quantinuum.qpu.h1-1':  
            #         both_filtered = both_provider_data[both_provider_data['Target'].str.contains('quantinuum.qpu.h1-1')]
            #         fig= px.line(both_filtered, x = "End Time", y ="Fidelity",
                    
            #         color = "Number of Qubits",facet_col="Number of Qubits")
            #         fig.update_layout(xaxis_title = "Date")
            #         fig.update_layout(showlegend = False)
            #         fig
            # if option == 'Harmony':  
            #         both_filtered = both_provider_data[both_provider_data['Target'].str.contains('Harmony')]
            #         fig= px.line(both_filtered, x = "End Time", y ="Fidelity",
                    
            #         color = "Number of Qubits",facet_col="Number of Qubits")
            #         fig.update_layout(xaxis_title = "Date")
            #         fig.update_layout(showlegend = False)
            #         fig        
            # if option == 'Garnet':  
            #         both_filtered = both_provider_data[both_provider_data['Target'].str.contains('Garnet')]
            #         fig= px.line(both_filtered, x = "End Time", y ="Fidelity",
                    
            #         color = "Number of Qubits",facet_col="Number of Qubits")
            #         fig.update_layout(xaxis_title = "Date")
            #         fig.update_layout(showlegend = False)
            #         fig
            # if option == 'Aria 2':  
            #         both_filtered = both_provider_data[both_provider_data['Target'].str.contains('Aria 2')]
            #         fig= px.line(both_filtered, x = "End Time", y ="Fidelity",
                    
            #         color = "Number of Qubits",facet_col="Number of Qubits")
            #         fig.update_layout(xaxis_title = "Date")
            #         fig.update_layout(showlegend = False)
            #         fig



    with st.container(border=True):
        st.header("Cost vs. Fidelity")
        st.write("Displays the cost trend compared to fidelity for QPUs on all the providers.")
        removed_column_cost = azure_data_cost.columns[0]
        azure_data_cost = azure_data_cost.drop(columns=[removed_column_cost])

        removed_column2_cost = aws_data_cost.columns[0]
        aws_data_cost = aws_data_cost.drop(columns=[removed_column2_cost])
        # merge the fidelities from the aws data and azure data together 
        # merge the cost estimates from 
        # add the fidelity from the aws data and azure data dataframe into 

    
       
        azure_merge = azure_data_cost[["Target", "Number of Qubits", "Fidelity", "Cost Estimate"]]
        aws_merge = aws_data_cost[["Target", "Number of Qubits", "Fidelity", "Cost Estimate"]]

        dataframe = [azure_merge, aws_merge]

        both_provider_data = pd.concat(dataframe)
        both_provider_data["Number of Qubits"] = both_provider_data["Number of Qubits"].astype(str)

        option = st.selectbox( "Qubit Size",
                                    ("8", "10","12"))
        if option == "8":
            both_filtered_scatter = both_provider_data[both_provider_data['Number of Qubits'].str.contains('8')]

        #size_map = {'ionq.qpu': 20, 'ionq.qpu.aria-2': 30, 'ionq.qpu': 15, 'quantinuum.qpu.h1-1': 35, 'quantinuum.qpu.h2-1': 55, 'rigetti.qpu.ankaa-2': 60}
        #both_provider_data['size'] = both_provider_data['Target'].map(size_map)
        #both_provider_data['size'] = [20, 30, 15, 35, 55, 60]
            both_filtered_scatter['size'] = (both_filtered_scatter['Cost Estimate'] - both_filtered_scatter['Cost Estimate'].min()) / (both_filtered_scatter['Cost Estimate'].max() - both_filtered_scatter['Cost Estimate'].min()) * 50 + 10
            fig = px.scatter(both_filtered_scatter, x = 'Cost Estimate', y = 'Fidelity', color = 'Target', size = 'size')
        #fig.update_traces(marker=dict(size=30))
            fig.update_xaxes(type='log', title = "Cost Total [in log scale]")
            fig 
        if option == "10":
            both_filtered_scatter = both_provider_data[both_provider_data['Number of Qubits'].str.contains('10')]

        #size_map = {'ionq.qpu': 20, 'ionq.qpu.aria-2': 30, 'ionq.qpu': 15, 'quantinuum.qpu.h1-1': 35, 'quantinuum.qpu.h2-1': 55, 'rigetti.qpu.ankaa-2': 60}
        #both_provider_data['size'] = both_provider_data['Target'].map(size_map)
        #both_provider_data['size'] = [20, 30, 15, 35, 55, 60]
            both_filtered_scatter['size'] = (both_filtered_scatter['Cost Estimate'] - both_filtered_scatter['Cost Estimate'].min()) / (both_filtered_scatter['Cost Estimate'].max() - both_filtered_scatter['Cost Estimate'].min()) * 50 + 10
            fig = px.scatter(both_filtered_scatter, x = 'Cost Estimate', y = 'Fidelity', color = 'Target', size = 'size')
        #fig.update_traces(marker=dict(size=30))
            fig.update_xaxes(type='log', title = "Cost Total [in log scale]")
            fig 
        if option == "12":
            both_filtered_scatter = both_provider_data[both_provider_data['Number of Qubits'].str.contains('12')]

        #size_map = {'ionq.qpu': 20, 'ionq.qpu.aria-2': 30, 'ionq.qpu': 15, 'quantinuum.qpu.h1-1': 35, 'quantinuum.qpu.h2-1': 55, 'rigetti.qpu.ankaa-2': 60}
        #both_provider_data['size'] = both_provider_data['Target'].map(size_map)
        #both_provider_data['size'] = [20, 30, 15, 35, 55, 60]
            both_filtered_scatter['size'] = (both_filtered_scatter['Cost Estimate'] - both_filtered_scatter['Cost Estimate'].min()) / (both_filtered_scatter['Cost Estimate'].max() - both_filtered_scatter['Cost Estimate'].min()) * 50 + 10
            fig = px.scatter(both_filtered_scatter, x = 'Cost Estimate', y = 'Fidelity', color = 'Target', size = 'size')
        #fig.update_traces(marker=dict(size=30))
            fig.update_xaxes(type='log', title = "Cost Total [in log scale]")
            fig 
        
      

   
    with col3:
        with st.container(border=True):
            st.header('Total Cost per QPU Azure')
            #azure_data_cost['Cost Estimate'] = azure_data_cost['Cost Estimate'].apply(lambda x: "${:,.2f}".format(x))
            total_all = azure_data_cost['Cost Estimate'].sum()
            filtered_azure_ionq = azure_data_cost[azure_data_cost['Target'].str.contains('ionq')] 
            total_ionq = filtered_azure_ionq['Cost Estimate'].sum()
            filtered_azure_quantinuum = azure_data_cost[azure_data_cost['Target'].str.contains('quantinuum')]
            total_quantinuum = filtered_azure_quantinuum['Cost Estimate'].sum() 
            filtered_azure_rigetti = azure_data_cost[azure_data_cost['Target'].str.contains('rigetti')]
            total_rigetti = filtered_azure_rigetti['Cost Estimate'].sum()

            def plot_graph_all():
                
                fig = px.bar(azure_data_cost, x = 'Target', y = 'Cost Estimate', color = 'Target', color_discrete_sequence=["#7b3294", "#e66101","#f1b6da", "#4dac26","#92c5de" , "#dfc27d"])
                fig.update_yaxes(type='log', title = "Cost Estimate [in log scale]")
                fig.update_layout(showlegend=False)

                fig
            def plot_graph_trapped_ion():
                merged_df = pd.concat([filtered_azure_ionq, filtered_azure_quantinuum], ignore_index=True, sort=False)
                fig = px.bar(merged_df, x = 'Target', y = 'Cost Estimate', color = 'Target', color_discrete_sequence=["#7b3294", "#e66101","#f1b6da", "#4dac26","#92c5de" , "#dfc27d"], 
                )
                fig.update_yaxes(type='log', title = "Cost Estimate [in log scale]")
                fig.update_xaxes(title = "QPU")
                fig.update_layout(showlegend=False)

                fig 
            def plot_graph_superconducting():
                filtered_azure = azure_data_cost[azure_data_cost['Target'].str.contains('rigetti')]
                
                fig = px.bar(filtered_azure, x = 'Target', y = 'Cost Estimate', color = 'Target', color_discrete_sequence=["#7b3294", "#e66101","#f1b6da", "#4dac26","#92c5de" , "#dfc27d"])
                fig.update_yaxes(type='log', title = "Cost Estimate [in log scale]")
                fig.update_layout(showlegend=False)
                fig 
            rounded_total_all = round(total_all, 2)
            rounded_total_trapped_ion = round((total_ionq + total_quantinuum), 2)
            rounded_total_superconducting = round(total_rigetti, 2)
            genre = st.radio(
            "Select the type of quantum computer:",
            ["***All***", "***Trapped Ion***", "***Superconducting***"],
            captions=[
                "Total Cost: " + "$" + str(rounded_total_all),
                "Total Cost: " + "$" + str(rounded_total_trapped_ion),
                "Total Cost: " + "$" + str(rounded_total_superconducting),
            ],
        )
            st.write("Quantinuum costs had to be allocated, based on a monthly subscription. Cost is in terms of hardware quantum credit.")
            if genre == "***All***":
                plot_graph_all()
            elif genre == "***Trapped Ion***":
                plot_graph_trapped_ion()  
            elif genre == "***Superconducting***":
                plot_graph_superconducting()
        

            st.header('Total Cost per QPU AWS')
            def aws_plot_graph_all():
                fig = px.bar(aws_data_cost, x = 'Target', y = 'Cost Estimate', color = 'Target', color_discrete_sequence=["#4dac26","#92c5de" , "#dfc27d"])
                fig.update_yaxes(type='linear', title = "Cost Estimate [in linear scale]")
                fig.update_layout(showlegend=False)

                fig
            aws_total_all = aws_data_cost['Cost Estimate'].sum()
            filtered_aws_aria = aws_data_cost[aws_data_cost['Target'].str.contains('Aria 2')] 
            total_aria = filtered_aws_aria['Cost Estimate'].sum()
            filtered_aws_harmony = aws_data_cost[aws_data_cost['Target'].str.contains('Harmony')]
            total_harmony = filtered_aws_harmony['Cost Estimate'].sum() 
            filtered_aws_garnet = aws_data_cost[aws_data_cost['Target'].str.contains('Garnet')]
            total_garnet = filtered_aws_garnet['Cost Estimate'].sum()

            def aws_plot_graph_trapped_ion():
                merged_df = pd.concat([filtered_aws_aria, filtered_aws_harmony], ignore_index=True, sort=False)
                fig = px.bar(merged_df, x = 'Target', y = 'Cost Estimate', color = 'Target', color_discrete_sequence=["#7b3294", "#e66101","#f1b6da", "#4dac26","#92c5de" , "#dfc27d"], 
                )
                fig.update_yaxes(type='linear', title = "Cost Estimate [in linear scale]")
                fig.update_xaxes(title = "QPU")
                fig.update_layout(showlegend=False)

                fig 

            def aws_plot_graph_superconducting():
            
                fig = px.bar(filtered_aws_garnet, x = 'Target', y = 'Cost Estimate', color = 'Target', color_discrete_sequence=["#7b3294", "#e66101","#f1b6da", "#4dac26","#92c5de" , "#dfc27d"], 
                )
                fig.update_yaxes(type='linear', title = "Cost Estimate [in linear scale]")
                fig.update_xaxes(title = "QPU")
                fig.update_layout(showlegend=False)

                fig 
            
            rounded_total_all_aws = round(aws_total_all, 2)
            rounded_total_trapped_ion_aws = round((total_aria + total_harmony), 2)
            rounded_total_superconducting_aws = round(total_garnet, 2)

            genre = st.radio(
            "Both Azure and AWS run jobs via IonQ.",
            ["***All***", "***Trapped Ion***", "***Superconducting***"],
            captions=[
                "Total Cost: " + "$" + str(rounded_total_all_aws),
                "Total Cost: " + "$" + str(rounded_total_trapped_ion_aws),
                "Total Cost: " + "$" + str(rounded_total_superconducting_aws),
            ],
        )
            
            if genre == "***All***":
                aws_plot_graph_all()
            elif genre == "***Trapped Ion***":
                aws_plot_graph_trapped_ion()  
            elif genre == "***Superconducting***":
                aws_plot_graph_superconducting()




    
#AZURE PAGE--------

if choice == "Azure": 
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.header("Azure Job Data") 

            #drop down to filter data by the target
            targets = azure_data["Target"].unique()
            azure_select_target = st.multiselect("Filter by Quantum Processing Unit (QPU)",targets )
            if azure_select_target:
                filtered_azure = azure_data[azure_data["Target"].isin(azure_select_target)]
            else: 
                filtered_azure = azure_data
            st.write(filtered_azure)

        with st.container(border=True):
        #TIME CORRELATION PLOT 
        #color_continuous_scale = "rdylgn"
        #calculate time difference 
            time_diff = azure_data["Time in Queue"] - azure_data["Average Queue Time"]
            #actual - reported
            azure_data["time_diff"] = time_diff
            azure_data['Time Difference'] = azure_data['time_diff'].apply(lambda x: 'Took Longer Than Predicted'if x > 0 else 'Took Less Than Predicted')
            
                 
            
            fig = px.scatter(azure_data, x = "Time in Queue", 
                            y = "Average Queue Time", color = "Time Difference", log_y=True,title = "Average Queue Time (Reported) VS Actual Queue Time",
                            color_discrete_map={'Took Longer Than Predicted': "red", "Took Less Than Predicted":"blue"}
                            )
            fig.update_xaxes(title = "Time in Queue (Hours)") 
            fig.update_yaxes(title = "Average Queue Time (Hours)")
            fig.update_layout(legend_title_text = " ")
            fig 

        
 
    with col2:
        with st.container(border=True):
            azure_data

            option = st.selectbox( "QPU",
                                    ("All", "ionq.qpu.aria-1", "ionq.simulator","ionq.qpu.aria-2",
                                        "rigetti.qpu.ankaa-2", "quantinuum.qpu.h1-1","quantinuum.qpu.h2-1" ))
            if option == "All":
                fig= px.box(azure_data, x = "Number of Qubits",
                    y ="Fidelity", title = "QFT Fidelity VS Number of Qubits (Azure)",
                        color = "Number of Qubits",
                        category_orders={"Number of Qubits": [8,10,12]}, color_discrete_sequence=["#66c2a5", "#fc8d62", "#8da0cb"]
                        )
                fig
            if option == "ionq.qpu.aria-1":  
                    filtered_azure = azure_data[azure_data['Target'].str.contains('ionq.qpu.aria-1')]
                    fig= px.box(filtered_azure, x = "Number of Qubits",
                    y ="Fidelity", title = "QFT Fidelity VS Number of Qubits (Azure)",
                        color = "Number of Qubits",
                        category_orders={"Number of Qubits": [8,10,12]}, color_discrete_sequence=["#66c2a5", "#fc8d62", "#8da0cb"]
                        )
                    fig
            if option == "ionq.simulator":
                    filtered_azure = azure_data[azure_data['Target'].str.contains('ionq.simulator')]
                    fig= px.box(filtered_azure, x = "Number of Qubits",
                    y ="Fidelity", title = "QFT Fidelity VS Number of Qubits (Azure)",
                        color = "Number of Qubits",
                        category_orders={"Number of Qubits": [8,10,12]}, color_discrete_sequence=["#66c2a5", "#fc8d62", "#8da0cb"])
                    fig
            if option == "ionq.qpu.aria-2":
                    filtered_azure = azure_data[azure_data['Target'].str.contains('ionq.qpu.aria-2')]
                    fig= px.box(filtered_azure, x = "Number of Qubits",
                    y ="Fidelity", title = "QFT Fidelity VS Number of Qubits (Azure)",
                        color = "Number of Qubits",
                        category_orders={"Number of Qubits": [8,10,12]}, color_discrete_sequence=["#66c2a5", "#fc8d62", "#8da0cb"])
                    fig
            if option == "rigetti.qpu.ankaa-2":
                    filtered_azure = azure_data[azure_data['Target'].str.contains('rigetti.qpu.ankaa-2')]
                    fig= px.box(filtered_azure, x = "Number of Qubits",
                    y ="Fidelity", title = "QFT Fidelity VS Number of Qubits (Azure)",
                        color = "Number of Qubits",
                        category_orders={"Number of Qubits": [8,10,12]}, color_discrete_sequence=["#66c2a5", "#fc8d62", "#8da0cb"])
                    fig
            if option == "quantinuum.qpu.h1-1":
                    filtered_azure = azure_data[azure_data['Target'].str.contains('quantinuum.qpu.h1-1')]
                    fig= px.box(filtered_azure, x = "Number of Qubits",
                    y ="Fidelity", title = "QFT Fidelity VS Number of Qubits (Azure)",
                        color = "Number of Qubits",
                        category_orders={"Number of Qubits": [8,10,12]}, color_discrete_sequence=["#66c2a5", "#fc8d62", "#8da0cb"])
                    fig
            if option == "quantinuum.qpu.h2-1":
                    filtered_azure = azure_data[azure_data['Target'].str.contains('quantinuum.qpu.h2-1')]
                    fig= px.box(filtered_azure, x = "Number of Qubits",
                    y ="Fidelity", title = "QFT Fidelity VS Number of Qubits (Azure)",
                        color = "Number of Qubits",
                        category_orders={"Number of Qubits": [8,10,12]}, color_discrete_sequence=["#66c2a5", "#fc8d62", "#8da0cb"])
                    fig
        
          
    #another graph
           
            #azure_data["Average Queue Time"]= azure_data["Average Queue Time"].div(3600)
        with st.container(border=True):
                fig = px.box(azure_data , x= "Target", y = "Average Queue Time",title = "Average Queue Time VS QPU",
                    color = 'Target', 
                    color_discrete_sequence=["#7b3294", "#e66101","#f1b6da", "#4dac26","#92c5de" , "#dfc27d"])
                fig.update_layout(showlegend=False, yaxis_title = "Average Queue Time (Hours)")
                fig.update_xaxes(title = "QPU")
                
                fig
        with st.container(border=True):
            fig = px.box(azure_data, x= "Target", y = "Run Time",
            title = "Run Time (Queue Time + Execution Time) VS QPU",
            color = 'Target', color_discrete_sequence=["#7b3294", "#e66101","#f1b6da", "#4dac26","#92c5de" , "#dfc27d"])
            fig.update_yaxes(title = "Run Time (Hours)")
            fig.update_xaxes(title = "QPU")
            fig.update_layout(showlegend=False)

            fig 



if choice == "AWS":
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
   # for seconds in range(3600):
        #st.dataframe(azure_data, use_container_width= True)
            st.header("AWS Job Data") #change this 

            #drop down to filter data by the target
            targets = aws_data["Target"].unique()
            aws_select_target = st.multiselect("Filter by QPU",targets )
            if aws_select_target:
                filtered_aws = aws_data[aws_data["Target"].isin(aws_select_target)]
            else: 
                filtered_aws = aws_data
            st.write(filtered_aws)
        
        #highlight the highest fidelity 
        #time.sleep(1)
    with col2: 
        with st.container(border=True):

            option = st.selectbox( "QPU",
                                    ("All", "Aria 2", "Garnet","Harmony",
                                        ))
            if option == "All":
                fig= px.box(aws_data, x = "Number of Qubits",
                    y ="Fidelity", title = "QFT Fidelity VS Number of Qubits",
                        color = "Number of Qubits",
                        category_orders={"Number of Qubits": [8,10,12]}, color_discrete_sequence=["#66c2a5", "#fc8d62", "#8da0cb"]
                        )
                fig
            if option == "Aria 2":  
                    filtered_aws = aws_data[aws_data['Target'].str.contains('Aria 2')]
                    fig= px.box(filtered_aws, x = "Number of Qubits",
                    y ="Fidelity", title = "QFT Fidelity VS Number of Qubits",
                        color = "Number of Qubits",
                        category_orders={"Number of Qubits": [8,10,12]}, color_discrete_sequence=["#66c2a5", "#fc8d62", "#8da0cb"]
                        )
                    fig
            if option == "Garnet":
                    filtered_aws = aws_data[aws_data['Target'].str.contains('Garnet')]
                    fig= px.box(filtered_aws, x = "Number of Qubits",
                    y ="Fidelity", title = "QFT Fidelity VS Number of Qubits",
                        color = "Number of Qubits",
                        category_orders={"Number of Qubits": [8,10,12]}, color_discrete_sequence=["#66c2a5", "#fc8d62", "#8da0cb"])
                    fig
            if option == "Harmony":
                    filtered_aws = aws_data[aws_data['Target'].str.contains('Harmony')]
                    fig= px.box(filtered_aws, x = "Number of Qubits",
                    y ="Fidelity", title = "QFT Fidelity VS Number of Qubits (Azure)",
                        color = "Number of Qubits",
                        category_orders={"Number of Qubits": [8,10,12]}, color_discrete_sequence=["#66c2a5", "#fc8d62", "#8da0cb"])
                    fig
            with st.container(border=True):
                fig = px.box(aws_data , x= "Target", y = "Run Time",
                title = "Run Time (Queue Time + Execution Time) VS Target", color = 'Target'

            
        )
                fig.update_yaxes(title = "Run Time (Hours)")
                #fig.update_layout("Ionq simulator has no average queue time because it is not running on real quantum hardware.")
                fig 
            
            
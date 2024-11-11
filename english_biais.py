import streamlit as streamlit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time 

# Variables 
n = 6
pts = 0 
if 'pts' not in streamlit.session_state: 
    streamlit.session_state.pts = 0
if 'valeur' not in streamlit.session_state:
    streamlit.session_state.valeur = 0
if 'i' not in streamlit.session_state:
    streamlit.session_state.i = 0
if 'result' not in streamlit.session_state:
    streamlit.session_state.result  = pd.DataFrame(np.zeros((n , 2)))

# Calculate the total points
streamlit.session_state.pts = streamlit.session_state.result.sum().sum() * 15  # Sum all values and multiply by 15

# Define the biases, questions, and answers
data = {
    "Biases": [
        "Sampling bias",
        "Confirmation bias",
        "Survivorship bias",
        "Correlation bias",
        "Availability bias",
        "Misleading averages"
    ],
    "Examples": [
        "A survey on electoral preferences that only takes into account respondents from an urban area.",
        "A person who only reads articles supporting their opinion on a controversial topic.",
        "Analyzing successful startups without considering those that failed.",
        "A study showing a correlation between chocolate consumption and winning a Nobel Prize.",
        "News reports about airplane accidents influencing our perception of flight risk.",
        "The average salaries of a company can be skewed by a few very high salaries."
    ],
    "Questions": [
        [
            "Did the survey use a representative sample?",
            "Did the survey exclude important groups?"
        ],
        [
            "Did the article you read support your opinion?",
            "Did the article present opposing arguments?"
        ],
        [
            "Did you account for failures in your analysis?",
            "Did you neglect startups that failed?"
        ],
        [
            "Does the correlation in the study imply causality?",
            "Are the study results linked to other factors?"
        ],
        [
            "Are news reports a reliable source for assessing flight risks?",
            "Do the reports reflect actual risks?"
        ],
        [
            "Is the average salary representative of most employees?",
            "Do extreme salaries influence the average?"
        ]
    ],
    "Answers": [
        [True, False],  # for Sampling bias
        [False, True],  # for Confirmation bias
        [True, False],  # for Survivorship bias
        [False, True],  # for Correlation bias
        [False, True],  # for Availability bias
        [True, False]    # for Misleading averages
    ]
}

bias_advice = {
    "Sampling bias": "Ensure that your sample is representative of the entire population by including diverse groups.",
    "Confirmation bias": "Try considering opposing arguments to avoid reinforcing your own beliefs and gain a more complete view.",
    "Survivorship bias": "Account for failures in your analysis to avoid distorting reality by focusing only on successes.",
    "Correlation bias": "Remember that correlation does not prove causality. Look for other factors before drawing conclusions.",
    "Availability bias": "Avoid judging risks based only on recent or widely reported events. Seek more complete data.",
    "Misleading averages": "Ensure the average is representative and not influenced by extreme values. Use alternative measures if necessary."
}

# Create the DataFrame
df_biais = pd.DataFrame(data)

# Function to display questions
def questions():
    df_biais = pd.DataFrame(data)
    # Select a bias
    selected_bias_index = streamlit.session_state.i
    # Display the concrete example
    streamlit.write("Concrete example:", df_biais["Examples"][selected_bias_index])
    # Display the first question with selectbox
    first_question = df_biais["Questions"][selected_bias_index][0]
    response_first = streamlit.selectbox(f"{first_question}", ["Yes", "No"])
    # Display the second question with selectbox
    second_question = df_biais["Questions"][selected_bias_index][1]
    response_second = streamlit.selectbox(f"{second_question}", ["Yes", "No"])
    # Display the selected answers
    streamlit.write("Answer to the first question:", response_first)
    streamlit.write("Answer to the second question:", response_second)
    return response_first, response_second

# Function for the dots menu
def dots_menu(i, n):
    x = list(range(n))
    colors = ['gray'] * n  # All points in gray by default
    colors[i] = 'red'  # Change the color of the i-th selected point
    # Create the plot
    plt.figure(figsize=(10, 2))
    plt.scatter(x, [1]*len(x), color=colors, s=100)  # Points on a horizontal line
    plt.yticks([])  # No y-axis
    plt.xlim(-0.5, n-0.5)  # Adjust x-axis limits
    plt.axis('off')  # Hide axes
    plt.gca().set_facecolor('none')  # Transparent plot background
    streamlit.pyplot(plt, transparent=True)

# Home page
if streamlit.session_state.valeur == 0:
    col1, col2 = streamlit.columns([1, 3])  
    with col1:
        streamlit.write(f"{streamlit.session_state.pts} pts")
    with col2:
        streamlit.title("Statistical Biases")
    col1, col2, col3 = streamlit.columns([1, 2, 1])  
    with col2:
        if streamlit.button("Start"):
            streamlit.session_state.valeur = 1 
            streamlit.success("Good luck!")
            time.sleep(0.3)
            streamlit.session_state.clear()  # Clears session state to trigger rerun
           

# Page for the game i
if streamlit.session_state.valeur == 1:
    time.sleep(0.31)
    col1, col2, col3 = streamlit.columns([1, 2, 1])
    with col1: 
        streamlit.write(f"{streamlit.session_state.pts} pts")
    dots_menu(streamlit.session_state.i, n)
    first, second = questions()
    col1, col2, col3 = streamlit.columns([1, 2, 1])
    with col1: 
        if streamlit.button("Previous") and streamlit.session_state.i > 0:
            streamlit.session_state.i -= 1 
           
    with col2: 
        streamlit.button("Check answer")  
    with col3: 
        if streamlit.session_state.i == n - 1:
            if streamlit.button("View results"): 
                streamlit.session_state.valeur = 2  
                streamlit.session_state.clear()  # Clears session state to trigger rerun
                
        if streamlit.session_state.i < n - 1:
            if streamlit.button("Next"):
                if (first == "Yes" and data["Answers"][streamlit.session_state.i][0]) or (first == "No" and not data["Answers"][streamlit.session_state.i][0]):
                    streamlit.session_state.result.iloc[streamlit.session_state.i, 0] = 1
                if (second == "Yes" and data["Answers"][streamlit.session_state.i][1]) or (second == "No" and not data["Answers"][streamlit.session_state.i][1]):
                    streamlit.session_state.result.iloc[streamlit.session_state.i, 1] = 1
                streamlit.session_state.i += 1
                time.sleep(0.3)
                streamlit.write("Current results:")
            

if streamlit.session_state.valeur == 2: 
    streamlit.write("Results")
    streamlit.markdown(f"You scored {streamlit.session_state.pts} pts")

    if 'result' in streamlit.session_state:
        streamlit.write(f"Total points: {streamlit.session_state.pts}")
        displayed_biases = set()
        for i in range(n):
            if i < streamlit.session_state.result.shape[0]:
                for j in range(2):  
                    if j < streamlit.session_state.result.shape[1]:
                        if streamlit.session_state.result.iloc[i, j] == 0:
                            if df_biais['Biases'][i] not in displayed_biases:
                                streamlit.write(f"You need to improve on the bias: {df_biais['Biases'][i]}")
                                streamlit.write(f"Advice: {bias_advice[df_biais['Biases'][i]]}")
                                displayed_biases.add(df_biais['Biases'][i])  
    else:
        streamlit.write("No results available.")

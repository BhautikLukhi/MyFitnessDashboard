import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np


df = pd.read_excel("FoodTracker.xlsx")


#Necessary columns to numeric
df['carbsTotal'] = pd.to_numeric(df['carbsTotal'], errors='coerce')
df['protienTotal'] = pd.to_numeric(df['protienTotal'], errors='coerce')
df['fatTotal'] = pd.to_numeric(df['fatTotal'], errors='coerce')
df['caloriesIntake'] = pd.to_numeric(df['caloriesIntake'], errors='coerce')
df['caloriesBurned'] = pd.to_numeric(df['caloriesBurned'], errors='coerce')
df['NetcalorieIntake'] = pd.to_numeric(df['NetcalorieIntake'], errors='coerce')
df['StepsWalked'] = pd.to_numeric(df['StepsWalked'], errors='coerce')
df['waterIntake'] = pd.to_numeric(df['waterIntake'], errors='coerce')


st.title("Macros, Movement & More")

#df to CSV
csv = df.to_csv(index=False)

#download button
st.download_button(
    label="Download detailed data as CSV",
    data=csv,
    file_name="FoodTracker.xlsx",
    mime="text/csv",
    key="download_button",
    help="Click to download Bhautik's full tracking data as CSV file"
)

#'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'])

#taking out only the day of the month
df['Day'] = df['Date'].dt.day

#stacked Bar Chart for macros
fig_macros = go.Figure()
fig_macros.add_trace(go.Bar(x=df['Day'], y=df['carbsTotal'], name='Carbs', marker_color='blue'))
fig_macros.add_trace(go.Bar(x=df['Day'], y=df['protienTotal'], name='Protein', marker_color='green'))
fig_macros.add_trace(go.Bar(x=df['Day'], y=df['fatTotal'], name='Fats', marker_color='red'))

fig_macros.update_layout(
    title="Macronutrients Intake Over The Whole Month",
    xaxis_title="Days of February",
    yaxis_title="Grams",
    barmode="stack",
    template="plotly_dark",
    xaxis=dict(tickmode="linear", tick0=1, dtick=1)  
)

st.plotly_chart(fig_macros)

#Histogram of Calorie Intake
fig_calories = px.histogram(df, x="caloriesIntake", nbins=20, title="Distribution of Daily Calorie Intake", labels={"caloriesIntake": "Calories"}, template="plotly_dark")
st.plotly_chart(fig_calories)

#pie Chart for Average Macronutrient Ratios
avg_macros = df[['carbsTotal', 'protienTotal', 'fatTotal']].mean()
fig_avg_macros = px.pie(values=avg_macros, names=avg_macros.index, title="Average Macronutrient Distribution", template="plotly_dark")
st.plotly_chart(fig_avg_macros)

#Correlation Heatmap
corr_matrix = df[['carbsTotal', 'protienTotal', 'fatTotal', 'caloriesIntake', 'caloriesBurned', 'NetcalorieIntake', 'StepsWalked', 'waterIntake']].corr()
fig_corr = ff.create_annotated_heatmap(
    z=np.round(corr_matrix.values, 2),
    x=list(corr_matrix.columns),
    y=list(corr_matrix.index),
    colorscale='Blues',
    showscale=True
)
fig_corr.update_layout(
    title_text="Correlation of Dietary and Movement Metrics",
    template="plotly_dark",
    margin=dict(l=80, r=80, t=110, b=100), 
    xaxis=dict(tickangle=-25, tickfont=dict(size=10)),  
    yaxis=dict(tickfont=dict(size=10))  
)

st.plotly_chart(fig_corr, use_container_width=True)

#linechart for Water Intake
avg_water = df["waterIntake"].mean()
fig_water_line = px.line(
    df, x="Date", y="waterIntake",
    title="Daily Water Intake Over The Whole Month",
    labels={"waterIntake": "Water Intake(liters)", "Date": "Date"},
    template="plotly_dark",
    markers=True
)
fig_water_line.add_trace(go.Scatter(x=df["Date"], y=[avg_water] * len(df["Date"]), mode='lines', name="Average", line=dict(color='red', dash='dash')))
st.plotly_chart(fig_water_line)


#line Chart for Calories Intake vs. Calories Burned
fig_cals = px.line(df, x="Date", y=["caloriesIntake", "caloriesBurned"], title="Calories Intake vs. Calories Burned Over The Whole Month", labels={"value": "Calories", "variable": ""}, template="plotly_dark")
st.plotly_chart(fig_cals)


#line chart for steps Walked
avg_steps = df["StepsWalked"].mean()
fig_steps_line = go.Figure()
fig_steps_line.add_trace(go.Scatter(x=df["Date"], y=df["StepsWalked"], mode='lines+markers', name="Steps", line=dict(color='blue')))
fig_steps_line.add_trace(go.Scatter(x=df["Date"], y=[avg_steps] * len(df["Date"]), mode='lines', name="Average", line=dict(color='red', dash='dash')))
fig_steps_line.update_layout(title="Steps Walked Over The Whole Month", xaxis_title="Date", yaxis_title="Steps Walked", template="plotly_dark")
st.plotly_chart(fig_steps_line)







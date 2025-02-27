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

# 1. Stacked Bar Chart for Macronutrient Intake Over Time
fig_macros = go.Figure()
fig_macros.add_trace(go.Bar(x=df['Date'], y=df['carbsTotal'], name='Carbs', marker_color='blue'))
fig_macros.add_trace(go.Bar(x=df['Date'], y=df['protienTotal'], name='Protein', marker_color='green'))
fig_macros.add_trace(go.Bar(x=df['Date'], y=df['fatTotal'], name='Fats', marker_color='red'))
fig_macros.update_layout(title="Macronutrient Intake Over Time", xaxis_title="Date", yaxis_title="Grams", barmode="stack", xaxis=dict(tickangle=-45), template="plotly_dark")
st.plotly_chart(fig_macros)

# 2. Histogram of Calorie Intake
fig_calories = px.histogram(df, x="caloriesIntake", nbins=20, title="Distribution of Daily Calorie Intake", labels={"caloriesIntake": "Calories"}, template="plotly_dark")
st.plotly_chart(fig_calories)

# 3. Scatter Plot: Steps Walked vs. Net Calorie Intake
fig_steps = px.scatter(df, x="StepsWalked", y="NetcalorieIntake", title="Steps Walked vs. Net Calorie Intake", labels={"StepsWalked": "Steps Walked", "NetcalorieIntake": "Net Calorie Intake"}, template="plotly_dark")
st.plotly_chart(fig_steps)

# 4. Boxplot of Water Intake
fig_water = px.box(df, y="waterIntake", title="Distribution of Daily Water Intake", labels={"waterIntake": "Water Intake (Liters)"}, template="plotly_dark")
st.plotly_chart(fig_water)

# 5. Correlation Heatmap
corr_matrix = df[['carbsTotal', 'protienTotal', 'fatTotal', 'caloriesIntake', 'caloriesBurned', 'NetcalorieIntake', 'StepsWalked', 'waterIntake']].corr()
fig_corr = ff.create_annotated_heatmap(z=np.round(corr_matrix.values, 2), x=list(corr_matrix.columns), y=list(corr_matrix.index), colorscale='Blues', showscale=True)
fig_corr.update_layout(title_text="Correlation Matrix of Nutritional and Activity Data", template="plotly_dark")
st.plotly_chart(fig_corr)

# 6. Line Chart: Calories Intake vs. Calories Burned
fig_cals = px.line(df, x="Date", y=["caloriesIntake", "caloriesBurned"], title="Calories Intake vs. Calories Burned Over Time", labels={"value": "Calories", "variable": "Legend"}, template="plotly_dark")
st.plotly_chart(fig_cals)

# 7. Pie Chart: Average Macronutrient Ratios
avg_macros = df[['carbsTotal', 'protienTotal', 'fatTotal']].mean()
fig_avg_macros = px.pie(values=avg_macros, names=avg_macros.index, title="Average Macronutrient Distribution", template="plotly_dark")
st.plotly_chart(fig_avg_macros)

#Average steps walked
avg_steps = df["StepsWalked"].mean()

#Steps Walked Over Time with Average Line
fig_steps_line = go.Figure()
fig_steps_line.add_trace(go.Scatter(x=df["Date"], y=df["StepsWalked"], mode='lines+markers', name="Steps", line=dict(color='blue')))
fig_steps_line.add_trace(go.Scatter(x=df["Date"], y=[avg_steps] * len(df["Date"]), mode='lines', name="Average Steps", line=dict(color='red', dash='dash')))
fig_steps_line.update_layout(title="Steps Walked Over Time with Average", xaxis_title="Date", yaxis_title="Steps Walked", template="plotly_dark")
st.plotly_chart(fig_steps_line)
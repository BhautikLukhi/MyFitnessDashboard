import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import io


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



#Title of the app
st.title("Macros, Movement & More")

#df to CSV
#csv = df.to_csv(index=False)

#dd to excel
output = io.BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, sheet_name="Tracking Data")
    writer.close()
xlsx_data = output.getvalue()

#download button
st.download_button(
    label="Download detailed data as Excel file",
    data=xlsx_data,
    file_name="FoodTracker.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    key="download_button",
    help="Click to download Bhautik's full tracking data"
)


# #Stacked Bar Chart for Macronutrient Intake Over Time
# fig_macros = go.Figure()
# fig_macros.add_trace(go.Bar(x=df['Date'], y=df['carbsTotal'], name='Carbs', marker_color='blue'))
# fig_macros.add_trace(go.Bar(x=df['Date'], y=df['protienTotal'], name='Protein', marker_color='green'))
# fig_macros.add_trace(go.Bar(x=df['Date'], y=df['fatTotal'], name='Fats', marker_color='red'))
# fig_macros.update_layout(title="Macronutrient Intake Over Time", xaxis_title="Date", yaxis_title="Grams", barmode="stack", xaxis=dict(tickangle=-45), template="plotly_dark")
# st.plotly_chart(fig_macros)

# Convert 'Date' to datetime format if it's not already
df['Date'] = pd.to_datetime(df['Date'])

# Extract only the day of the month for better readability
df['Day'] = df['Date'].dt.day

# Stacked Bar Chart with Improved X-axis Labels
fig_macros = go.Figure()
fig_macros.add_trace(go.Bar(x=df['Day'], y=df['carbsTotal'], name='Carbs', marker_color='blue'))
fig_macros.add_trace(go.Bar(x=df['Day'], y=df['protienTotal'], name='Protein', marker_color='green'))
fig_macros.add_trace(go.Bar(x=df['Day'], y=df['fatTotal'], name='Fats', marker_color='red'))

fig_macros.update_layout(
    title="Macronutrient Intake Over Time",
    xaxis_title="Days of February",
    yaxis_title="Grams",
    barmode="stack",
    template="plotly_dark",
    xaxis=dict(tickmode="linear", tick0=1, dtick=1)  # Ensure every day is labeled
)

st.plotly_chart(fig_macros)

#Histogram of Calorie Intake
fig_calories = px.histogram(df, x="caloriesIntake", nbins=20, title="Distribution of Daily Calorie Intake", labels={"caloriesIntake": "Calories"}, template="plotly_dark")
st.plotly_chart(fig_calories)

#Pie Chart for Average Macronutrient Ratios
avg_macros = df[['carbsTotal', 'protienTotal', 'fatTotal']].mean()
fig_avg_macros = px.pie(values=avg_macros, names=avg_macros.index, title="Average Macronutrient Distribution Over The Whole Month", template="plotly_dark")
st.plotly_chart(fig_avg_macros)

#Correlation Heatmap with Mobile-Friendly Adjustments
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
    margin=dict(l=80, r=80, t=100, b=100),  # Adjust margins for better layout
    xaxis=dict(tickangle=-25, tickfont=dict(size=10)),  # Rotate x-axis labels and reduce font size
    yaxis=dict(tickfont=dict(size=10))  # Reduce y-axis font size
)

st.plotly_chart(fig_corr, use_container_width=True)


# #Boxplot of Water Intake
# fig_water = px.box(df, y="waterIntake", title="Distribution of Daily Water Intake", labels={"waterIntake": "Water Intake (Liters)"}, template="plotly_dark")
# st.plotly_chart(fig_water)

#Boxplot of Water Intake
avg_water = df["waterIntake"].mean()
fig_water_line = px.line(
    df, x="Date", y="waterIntake",
    title="Daily Water Intake Over Time",
    labels={"waterIntake": "Water Intake", "Date": "Date"},
    template="plotly_dark",
    markers=True
)
fig_water_line.add_trace(go.Scatter(x=df["Date"], y=[avg_water] * len(df["Date"]), mode='lines', name="Average Water", line=dict(color='red', dash='dash')))
st.plotly_chart(fig_water_line)


#Line Chart for Calories Intake vs. Calories Burned
fig_cals = px.line(df, x="Date", y=["caloriesIntake", "caloriesBurned"], title="Calories Intake vs. Calories Burned Over Time", labels={"value": "Calories", "variable": "Legend"}, template="plotly_dark")
st.plotly_chart(fig_cals)


#Steps Walked Over Time with Average Line
avg_steps = df["StepsWalked"].mean()
fig_steps_line = go.Figure()
fig_steps_line.add_trace(go.Scatter(x=df["Date"], y=df["StepsWalked"], mode='lines+markers', name="Steps", line=dict(color='blue')))
fig_steps_line.add_trace(go.Scatter(x=df["Date"], y=[avg_steps] * len(df["Date"]), mode='lines', name="Average Steps", line=dict(color='red', dash='dash')))
fig_steps_line.update_layout(title="Steps Walked Over Time with Average", xaxis_title="Date", yaxis_title="Steps Walked", template="plotly_dark")
st.plotly_chart(fig_steps_line)





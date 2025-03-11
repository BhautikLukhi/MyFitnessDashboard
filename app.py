import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np

# Load the data
df = pd.read_excel("FoodTracker.xlsx")

# Convert necessary columns to numeric
numeric_cols = ['carbsTotal', 'protienTotal', 'fatTotal', 'caloriesIntake', 
                'caloriesBurned', 'NetcalorieIntake', 'StepsWalked', 'waterIntake']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Convert 'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'])
df['Day'] = df['Date'].dt.day  # Extracting day of the month

# Create Tabs for Navigation
tab1, tab2 = st.tabs(["Overview & Visualizations", "🍽️ Meal Photos"])

# ------------- 📊 Tab 1: Overview & Visualizations -------------
with tab1:
    st.title("Macros, Movement & More!")

    st.markdown("""
    For the entire month of **February**, I meticulously tracked everything I ate—each snack, every calorie, and all my activities.  
    Below is a visual breakdown of my **daily intake, macronutrient distribution, movement patterns, and overall trends** in an interactive format.
    """)

    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data",
        data=csv,
        file_name="FoodTracker.csv",
        mime="text/csv",
        key="download_csv",
        help="Click to download Bhautik's full tracking data as CSV file"
    )

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

    avg_steps = df["StepsWalked"].mean()
    fig_steps_line = go.Figure()
    fig_steps_line.add_trace(go.Scatter(x=df["Date"], y=df["StepsWalked"], mode='lines+markers', name="Steps", line=dict(color='blue')))
    fig_steps_line.add_trace(go.Scatter(x=df["Date"], y=[avg_steps] * len(df["Date"]), mode='lines', name="Average", line=dict(color='red', dash='dash')))
    fig_steps_line.update_layout(title="Steps Walked Over The Whole Month", xaxis_title="Date", yaxis_title="Steps Walked", template="plotly_dark")
    st.plotly_chart(fig_steps_line)

# ------------- 🍽️ Tab 2: Food Tracker - Meal Photos -------------
with tab2:
    st.title("Meal Images - February")
    st.write("Here are the images of the meals I ate throughout February, along with their corresponding names.")

    # **Mapping Image Filenames to Meal Names**
    meal_images = {
        "03L.png": "Fried croquettes, potatoes and Protein bowl",
        "03S1.png": "Hasan's Caramel Latte",
        "04B.png": "Protein Shake",
        "04S1.png": "Small Fruit Bowl at WestEnd",
        "05L.png": "Pasta with sauce, potatoes and Protein bowl",
        "07D.png": "Moong beans sabji with Protein tortillas, yogurt, peanuts",
        "07L.png": "Red Thai curry with Tofu and Rice",
        "09S2.png": "Veggie Delight 15cm",
        "10L.png": "Cheese Spaetzle with Mix vegetables and Protein bowl",
        "11L.png": "Cheese potato pockets, Boiled potatoes with Protein bowl",
        "12L.png": "Gnocchi with Rice and Protein bowl",
        "13L.png": "Pumpkin-potato curry with Rice and Protein bowl",
        "13S1.png": "Apple and Coffee",
        "14D.png": "Pigeon peas Dal with Protein tortillas, yogurt, peanuts",
        "14L.png": "Spinach Puff Pastry, Boiled potatoes and Protein bowl",
        "16D.png": "Vangibhath + Deep fried onion pakora and Milk Tea",
        "16S2.png": "Spicy Chickpeas from Regel",
        "17L.png": "Veg. Schnitzel with Bulgur and Protein bowl",
        "18L.png": "Kale curry with coconut milk with Rice and Grilled Apple",
        "20D.png": "Broccoli-Tofu sabji with Protein tortillas, yogurt, peanuts",
        "20L.png": "Pumpkin-potato curry with Rice and Protein bowl",
        "21L.png": "Pasta with sauce, potatoes and Protein bowl",
        "22D.png": "Cooked Chana dal with Rice and Buttermilk at Eiram's",
        "23D.png": "Veg. chilli burger with Cola zero and Ketchup at Burger Corner",
        "24L.png": "Shepherd's cheese pockets with Broccoli and Protein bowl",
        "25D.png": "Cooked Black gram Dal with Protein tortillas, yogurt, peanuts",
        "25L.png": "Spinach Puff Pastry, Boiled pasta and Protein bowl",
        "27L.png": "Chinese 'Hong-Kong' crispy slice with Boiled potatoes and Protein Bowl",
        "28L.png": "Cauliflower cheese Medallion with Rice and Protein bowl"
    }

    # Display images from the "food" folder
    cols = st.columns(3)  # Creating three columns for grid layout
    for idx, (filename, caption) in enumerate(meal_images.items()):
        with cols[idx % 3]:  # Distribute images across columns
            st.image(f"Food/{filename}", caption=caption, use_container_width=True)


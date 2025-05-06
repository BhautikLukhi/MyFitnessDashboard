import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
# from core.management.data.post import DataManage

#The data :-)
df = pd.read_excel("FoodTracker.xlsx")
march_df = pd.read_excel("FoodTrackerM.xlsx")
april_df = pd.read_excel("FoodTrackerA.xlsx")

numeric_cols = ['carbsTotal', 'protienTotal', 'fatTotal', 'caloriesIntake', 
                'caloriesBurned', 'NetcalorieIntake', 'StepsWalked', 'waterIntake']
# df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Convert columns to numeric
for data in [df, march_df, april_df]:
    data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')
    data['Date'] = pd.to_datetime(data['Date'])
    data['Day'] = data['Date'].dt.day


# #'Date' to datetime format
# df['Date'] = pd.to_datetime(df['Date'])
# df['Day'] = df['Date'].dt.day  #day of the month

#Tabs for Navigation
# tab1, tab2 = st.tabs(["Overview & Visualizations", "🍽️ Meal Photos"])

# Tabs for Navigation
tab1, tab2, tab3, tab4 = st.tabs(["📅 February", "📅 March", "📅 April", "📷Image Gallery"])



# ------------ Tab 1: February Overview ------------

with tab1:
    st.title("Macros, Movement & More! - February")

    st.markdown("""
    From **February**, I have been meticulously tracking everything I am eating—each snack, every calorie, and my physical activities.  
    Below is a visual breakdown of my **daily intake, macronutrient distribution, movement patterns, and overall trends**.
    """)

    #Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data",
        data=csv,
        file_name="FoodTracker.csv",
        mime="text/csv",
        key="download_csvF",
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

    #Pie Chart for Average Macronutrient Ratios
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

    #Linechart for Water Intake
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

    #Line Chart for Calories Intake vs. Calories Burned
    fig_cals = px.line(df, x="Date", y=["caloriesIntake", "caloriesBurned"], title="Calories Intake vs. Calories Burned Over The Whole Month", labels={"value": "Calories", "variable": ""}, template="plotly_dark")
    st.plotly_chart(fig_cals)

    avg_steps = df["StepsWalked"].mean()
    fig_steps_line = go.Figure()
    fig_steps_line.add_trace(go.Scatter(x=df["Date"], y=df["StepsWalked"], mode='lines+markers', name="Steps", line=dict(color='blue')))
    fig_steps_line.add_trace(go.Scatter(x=df["Date"], y=[avg_steps] * len(df["Date"]), mode='lines', name="Average", line=dict(color='red', dash='dash')))
    fig_steps_line.update_layout(title="Steps Walked Over The Whole Month", xaxis_title="Date", yaxis_title="Steps Walked", template="plotly_dark")
    st.plotly_chart(fig_steps_line)

with tab2:
    st.title("March")
    st.write("Analysis of macronutrients, calories, and movement patterns for March.")

    #Download button
    csv = march_df.to_csv(index=False)
    st.download_button(
        label="Download data",
        data=csv,
        file_name="FoodTrackerM.csv",
        mime="text/csv",
        key="download_csvM",
        help="Click to download Bhautik's full tracking data as CSV file"
    )

    #stacked Bar Chart for macros
    fig_macros = go.Figure()
    fig_macros.add_trace(go.Bar(x=march_df['Day'], y=march_df['carbsTotal'], name='Carbs', marker_color='blue'))
    fig_macros.add_trace(go.Bar(x=march_df['Day'], y=march_df['protienTotal'], name='Protein', marker_color='green'))
    fig_macros.add_trace(go.Bar(x=march_df['Day'], y=march_df['fatTotal'], name='Fats', marker_color='red'))

    fig_macros.update_layout(
        title="Macronutrients Intake Over The Whole Month",
        xaxis_title="Days of March",
        yaxis_title="Grams",
        barmode="stack",
        template="plotly_dark",
        xaxis=dict(tickmode="linear", tick0=1, dtick=1)  
    )

    st.plotly_chart(fig_macros)

    #Histogram of Calorie Intake
    fig_calories = px.histogram(march_df, x="caloriesIntake", nbins=20, title="Distribution of Daily Calorie Intake", labels={"caloriesIntake": "Calories"}, template="plotly_dark")
    st.plotly_chart(fig_calories)

    #Pie Chart for Average Macronutrient Ratios
    avg_macros = march_df[['carbsTotal', 'protienTotal', 'fatTotal']].mean()
    fig_avg_macros = px.pie(values=avg_macros, names=avg_macros.index, title="Average Macronutrient Distribution", template="plotly_dark")
    st.plotly_chart(fig_avg_macros)

    #Correlation Heatmap
    corr_matrix = march_df[['carbsTotal', 'protienTotal', 'fatTotal', 'caloriesIntake', 'caloriesBurned', 'NetcalorieIntake', 'StepsWalked', 'waterIntake']].corr()
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

    #Linechart for Water Intake
    avg_water = march_df["waterIntake"].mean()
    fig_water_line = px.line(
        march_df, x="Date", y="waterIntake",
        title="Daily Water Intake Over The Whole Month",
        labels={"waterIntake": "Water Intake(liters)", "Date": "Date"},
        template="plotly_dark",
        markers=True
    )
    fig_water_line.add_trace(go.Scatter(x=march_df["Date"], y=[avg_water] * len(march_df["Date"]), mode='lines', name="Average", line=dict(color='red', dash='dash')))
    st.plotly_chart(fig_water_line)

    #Line Chart for Calories Intake vs. Calories Burned
    fig_cals = px.line(march_df, x="Date", y=["caloriesIntake", "caloriesBurned"], title="Calories Intake vs. Calories Burned Over The Whole Month", labels={"value": "Calories", "variable": ""}, template="plotly_dark")
    st.plotly_chart(fig_cals)

    avg_steps = march_df["StepsWalked"].mean()
    fig_steps_line = go.Figure()
    fig_steps_line.add_trace(go.Scatter(x=march_df["Date"], y=march_df["StepsWalked"], mode='lines+markers', name="Steps", line=dict(color='blue')))
    fig_steps_line.add_trace(go.Scatter(x=march_df["Date"], y=[avg_steps] * len(march_df["Date"]), mode='lines', name="Average", line=dict(color='red', dash='dash')))
    fig_steps_line.update_layout(title="Steps Walked Over The Whole Month", xaxis_title="Date", yaxis_title="Steps Walked", template="plotly_dark")
    st.plotly_chart(fig_steps_line)


# ------------ Tab 3: April Overview ------------
with tab3:
    st.title("April")
    st.write("Analysis of macronutrients, calories, and movement patterns for April.")

    #Download button
    csv = april_df.to_csv(index=False)
    st.download_button(
        label="Download data",
        data=csv,
        file_name="FoodTrackerA.csv",
        mime="text/csv",
        key="download_csvA",
        help="Click to download April tracking data"
    )

    # Stacked bar chart for macros
    fig_macros = go.Figure()
    fig_macros.add_trace(go.Bar(x=april_df['Day'], y=april_df['carbsTotal'], name='Carbs', marker_color='blue'))
    fig_macros.add_trace(go.Bar(x=april_df['Day'], y=april_df['protienTotal'], name='Protein', marker_color='green'))
    fig_macros.add_trace(go.Bar(x=april_df['Day'], y=april_df['fatTotal'], name='Fats', marker_color='red'))

    fig_macros.update_layout(
        title="Macronutrients Intake Over April",
        xaxis_title="Days of April",
        yaxis_title="Grams",
        barmode="stack",
        template="plotly_dark",
        xaxis=dict(tickmode="linear", tick0=1, dtick=1)
    )
    st.plotly_chart(fig_macros)


    # Pie chart for Average Macronutrients
    avg_macros = april_df[['carbsTotal', 'protienTotal', 'fatTotal']].mean()
    fig_avg_macros = px.pie(values=avg_macros, names=avg_macros.index, title="Average Macronutrient Distribution", template="plotly_dark")
    st.plotly_chart(fig_avg_macros)

    # Correlation heatmap
    corr_matrix = april_df[numeric_cols].corr()
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

    # Linechart for Water Intake
    avg_water = april_df["waterIntake"].mean()
    fig_water_line = px.line(
        april_df, x="Date", y="waterIntake",
        title="Daily Water Intake Over April",
        labels={"waterIntake": "Water Intake (liters)", "Date": "Date"},
        template="plotly_dark",
        markers=True
    )
    fig_water_line.add_trace(go.Scatter(x=april_df["Date"], y=[avg_water]*len(april_df), mode='lines', name="Average", line=dict(color='red', dash='dash')))
    st.plotly_chart(fig_water_line)

    # Line chart: Calories Intake vs Burned
    fig_cals = px.line(april_df, x="Date", y=["caloriesIntake", "caloriesBurned"], title="Calories Intake vs. Calories Burned in April", labels={"value": "Calories", "variable": ""}, template="plotly_dark")
    st.plotly_chart(fig_cals)

    # Steps chart
    avg_steps = april_df["StepsWalked"].mean()
    fig_steps_line = go.Figure()
    fig_steps_line.add_trace(go.Scatter(x=april_df["Date"], y=april_df["StepsWalked"], mode='lines+markers', name="Steps", line=dict(color='blue')))
    fig_steps_line.add_trace(go.Scatter(x=april_df["Date"], y=[avg_steps] * len(april_df), mode='lines', name="Average", line=dict(color='red', dash='dash')))
    fig_steps_line.update_layout(title="Steps Walked in April", xaxis_title="Date", yaxis_title="Steps Walked", template="plotly_dark")
    st.plotly_chart(fig_steps_line)


# ------------- 🍽️ Tab 3: Food Tracker - Meal Photos -------------
with tab4:
    st.title("Little fact: Switching to this diet cost me €150 more than my usual grocery/food expenses.")
    #st.write("Here are some images of what I ate throughout February and March.")
    # Instagram link with icon
    st.markdown(
    """
    <div style="text-align:center; margin-bottom: 20px;">
        <a href="https://instagram.com/bhautik.py" target="_blank" style="text-decoration: none;">
            <img src="https://img.icons8.com/?size=100&id=ZRiAFreol5mE&format=png&color=000000" style="vertical-align: middle; margin-right: 8px; width="40" ; height="40""/>
            <span style="font-size: 20px; color: #1E90FF;">Wanna see more of my fitness grind? Catch me on Instagram!</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


    # **Mapping Image Filenames to Meal Names**
    meal_images = {
        "03L.png": "Fried croquettes, potatoes and Protein bowl",
        "03S1.png": "Hasan's Caramel Latte",
        "04B.png": "Protein Shake",
        "Back.png": "Back gains after 3 months of Weight Training",
        "M28.png": "DM-Protien Cookie",
        "M29S.png": "Hot indian Snack",
        "M30.png": "Solo starbucks date after 3 hours of Gym session",
        "04S1.png": "Small Fruit Bowl at WestEnd",
        "05L.png": "Pasta with sauce, potatoes and Protein bowl",
        "07D.png": "Moong beans sabji with Protein tortillas, yogurt, peanuts",
        "07L.png": "Red Thai curry with Tofu and Rice",
        "09S2.png": "Veggie Delight 15cm",
        "M1.png": "Samosa (Indian snack - deep-fried pastry with savory filling)",
        "M2.png": "Paneer butter masala with Naan and Rice - Swaad Indian Restaurant, Düsseldorf",
        "M3.png": "Croissant with Hot Chocolate",
        "M4.png": "Soya Rice outside X-Building",
        "M5.png": "Pizza with Veggies and Dip",
        "M6.png": "Soya Rice with Quark and Peanuts",
        "M7.png": "Kassebrotchen",
        "M8.png": "Mixed Vegetable Curry with Quark and Protein Tortillas",
        #"M9.png": "Pappermint Tea X-cafeteria",
        "M10.png": "Mixed Beans and Nuts Bowl",
        "M11.png": "Slice of Cheesecake",
        "M12.png": "Hasan's Cappuccino",
        "M13.png": "Soya Rice",
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
        #"28L.png": "Cauliflower cheese Medallion with Rice and Protein bowl"
    }

        #Iterate through images 
    cols = st.columns(3)  # three columns for grid layout
    for idx, (filename, caption) in enumerate(meal_images.items()):
        with cols[idx % 3]:  
            st.image(f"Food/{filename}", caption=caption)



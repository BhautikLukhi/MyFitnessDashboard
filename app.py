# from pathlib import Path

# import numpy as np
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import streamlit as st

# # -------------------------------------------------------------------
# # Nutrify: Food, movement, and nutrition dashboard
# # Keep FoodTracker.xlsx, FoodTrackerM.xlsx, FoodTrackerA.xlsx and the
# # Food/ image folder in the same repository as this app.py file.
# # -------------------------------------------------------------------

# st.set_page_config(page_title="Nutrify | Food & Fitness Dashboard", page_icon="🥗", layout="wide")

# BASE_DIR = Path(__file__).resolve().parent

# NUMERIC_COLS = [
#     "carbsTotal",
#     "protienTotal",
#     "fatTotal",
#     "caloriesIntake",
#     "caloriesBurned",
#     "NetcalorieIntake",
#     "StepsWalked",
#     "waterIntake",
# ]

# MONTHS = [
#     {
#         "label": "📅 February",
#         "file": "FoodTracker.xlsx",
#         "title": "Macros, Movement & More! - February",
#         "description": (
#             "From **February**, I have been meticulously tracking everything I am "
#             "eating—each snack, every calorie, and my physical activities. Below is "
#             "a visual breakdown of my **daily intake, macronutrient distribution, "
#             "movement patterns, and overall trends**."
#         ),
#         "csv_name": "FoodTracker.csv",
#         "month_label": "February",
#         "show_histogram": True,
#     },
#     {
#         "label": "📅 March",
#         "file": "FoodTrackerM.xlsx",
#         "title": "March",
#         "description": "Analysis of macronutrients, calories, and movement patterns for March.",
#         "csv_name": "FoodTrackerM.csv",
#         "month_label": "March",
#         "show_histogram": True,
#     },
#     {
#         "label": "📅 April",
#         "file": "FoodTrackerA.xlsx",
#         "title": "April",
#         "description": "Analysis of macronutrients, calories, and movement patterns for April.",
#         "csv_name": "FoodTrackerA.csv",
#         "month_label": "April",
#         "show_histogram": False,
#     },
# ]

# MEAL_IMAGES = {
#     "03L.png": "Fried croquettes, potatoes and Protein bowl",
#     "03S1.png": "Hasan's Caramel Latte",
#     "04B.png": "Protein Shake",
#     "Back.png": "Back gains after 3 months of Weight Training",
#     "M28.png": "DM-Protein Cookie",
#     "M29S.png": "Hot Indian Snack",
#     "M30.png": "Solo Starbucks date after 3 hours of Gym session",
#     "04S1.png": "Small Fruit Bowl at WestEnd",
#     "05L.png": "Pasta with sauce, potatoes and Protein bowl",
#     "07D.png": "Moong beans sabji with Protein tortillas, yogurt, peanuts",
#     "07L.png": "Red Thai curry with Tofu and Rice",
#     "09S2.png": "Veggie Delight 15cm",
#     "M1.png": "Samosa (Indian snack - deep-fried pastry with savory filling)",
#     "M2.png": "Paneer butter masala with Naan and Rice - Swaad Indian Restaurant, Düsseldorf",
#     "M3.png": "Croissant with Hot Chocolate",
#     "M4.png": "Soya Rice outside X-Building",
#     "M5.png": "Pizza with Veggies and Dip",
#     "M6.png": "Soya Rice with Quark and Peanuts",
#     "M7.png": "Kassebrötchen",
#     "M8.png": "Mixed Vegetable Curry with Quark and Protein Tortillas",
#     "M10.png": "Mixed Beans and Nuts Bowl",
#     "M11.png": "Slice of Cheesecake",
#     "M12.png": "Hasan's Cappuccino",
#     "M13.png": "Soya Rice",
#     "10L.png": "Cheese Spaetzle with Mixed Vegetables and Protein bowl",
#     "11L.png": "Cheese potato pockets, boiled potatoes with Protein bowl",
#     "12L.png": "Gnocchi with Rice and Protein bowl",
#     "13L.png": "Pumpkin-potato curry with Rice and Protein bowl",
#     "13S1.png": "Apple and Coffee",
#     "14L.png": "Spinach Puff Pastry, boiled potatoes and Protein bowl",
#     "16D.png": "Vangibhath, deep-fried onion pakora and milk tea",
#     "16S2.png": "Spicy Chickpeas from Regel",
#     "17L.png": "Veg. Schnitzel with Bulgur and Protein bowl",
#     "18L.png": "Kale curry with coconut milk, Rice and Grilled Apple",
#     "20D.png": "Broccoli-Tofu sabji with Protein tortillas, yogurt, peanuts",
#     "20L.png": "Pumpkin-potato curry with Rice and Protein bowl",
#     "21L.png": "Pasta with sauce, potatoes and Protein bowl",
#     "22D.png": "Cooked Chana dal with Rice and Buttermilk at Eiram's",
#     "23D.png": "Veggie chilli burger with Cola Zero and Ketchup at Burger Corner",
#     "24L.png": "Shepherd's cheese pockets with Broccoli and Protein bowl",
#     "25D.png": "Cooked Black gram Dal with Protein tortillas, yogurt, peanuts",
#     "25L.png": "Spinach Puff Pastry, boiled pasta and Protein bowl",
#     "27L.png": "Chinese 'Hong-Kong' crispy slice with boiled potatoes and Protein Bowl",
# }


# @st.cache_data
# def load_month_data(filename: str) -> pd.DataFrame:
#     """Load and prepare one monthly Excel file."""
#     file_path = BASE_DIR / filename
#     if not file_path.exists():
#         raise FileNotFoundError(
#             f"Could not find {filename}. Upload it to the same GitHub repository "
#             "folder as app.py."
#         )

#     data = pd.read_excel(file_path)

#     missing = [column for column in ["Date", *NUMERIC_COLS] if column not in data.columns]
#     if missing:
#         raise ValueError(
#             f"{filename} is missing required column(s): {', '.join(missing)}. "
#             "Please check the Excel column names."
#         )

#     for column in NUMERIC_COLS:
#         data[column] = pd.to_numeric(data[column], errors="coerce")

#     data["Date"] = pd.to_datetime(data["Date"], errors="coerce", dayfirst=False)
#     data = data.dropna(subset=["Date"]).copy()
#     data["Day"] = data["Date"].dt.day
#     return data.sort_values("Date").reset_index(drop=True)


# def correlation_heatmap(data: pd.DataFrame, month_label: str):
#     """Create a correlation heatmap without the deprecated figure_factory API."""
#     corr_matrix = data[NUMERIC_COLS].corr().fillna(0)

#     # px.imshow works with a Pandas DataFrame and supports cell annotations.
#     fig = px.imshow(
#         corr_matrix,
#         text_auto=".2f",
#         aspect="auto",
#         color_continuous_scale="Blues",
#         zmin=-1,
#         zmax=1,
#         origin="lower",
#         labels={"x": "Metric", "y": "Metric", "color": "Correlation"},
#         title=f"Correlation of Dietary and Movement Metrics — {month_label}",
#     )
#     fig.update_layout(
#         template="plotly_dark",
#         margin=dict(l=80, r=80, t=100, b=120),
#         coloraxis_colorbar=dict(title="Correlation"),
#     )
#     fig.update_xaxes(tickangle=-35, tickfont=dict(size=10))
#     fig.update_yaxes(tickfont=dict(size=10))
#     return fig


# def render_month(data: pd.DataFrame, month: dict):
#     month_label = month["month_label"]
#     st.title(month["title"])
#     st.markdown(month["description"])

#     st.download_button(
#         label="Download data",
#         data=data.to_csv(index=False).encode("utf-8"),
#         file_name=month["csv_name"],
#         mime="text/csv",
#         key=f"download_{month_label.lower()}",
#         help="Download this month's tracking data as a CSV file.",
#     )

#     if data.empty:
#         st.warning(f"There are no valid dated records in the {month_label} dataset.")
#         return

#     # Macronutrients: stacked daily bar chart
#     fig_macros = go.Figure()
#     fig_macros.add_trace(
#         go.Bar(x=data["Day"], y=data["carbsTotal"], name="Carbs", marker_color="blue")
#     )
#     fig_macros.add_trace(
#         go.Bar(x=data["Day"], y=data["protienTotal"], name="Protein", marker_color="green")
#     )
#     fig_macros.add_trace(
#         go.Bar(x=data["Day"], y=data["fatTotal"], name="Fats", marker_color="red")
#     )
#     fig_macros.update_layout(
#         title=f"Macronutrient Intake Over {month_label}",
#         xaxis_title=f"Days of {month_label}",
#         yaxis_title="Grams",
#         barmode="stack",
#         template="plotly_dark",
#         xaxis=dict(tickmode="linear", tick0=1, dtick=1),
#     )
#     st.plotly_chart(fig_macros, use_container_width=True)

#     # Calorie distribution (not shown in the original April tab)
#     if month["show_histogram"]:
#         fig_calories = px.histogram(
#             data,
#             x="caloriesIntake",
#             nbins=20,
#             title="Distribution of Daily Calorie Intake",
#             labels={"caloriesIntake": "Calories"},
#             template="plotly_dark",
#         )
#         st.plotly_chart(fig_calories, use_container_width=True)

#     # Average macronutrient distribution
#     avg_macros = data[["carbsTotal", "protienTotal", "fatTotal"]].mean().fillna(0)
#     if avg_macros.sum() > 0:
#         fig_avg_macros = px.pie(
#             values=avg_macros.values,
#             names=["Carbs", "Protein", "Fats"],
#             title="Average Macronutrient Distribution",
#             template="plotly_dark",
#         )
#         st.plotly_chart(fig_avg_macros, use_container_width=True)
#     else:
#         st.info("There is not enough macronutrient data to calculate the average distribution.")

#     # Correlation heatmap: px.imshow replaces deprecated ff.create_annotated_heatmap
#     st.plotly_chart(correlation_heatmap(data, month_label), use_container_width=True)

#     # Water intake and average line
#     avg_water = data["waterIntake"].mean()
#     fig_water_line = px.line(
#         data,
#         x="Date",
#         y="waterIntake",
#         title=f"Daily Water Intake Over {month_label}",
#         labels={"waterIntake": "Water Intake (liters)", "Date": "Date"},
#         template="plotly_dark",
#         markers=True,
#     )
#     if pd.notna(avg_water):
#         fig_water_line.add_trace(
#             go.Scatter(
#                 x=data["Date"],
#                 y=[avg_water] * len(data),
#                 mode="lines",
#                 name="Average",
#                 line=dict(color="red", dash="dash"),
#             )
#         )
#     st.plotly_chart(fig_water_line, use_container_width=True)

#     # Calories consumed versus burned
#     fig_cals = px.line(
#         data,
#         x="Date",
#         y=["caloriesIntake", "caloriesBurned"],
#         title=f"Calories Intake vs. Calories Burned — {month_label}",
#         labels={"value": "Calories", "variable": ""},
#         template="plotly_dark",
#     )
#     st.plotly_chart(fig_cals, use_container_width=True)

#     # Steps and average line
#     avg_steps = data["StepsWalked"].mean()
#     fig_steps = go.Figure()
#     fig_steps.add_trace(
#         go.Scatter(
#             x=data["Date"],
#             y=data["StepsWalked"],
#             mode="lines+markers",
#             name="Steps",
#             line=dict(color="blue"),
#         )
#     )
#     if pd.notna(avg_steps):
#         fig_steps.add_trace(
#             go.Scatter(
#                 x=data["Date"],
#                 y=[avg_steps] * len(data),
#                 mode="lines",
#                 name="Average",
#                 line=dict(color="red", dash="dash"),
#             )
#         )
#     fig_steps.update_layout(
#         title=f"Steps Walked in {month_label}",
#         xaxis_title="Date",
#         yaxis_title="Steps Walked",
#         template="plotly_dark",
#     )
#     st.plotly_chart(fig_steps, use_container_width=True)


# def render_gallery():
#     st.title("📷 Meal & Fitness Image Gallery")
#     st.write("A collection of meal photos and fitness progress images.")

#     image_dir = BASE_DIR / "Food"
#     cols = st.columns(3)
#     shown = 0

#     for filename, caption in MEAL_IMAGES.items():
#         image_path = image_dir / filename
#         if not image_path.is_file():
#             continue
#         with cols[shown % 3]:
#             st.image(str(image_path), caption=caption, use_container_width=True)
#         shown += 1

#     if shown == 0:
#         st.info(
#             "No gallery images were found. Make sure the Food folder and its image "
#             "files are committed to the GitHub repository."
#         )


# st.title("Nutrify — Food, Movement & More")

# tabs = st.tabs([month["label"] for month in MONTHS] + ["📷 Image Gallery"])

# for tab, month in zip(tabs[:3], MONTHS):
#     with tab:
#         try:
#             monthly_data = load_month_data(month["file"])
#             render_month(monthly_data, month)
#         except (FileNotFoundError, ValueError, ImportError) as exc:
#             st.error(str(exc))
#         except Exception as exc:
#             st.error(
#                 f"Something went wrong while loading {month['month_label']} data. "
#                 "Check the Streamlit Cloud logs for the technical details."
#             )
#             st.exception(exc)

# with tabs[3]:
#     render_gallery()


from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -------------------------------------------------------------------
# Nutrify: Food, movement, and nutrition dashboard
#
# Repository structure:
# app.py
# requirements.txt
# FoodTracker.xlsx
# FoodTrackerM.xlsx
# FoodTrackerA.xlsx
# Food/
#   (meal and fitness images)
# -------------------------------------------------------------------

st.set_page_config(
    page_title="Nutrify | Food & Fitness Dashboard",
    page_icon="🥗",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent

NUMERIC_COLS = [
    "carbsTotal",
    "protienTotal",
    "fatTotal",
    "caloriesIntake",
    "caloriesBurned",
    "NetcalorieIntake",
    "StepsWalked",
    "waterIntake",
]

MONTHS = [
    {
        "label": "📅 February",
        "file": "FoodTracker.xlsx",
        "title": "Macros, Movement & More! - February",
        "description": (
            "From **February**, I have been meticulously tracking everything I am "
            "eating—each snack, every calorie, and my physical activities. Below is "
            "a visual breakdown of my **daily intake, macronutrient distribution, "
            "movement patterns, and overall trends**."
        ),
        "csv_name": "FoodTracker.csv",
        "month_label": "February",
        "show_histogram": True,
    },
    {
        "label": "📅 March",
        "file": "FoodTrackerM.xlsx",
        "title": "March",
        "description": (
            "Analysis of macronutrients, calories, and movement patterns for March."
        ),
        "csv_name": "FoodTrackerM.csv",
        "month_label": "March",
        "show_histogram": True,
    },
    {
        "label": "📅 April",
        "file": "FoodTrackerA.xlsx",
        "title": "April",
        "description": (
            "Analysis of macronutrients, calories, and movement patterns for April."
        ),
        "csv_name": "FoodTrackerA.csv",
        "month_label": "April",
        "show_histogram": False,
    },
]

MEAL_IMAGES = {
    "03L.png": "Fried croquettes, potatoes and Protein bowl",
    "03S1.png": "Hasan's Caramel Latte",
    "04B.png": "Protein Shake",
    "Back.png": "Back gains after 3 months of Weight Training",
    "M28.png": "DM-Protein Cookie",
    "M29S.png": "Hot Indian Snack",
    "M30.png": "Solo Starbucks date after 3 hours of Gym session",
    "04S1.png": "Small Fruit Bowl at WestEnd",
    "05L.png": "Pasta with sauce, potatoes and Protein bowl",
    "07D.png": "Moong beans sabji with Protein tortillas, yogurt, peanuts",
    "07L.png": "Red Thai curry with Tofu and Rice",
    "09S2.png": "Veggie Delight 15cm",
    "M1.png": "Samosa (Indian snack - deep-fried pastry with savory filling)",
    "M2.png": (
        "Paneer butter masala with Naan and Rice - "
        "Swaad Indian Restaurant, Düsseldorf"
    ),
    "M3.png": "Croissant with Hot Chocolate",
    "M4.png": "Soya Rice outside X-Building",
    "M5.png": "Pizza with Veggies and Dip",
    "M6.png": "Soya Rice with Quark and Peanuts",
    "M7.png": "Kassebrötchen",
    "M8.png": "Mixed Vegetable Curry with Quark and Protein Tortillas",
    "M10.png": "Mixed Beans and Nuts Bowl",
    "M11.png": "Slice of Cheesecake",
    "M12.png": "Hasan's Cappuccino",
    "M13.png": "Soya Rice",
    "10L.png": "Cheese Spaetzle with Mixed Vegetables and Protein bowl",
    "11L.png": "Cheese potato pockets, boiled potatoes with Protein bowl",
    "12L.png": "Gnocchi with Rice and Protein bowl",
    "13L.png": "Pumpkin-potato curry with Rice and Protein bowl",
    "13S1.png": "Apple and Coffee",
    "14L.png": "Spinach Puff Pastry, boiled potatoes and Protein bowl",
    "16D.png": "Vangibhath, deep-fried onion pakora and milk tea",
    "16S2.png": "Spicy Chickpeas from Regel",
    "17L.png": "Veg. Schnitzel with Bulgur and Protein bowl",
    "18L.png": "Kale curry with coconut milk, Rice and Grilled Apple",
    "20D.png": "Broccoli-Tofu sabji with Protein tortillas, yogurt, peanuts",
    "20L.png": "Pumpkin-potato curry with Rice and Protein bowl",
    "21L.png": "Pasta with sauce, potatoes and Protein bowl",
    "22D.png": "Cooked Chana dal with Rice and Buttermilk at Eiram's",
    "23D.png": "Veggie chilli burger with Cola Zero and Ketchup at Burger Corner",
    "24L.png": "Shepherd's cheese pockets with Broccoli and Protein bowl",
    "25D.png": "Cooked Black gram Dal with Protein tortillas, yogurt, peanuts",
    "25L.png": "Spinach Puff Pastry, boiled pasta and Protein bowl",
    "27L.png": "Chinese 'Hong-Kong' crispy slice with boiled potatoes and Protein Bowl",
}


# -------------------------------------------------------------------
# DATA LOADING
# -------------------------------------------------------------------

@st.cache_data
def load_month_data(filename: str) -> pd.DataFrame:
    """Load and prepare one monthly Excel file."""
    file_path = BASE_DIR / filename

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Could not find {filename}. Make sure it is committed to the "
            "same GitHub repository folder as app.py."
        )

    data = pd.read_excel(file_path)

    required_columns = ["Date", *NUMERIC_COLS]
    missing = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"{filename} is missing required column(s): "
            f"{', '.join(missing)}. Please check the Excel column names."
        )

    # Convert numeric columns safely.
    for column in NUMERIC_COLS:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    # Handle Excel dates and invalid date values.
    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce",
    )

    data = data.dropna(subset=["Date"]).copy()
    data["Day"] = data["Date"].dt.day

    return data.sort_values("Date").reset_index(drop=True)


# -------------------------------------------------------------------
# CORRELATION HEATMAP
# Uses graph_objects instead of px.imshow to avoid image-related
# compatibility problems with some Plotly and NumPy combinations.
# -------------------------------------------------------------------

def correlation_heatmap(data: pd.DataFrame, month_label: str):
    """Create an annotated correlation heatmap."""

    corr_matrix = data[NUMERIC_COLS].corr()

    # Replace undefined correlations so the chart renders reliably.
    corr_values = corr_matrix.to_numpy(dtype=float)
    corr_values = np.nan_to_num(
        corr_values,
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=corr_values,
            x=NUMERIC_COLS,
            y=NUMERIC_COLS,
            colorscale="Blues",
            zmin=-1,
            zmax=1,
            colorbar=dict(title="Correlation"),
            text=np.round(corr_values, 2),
            texttemplate="%{text:.2f}",
            hovertemplate=(
                "%{y} vs %{x}<br>"
                "Correlation: %{z:.2f}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=f"Correlation of Dietary and Movement Metrics — {month_label}",
        template="plotly_dark",
        margin=dict(l=80, r=40, t=90, b=140),
        height=650,
    )

    fig.update_xaxes(
        tickangle=-40,
        tickfont=dict(size=10),
        automargin=True,
    )

    fig.update_yaxes(
        tickfont=dict(size=10),
        autorange="reversed",
        automargin=True,
    )

    return fig


# -------------------------------------------------------------------
# MONTHLY DASHBOARD
# -------------------------------------------------------------------

def render_month(data: pd.DataFrame, month: dict):
    month_label = month["month_label"]

    st.title(month["title"])
    st.markdown(month["description"])

    st.download_button(
        label="Download data",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name=month["csv_name"],
        mime="text/csv",
        key=f"download_{month_label.lower()}",
        help="Download this month's tracking data as a CSV file.",
    )

    if data.empty:
        st.warning(
            f"There are no valid dated records in the {month_label} dataset."
        )
        return

    # ---------------------------------------------------------------
    # Macronutrient intake: stacked daily bar chart
    # ---------------------------------------------------------------

    fig_macros = go.Figure()

    fig_macros.add_trace(
        go.Bar(
            x=data["Day"],
            y=data["carbsTotal"],
            name="Carbs",
            marker_color="blue",
        )
    )

    fig_macros.add_trace(
        go.Bar(
            x=data["Day"],
            y=data["protienTotal"],
            name="Protein",
            marker_color="green",
        )
    )

    fig_macros.add_trace(
        go.Bar(
            x=data["Day"],
            y=data["fatTotal"],
            name="Fats",
            marker_color="red",
        )
    )

    fig_macros.update_layout(
        title=f"Macronutrient Intake Over {month_label}",
        xaxis_title=f"Days of {month_label}",
        yaxis_title="Grams",
        barmode="stack",
        template="plotly_dark",
        xaxis=dict(
            tickmode="linear",
            tick0=1,
            dtick=1,
        ),
    )

    st.plotly_chart(
        fig_macros,
        use_container_width=True,
        key=f"macros_{month_label}",
    )

    # ---------------------------------------------------------------
    # Calorie distribution
    # ---------------------------------------------------------------

    if month["show_histogram"]:
        calorie_data = data.dropna(subset=["caloriesIntake"])

        if not calorie_data.empty:
            fig_calories = px.histogram(
                calorie_data,
                x="caloriesIntake",
                nbins=20,
                title="Distribution of Daily Calorie Intake",
                labels={"caloriesIntake": "Calories"},
                template="plotly_dark",
            )

            st.plotly_chart(
                fig_calories,
                use_container_width=True,
                key=f"calories_hist_{month_label}",
            )
        else:
            st.info("No calorie intake data is available for this month.")

    # ---------------------------------------------------------------
    # Average macronutrient distribution
    # ---------------------------------------------------------------

    avg_macros = (
        data[["carbsTotal", "protienTotal", "fatTotal"]]
        .mean()
        .fillna(0)
    )

    if avg_macros.sum() > 0:
        fig_avg_macros = px.pie(
            values=avg_macros.values,
            names=["Carbs", "Protein", "Fats"],
            title="Average Macronutrient Distribution",
            template="plotly_dark",
        )

        st.plotly_chart(
            fig_avg_macros,
            use_container_width=True,
            key=f"macro_pie_{month_label}",
        )
    else:
        st.info(
            "There is not enough macronutrient data to calculate "
            "the average distribution."
        )

    # ---------------------------------------------------------------
    # Correlation heatmap
    # ---------------------------------------------------------------

    st.plotly_chart(
        correlation_heatmap(data, month_label),
        use_container_width=True,
        key=f"correlation_{month_label}",
    )

    # ---------------------------------------------------------------
    # Water intake and average line
    # ---------------------------------------------------------------

    water_data = data.dropna(subset=["waterIntake"])
    avg_water = water_data["waterIntake"].mean()

    fig_water_line = px.line(
        water_data,
        x="Date",
        y="waterIntake",
        title=f"Daily Water Intake Over {month_label}",
        labels={
            "waterIntake": "Water Intake (liters)",
            "Date": "Date",
        },
        template="plotly_dark",
        markers=True,
    )

    if pd.notna(avg_water) and not water_data.empty:
        fig_water_line.add_trace(
            go.Scatter(
                x=water_data["Date"],
                y=[avg_water] * len(water_data),
                mode="lines",
                name="Average",
                line=dict(color="red", dash="dash"),
            )
        )

    st.plotly_chart(
        fig_water_line,
        use_container_width=True,
        key=f"water_{month_label}",
    )

    # ---------------------------------------------------------------
    # Calories consumed versus burned
    # ---------------------------------------------------------------

    calorie_comparison = data[
        ["Date", "caloriesIntake", "caloriesBurned"]
    ].copy()

    fig_cals = px.line(
        calorie_comparison,
        x="Date",
        y=["caloriesIntake", "caloriesBurned"],
        title=f"Calories Intake vs. Calories Burned — {month_label}",
        labels={
            "value": "Calories",
            "variable": "",
            "Date": "Date",
        },
        template="plotly_dark",
    )

    st.plotly_chart(
        fig_cals,
        use_container_width=True,
        key=f"calorie_comparison_{month_label}",
    )

    # ---------------------------------------------------------------
    # Steps walked and average line
    # ---------------------------------------------------------------

    steps_data = data.dropna(subset=["StepsWalked"])
    avg_steps = steps_data["StepsWalked"].mean()

    fig_steps = go.Figure()

    fig_steps.add_trace(
        go.Scatter(
            x=steps_data["Date"],
            y=steps_data["StepsWalked"],
            mode="lines+markers",
            name="Steps",
            line=dict(color="blue"),
        )
    )

    if pd.notna(avg_steps) and not steps_data.empty:
        fig_steps.add_trace(
            go.Scatter(
                x=steps_data["Date"],
                y=[avg_steps] * len(steps_data),
                mode="lines",
                name="Average",
                line=dict(color="red", dash="dash"),
            )
        )

    fig_steps.update_layout(
        title=f"Steps Walked in {month_label}",
        xaxis_title="Date",
        yaxis_title="Steps Walked",
        template="plotly_dark",
    )

    st.plotly_chart(
        fig_steps,
        use_container_width=True,
        key=f"steps_{month_label}",
    )


# -------------------------------------------------------------------
# MEAL AND FITNESS GALLERY
# -------------------------------------------------------------------

def render_gallery():
    st.title("📷 Meal & Fitness Image Gallery")
    st.write(
        "A collection of meal photos and fitness progress images."
    )

    image_dir = BASE_DIR / "Food"

    if not image_dir.is_dir():
        st.info(
            "The Food folder was not found. Make sure it is committed "
            "to the GitHub repository alongside app.py."
        )
        return

    cols = st.columns(3)
    shown = 0

    for filename, caption in MEAL_IMAGES.items():
        image_path = image_dir / filename

        if not image_path.is_file():
            continue

        try:
            with cols[shown % 3]:
                # Compatibility fix:
                # use_column_width works with older Streamlit versions
                # that do not accept use_container_width in st.image().
                st.image(
                    str(image_path),
                    caption=caption,
                    use_column_width=True,
                )

            shown += 1

        except Exception as exc:
            st.warning(
                f"Could not display {filename}: {exc}"
            )

    if shown == 0:
        st.info(
            "No gallery images were found. Check that the Food folder "
            "contains the expected image files and that their names "
            "match MEAL_IMAGES."
        )


# -------------------------------------------------------------------
# MAIN APPLICATION
# -------------------------------------------------------------------

st.title("Nutrify — Food, Movement & More")

tabs = st.tabs(
    [month["label"] for month in MONTHS] + ["📷 Image Gallery"]
)

for tab, month in zip(tabs[:3], MONTHS):
    with tab:
        try:
            monthly_data = load_month_data(month["file"])
            render_month(monthly_data, month)

        except (FileNotFoundError, ValueError) as exc:
            st.error(str(exc))

        except ImportError as exc:
            st.error(
                "A required Python package is missing. "
                "Check requirements.txt and redeploy the app. "
                f"Details: {exc}"
            )

        except Exception as exc:
            st.error(
                f"Something went wrong while loading "
                f"{month['month_label']} data."
            )
            st.exception(exc)


with tabs[3]:
    render_gallery()

import streamlit as st  # type: ignore[import]
try:
    import pandas as pd  # type: ignore[import]
except ImportError:
    st.error("Required dependency 'pandas' is not installed. Install it with `pip install pandas`.")
    st.stop()
import plotly.express as px
from prophet import Prophet
import folium 
from streamlit_folium import st_folium

# Custom styling
st.markdown(
    """
    <style>
    .main {
        background-color: #1E1E1E;
        color: White;
    }
    h1, h2, h3 {
        color:#00ADB5;
    }
    .stMetric {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Dashboard title 
st.title("EpiPulse AI")
st.subheader("Disease Outbreak Monitoring Dashboard")
st.sidebar.title("EpiPulse Controls")

# Dasboard tabs

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Forecasting",
    "MAps",
    "Risk Analysis"
])

# Load Dataset
df=pd.read_csv("disease_dataset.csv")

# KPI Metrics
with tab1:
    col1, col2, col3 = st.columns(3)

# Total confirmed cases
    total_cases = df['Confirmed'].sum()

# Maximum deaths
    max_deaths = df['Deaths'].max()

# Maximum recoveries
    max_recovered = df['Recovered'].max()

# KPI Cards
    col1.metric(
    "Total Confirmed Cases",
    f"{total_cases:,}"
    )

    col2.metric(
    "Maximum Deaths",
    f"{max_deaths:,}"
    )

    col3.metric(
    "Maximum Recovered",
    f"{max_recovered:,}"
    )

    selected_rows = st.sidebar.slider(
        "Select Number of Rows",
        5,
        50,
        10
    )

    st.write(df.head(selected_rows))

#Show Dataset Preview
    st.write("Dataset Preview")
    st.dataframe(df.head(selected_rows))

# show available columns
    st.write("AvailableColumns:")
    st.write(df.columns)

#Select numeric columns
    numeric_columns = df.select_dtypes(include=['int64', 'float64']
    ).columns

# Sidebar instructions
    st.sidebar.title("EpiPuse AI Controls")

# Row Selector
    selected_rows = st.sidebar.slider(
        "Select Number of Rows",
        min_value=5,
        max_value=100,
        value=20
    )
# Column SElector
    sidebar_column = st.sidebar.selectbox(
        "Select Visualozation Column",
        numeric_columns
    )

# Dropdown menu
    selected_column = st.selectbox(
        "Select Data to Visualize",
        numeric_columns
    )

#create graph
    fig = px.line(
        df,
        y = sidebar_column,
        title = f"{sidebar_column} Trend Analysis"
    )

# Show graph
    st.plotly_chart(fig)

#Dataset Statistics
    st.subheader("Dataset Statistics")
    st.write(df.describe())

# Outbreak Detection
    st.subheader("Outbreak Detection Alerts")

# Select threshold column
    alert_column = st.selectbox(
        "Select Column for Alert Detection",
        numeric_columns
    )

# Calculate threshold
    mean_value = df[alert_column].mean()
    std_value = df[alert_column].std()

    threshold = mean_value + 2 *std_value

# Detect outbreaks rows
    outbreaks = df[df[alert_column] > threshold]

# Show threshhold
    st.write(f"Alert Threshold: {threshold:.2f}")

# Display alerts
    if len(outbreaks) > 0:
        st.error(
            f"⚠️ Potential Outbreak Detected in {alert_column}"
    )
        st.dataframe(outbreaks.head())
    else:
        st.success("✅ No Major Outbreaks Detected")

# Forecast Prediction 

with tab2:
    st.subheader("Future Outbreak Forecast")

# Prepare forecasting data
    forecast_df = df[['Date', 'Confirmed']]

# Rename columns for prophet
    forecast_df = forecast_df.rename(
        columns={
            'Date': 'ds',
            'Confirmed': 'y'
        }
    )

# Convert date column
    forecast_df['ds'] = pd.to_datetime(
        forecast_df['ds']
    )

# Create prophet model
    model = Prophet()

# Train model
    model.fit(forecast_df)

# Future dates
    future = model.make_future_dataframe(
        periods=30
    )

# Predict future
    prediction = model.predict(future)

# Show forecast
    st.write(prediction[['ds', 'yhat']].tail())

# plot forecast
    forecast_fig = px.line(
        prediction, 
        x='ds',
        y='yhat',
        title="30-Day Disease Forecast"
    )

    st.plotly_chart(forecast_fig)

# Geographic Outbreak Map

with tab3:
    st.subheader("Geographic Outbreak Map")

# Creating base map centered on India
    outbreak_map = folium.Map(
        location=[22.9734, 78.6569],
        zoom_start=5
    )

# Adding Markers
    folium.Marker(
        [28.6139, 77.2090],
        popups="Delhi Oubreak Zone",
        icon=folium.Icon(color='red')
    ).add_to(outbreak_map)
        
    folium.Marker(
        [19.0760, 72.8777],
        popups="Mumbai Risk Zone",
        icon=folium.Icon(color="red"),
    ).add_to(outbreak_map)

    folium.Marker(
        [13.0827, 80.2707],
        popups="Punjab Alert Zone",
        icon=folium.Icon(color="red")
    ).add_to(outbreak_map)

# Display map
    st_folium(outbreak_map, width=700, height=500)

# Risk Score Engine

with tab4:
    st.subheader("Outbreak Risk Analysis")

# Calculate risk score
    latest_cases = df[alert_column].iloc[-1]

    mean_cases = df[alert_column].mean()

    risk_percentage = (
        latest_cases / mean_cases
    ) * 50

# Limiting score to 100%
    risk_percentage = min(risk_percentage, 100)

# Show percentage
    st.metric(
        label="Current Outbreak Risk ",
        value=f"{risk_percentage:.1f}%"
    )

# Risk classification
    if risk_percentage < 40:
        st.success("🟢Low Risk Zone")

    elif risk_percentage < 70:
        st.warning("🟡Medium Risk Zone")
    else:
        st.error("🟠High Risk Zone")
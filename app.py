import plotly.express as px 
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

try:
    from sidebar import show_sidebar  # type: ignore[import]
except ImportError:
    def show_sidebar():
        st.sidebar.title("EpiPulse Controls")
        return None
    
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #0f172a, #111827);
    color: white;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.stButton>button {
    background: linear-gradient(90deg,#7c3aed,#06b6d4);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

h1,h2,h3 {
    color: white;
}

</style>
""", unsafe_allow_html=True)


menu = show_sidebar()
from fpdf import FPDF

st.set_page_config(
    page_title="EpiPulse AI",
    page_icon="🧠",
    layout="wide"
)

if menu == "🏠 Dashboard":
    st.title("🏠 EpiPulse AI Dashboard")

elif menu == "📊 Analytics":
    st.title("📊 Medical Analytics")

elif menu == "🧬 Predictions":
    st.title("🧬 Disease Predictions")

elif menu == "📄 Reports":
    st.title("📄 AI Reports")

elif menu == "⚙️ Settings":
    st.title("⚙️ System Settings")

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
    """,unsafe_allow_html=True
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

# Outbreak Trend Chart
chart_data = {
    "Category": ["Risk", "Safe"],
    "Value": [risk_percentage, 100 - risk_percentage]
}

fig = px.pie(
    values=chart_data["Value"],
    names=chart_data["Category"],
    title="Disease Risk Distribution",
    hole=0.5
)

st.plotly_chart(fig, use_container_width=True)

# Example prediction probabilities for disease analysis
disease_data = {
    "Disease": [
        "Diabetes",
        "Heart Disease",
        "Hypertension",
        "Asthma",
        "Stroke"
    ],
    "Probability": [
        82,
        65,
        48,
        30,
        15
    ]
}

disease_df = pd.DataFrame(disease_data)

# Top Predicted Diseases
top_disease = disease_df.iloc[0]["Disease"]
top_probability = disease_df.iloc[0]["Probability"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Risk %", f"{risk_percentage:.1f}%")

with col2:
    st.metric("Predicted Disease", top_disease)

with col3:
    st.metric("Confidence", f"{top_probability}%")

# Risk Analysis Interprtation
st.markdown("## 🧠 AI Risk Analysis")

if risk_percentage < 40:
    risk_color = "#22c55e"
    risk_text = "🟢 Low Risk Zone"
    risk_message = "Patient condition appears stable."

elif risk_percentage < 70:
    risk_color = "#facc15"
    risk_text = "🟡 Medium Risk Zone"
    risk_message = "Patient may require medical attention."

else:
    risk_color = "#ef4444"
    risk_text = "🔴 High Risk Zone"
    risk_message = "Immediate medical attention recommended."

# Stylish Risk Card
if risk_percentage < 40:
    st.markdown(f"""
                <div style="
        background-color:#22c55e20;
        padding:20px;
        border-radius:15px;
        border-left:6px solid #22c55e;
    ">
        <h3>{risk_text}</h3>
        <p>{risk_message}</p>
    </div>
    """, unsafe_allow_html=True)

elif risk_percentage < 70:
    st.markdown(f"""
                <div style="
        background-color:#facc1520;
        padding:20px;
        border-radius:15px;
        border-left:6px solid #facc15;
    ">
        <h3>{risk_text}</h3>
        <p>{risk_message}</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown(f"""
         <div style="
        background-color:#ef444420;
        padding:20px;
        border-radius:15px;
        border-left:6px solid #ef4444;
    ">
        <h3>{risk_text}</h3>
        <p>{risk_message}</p>
    </div>
    """, unsafe_allow_html=True)
   

    st.progress(int(risk_percentage))

    st.caption(f"AI Confidence Score: {risk_percentage:.1f}%")

    import pandas as pd

# Example prediction probabilities
    disease_data = {
    "Disease": [
        "Diabetes",
        "Heart Disease",
        "Hypertension",
        "Asthma",
        "Stroke"
    ],
    
    "Probability": [
        82,
        65,
        48,
        30,
        15
    ]
}

    df = pd.DataFrame(disease_data)

    st.markdown("## 📊 Disease Prediction Analysis")

    st.bar_chart(
        data=df.set_index("Disease")
    )

# Top Predicted Diseases

    top_disease = df.iloc[0]["Disease"]
    top_probability = df.iloc[0]["Probability"]

    st.markdown(f"""
    <div style="
        background:#111827;
        padding:20px;
        border-radius:18px;
        color:white;
        margin-top:20px;
    ">
        <h2>🧬 Most Likely Condition</h2>
        <h1>{top_disease}</h1>
        <h3>Prediction Confidence: {top_probability}%</h3>
    </div>
    """, unsafe_allow_html=True)

# PDF Report function

    def generate_report():

        pdf = FPDF()

        pdf.add_page()

        pdf.set_font("Arial", size=16)

        pdf.cell(200, 10,
                txt="EpiPulse AI Medical Report",
                ln=True,
                align='C')

        pdf.ln(10)

        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10,
                txt=f"Risk Percentage: {risk_percentage:.1f}%",
                ln=True)

        pdf.cell(200, 10,
                txt=f"Top Predicted Disease: {top_disease}",
                ln=True)

        pdf.cell(200, 10,
                txt=f"Prediction Confidence: {top_probability}%",
                ln=True)

        pdf.output("EpiPulse_Report.pdf")


# Download Report Button


    if st.button("📄 Generate AI Report"):

        generate_report()

        with open("EpiPulse_Report.pdf", "rb") as file:

            st.download_button(
                label="⬇ Download Report",
                data=file,
                file_name="EpiPulse_Report.pdf",
                mime="application/pdf"
            )
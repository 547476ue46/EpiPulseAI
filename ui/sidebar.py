import streamlit as st

def show_sidebar():

    with st.sidebar:

        st.markdown("""
        <h1 style='text-align:center; color:#4ade80;'>
        🧠 EpiPulse AI
        </h1>
        """, unsafe_allow_html=True)

        st.markdown("---")

        menu = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "📊 Analytics",
                "🧬 Predictions",
                "📄 Reports",
                "⚙️ Settings"
            ]
        )

        st.markdown("---")

        st.markdown("""
        <div style="
        padding:15px;
        border-radius:15px;
        background:#111827;
        color:white;
        text-align:center;
        ">
        🚀 AI Healthcare System
        <br><br>
        Version 1.0
        </div>
        """, unsafe_allow_html=True)

    return menu
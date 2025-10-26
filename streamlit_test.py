"""
Simple test app for Streamlit Cloud deployment
"""
import streamlit as st
import requests

st.title("🌍 Earthquake Monitor Test")
st.write("Testing Streamlit Cloud deployment...")

try:
    # Test USGS API connection
    response = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson", timeout=5)
    if response.status_code == 200:
        data = response.json()
        earthquake_count = len(data['features'])
        st.success(f"✅ Successfully connected to USGS API")
        st.write(f"Found {earthquake_count} earthquakes in the past hour worldwide")
    else:
        st.error(f"❌ API Error: Status {response.status_code}")
except Exception as e:
    st.error(f"❌ Connection Error: {e}")

st.write("If you see this, Streamlit Cloud deployment is working!")
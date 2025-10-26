"""
Simple USGS Earthquake Monitor - Mobile Web App
Working version without complex modules
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np

# Configure page
st.set_page_config(
    page_title="🌍 USGS Earthquake Monitor", 
    page_icon="🌍",
    layout="wide"
)

# CSS styling
st.markdown("""
<style>
    .main > div { padding-top: 1rem; }
    .stButton > button { width: 100%; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def fetch_earthquake_data(feed_type="all_hour"):
    """Fetch earthquake data from USGS"""
    url = f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{feed_type}.geojson"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        earthquakes = []
        for feature in data['features']:
            props = feature['properties']
            coords = feature['geometry']['coordinates']
            
            # Filter for USA earthquakes
            longitude, latitude = coords[0], coords[1]
            if -180 <= longitude <= -60 and 15 <= latitude <= 75:
                earthquakes.append({
                    'magnitude': props.get('mag', 0),
                    'place': props.get('place', 'Unknown'),
                    'time': props.get('time', 0),
                    'depth': coords[2] if len(coords) > 2 else 0,
                    'longitude': longitude,
                    'latitude': latitude
                })
        
        return earthquakes
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

def create_map(earthquakes):
    """Create earthquake map"""
    if not earthquakes:
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] > 0]
    if not valid_earthquakes:
        return
    
    df = pd.DataFrame(valid_earthquakes)
    
    fig = px.scatter_map(
        df,
        lat="latitude",
        lon="longitude", 
        size="magnitude",
        color="magnitude",
        hover_name="place",
        color_continuous_scale="Reds",
        zoom=3,
        height=400,
        title="🗺️ US Earthquake Activity"
    )
    
    fig.update_layout(
        map_style="open-street-map",
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_stats(earthquakes):
    """Show earthquake statistics"""
    if not earthquakes:
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] > 0]
    if not valid_earthquakes:
        return
    
    magnitudes = [eq['magnitude'] for eq in valid_earthquakes]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Earthquakes", len(valid_earthquakes))
    
    with col2:
        st.metric("Max Magnitude", f"M {max(magnitudes):.1f}")
    
    with col3:
        st.metric("Avg Magnitude", f"M {np.mean(magnitudes):.1f}")

def main():
    """Main application"""
    st.title("🌍 USGS Earthquake Monitor")
    st.write("Real-time earthquake monitoring for mobile devices")
    
    # Navigation
    st.subheader("📡 Select Data Source")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🕐 Past Hour"):
            st.session_state.feed_type = "all_hour"
        if st.button("📅 Past Day"):
            st.session_state.feed_type = "all_day"
    
    with col2:
        if st.button("🌍 Past Week"): 
            st.session_state.feed_type = "all_week"
        if st.button("🌋 Major Quakes"):
            st.session_state.feed_type = "4.5_week"
    
    # Initialize session state
    if 'feed_type' not in st.session_state:
        st.session_state.feed_type = "all_hour"
    
    # Fetch and display data
    with st.spinner("📡 Loading earthquake data..."):
        earthquakes = fetch_earthquake_data(st.session_state.feed_type)
    
    if earthquakes:
        st.success(f"✅ Found {len(earthquakes)} earthquakes")
        
        show_stats(earthquakes)
        create_map(earthquakes)
        
        # Show recent earthquakes
        st.subheader("📋 Recent Earthquakes")
        valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] > 0]
        
        for eq in sorted(valid_earthquakes, key=lambda x: x['magnitude'], reverse=True)[:5]:
            time_dt = datetime.fromtimestamp(eq['time']/1000)
            time_str = time_dt.strftime("%m/%d %H:%M")
            
            st.markdown(f"""
            **M {eq['magnitude']:.1f}** - {eq['place']}  
            *{time_str} | Depth: {eq['depth']:.1f}km*
            """)
    else:
        st.warning("⚠️ No earthquake data available")
    
    # Footer
    st.markdown("---")
    st.markdown("📡 Data from USGS Earthquake Hazards Program")

if __name__ == "__main__":
    main()
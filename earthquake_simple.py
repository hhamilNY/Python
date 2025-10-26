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
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS styling
st.markdown("""
<style>
    .main > div { 
        padding-top: 1rem; 
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton > button { 
        width: 100%; 
    }
    .element-container {
        margin: 0 auto;
    }
    .stSelectbox > div > div {
        margin: 0 auto;
    }
    .stSlider > div {
        margin: 0 auto;
    }
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .stMetric {
        text-align: center;
    }
    h1, h2, h3 {
        text-align: center;
    }
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
    # Centered title with better styling
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🌍 USGS Earthquake Monitor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #666;'>Real-time earthquake monitoring for mobile devices</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Select View dropdown
    st.markdown("<h3 style='text-align: center;'>📡 Select Data Source</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🕐 Past Hour"):
            st.session_state.feed_type = "all_hour"
        if st.button("📅 Past Day"):
            st.session_state.feed_type = "all_day"
        if st.button("🌍 Past Week"):
            st.session_state.feed_type = "all_week"
    
    with col2:
        if st.button("📆 Past Month"):
            st.session_state.feed_type = "all_month"
        if st.button("🌋 Major Quakes (4.5+)"):
            st.session_state.feed_type = "4.5_week"
        if st.button("⚠️ Significant Events"):
            st.session_state.feed_type = "significant_month"
    
    # Initialize session state
    if 'feed_type' not in st.session_state:
        st.session_state.feed_type = "all_hour"
    
    # Get feed type from session state
    feed_type = st.session_state.feed_type
    
    # Select View options
    st.markdown("<h3 style='text-align: center;'>📊 Select View</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        min_magnitude = st.slider(
            "Minimum Magnitude",
            min_value=0.0,
            max_value=7.0,
            value=0.0,
            step=0.1,
            help="Filter earthquakes by minimum magnitude"
        )
    
    with col2:
        show_recent = st.checkbox("Show Recent List", value=True, help="Display list of recent earthquakes")
        show_map = st.checkbox("Show Map", value=True, help="Display earthquake map")
    
    # Fetch and display data
    with st.spinner("📡 Loading earthquake data..."):
        earthquakes = fetch_earthquake_data(feed_type)
    
    # Apply magnitude filter
    if min_magnitude > 0.0:
        earthquakes = [eq for eq in earthquakes if eq.get('magnitude', 0) >= min_magnitude]
    
    if earthquakes:
        # Show current selection info
        current_selection = {
            "all_hour": "🕐 Past Hour",
            "all_day": "📅 Past Day", 
            "all_week": "🌍 Past Week",
            "all_month": "📆 Past Month",
            "4.5_week": "🌋 Major Quakes (4.5+)",
            "significant_month": "⚠️ Significant Events"
        }
        
        selected_name = current_selection.get(feed_type, "Unknown")
        st.info(f"📊 Showing: **{selected_name}** | Minimum Magnitude: **M {min_magnitude}**")
        st.success(f"✅ Found {len(earthquakes)} earthquakes")
        
        show_stats(earthquakes)
        
        if show_map:
            create_map(earthquakes)
        
        # Show recent earthquakes
        if show_recent:
            st.markdown("<h3 style='text-align: center;'>📋 Recent Earthquakes</h3>", unsafe_allow_html=True)
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
    st.markdown("<p style='text-align: center; color: #888;'>📡 Data from USGS Earthquake Hazards Program</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
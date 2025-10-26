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
    
    # Select View dropdown
    st.subheader("📡 Select View")
    
    feed_options = {
        "🕐 Past Hour": "all_hour",
        "� Past Day": "all_day", 
        "🌍 Past Week": "all_week",
        "� Past Month": "all_month",
        "🌋 Major Quakes (4.5+ Week)": "4.5_week",
        "⚠️ Significant Events (Month)": "significant_month",
        "🔍 Magnitude 2.5+ (Week)": "2.5_week"
    }
    
    selected_view = st.selectbox(
        "Choose earthquake data timeframe:",
        options=list(feed_options.keys()),
        index=0,
        help="Select the time period and magnitude range for earthquake data"
    )
    
    # Get feed type from selection
    feed_type = feed_options[selected_view]
    
    # Magnitude filter
    st.subheader("🎛️ Filters")
    min_magnitude = st.slider(
        "Minimum Magnitude",
        min_value=0.0,
        max_value=7.0,
        value=0.0,
        step=0.1,
        help="Filter earthquakes by minimum magnitude"
    )
    
    # Fetch and display data
    with st.spinner("📡 Loading earthquake data..."):
        earthquakes = fetch_earthquake_data(feed_type)
    
    # Apply magnitude filter
    if min_magnitude > 0.0:
        earthquakes = [eq for eq in earthquakes if eq.get('magnitude', 0) >= min_magnitude]
    
    if earthquakes:
        # Show current selection info
        st.info(f"📊 Showing: **{selected_view}** | Minimum Magnitude: **M {min_magnitude}**")
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
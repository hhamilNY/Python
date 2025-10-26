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
def fetch_earthquake_data(feed_type="all_hour", region="usa"):
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
            
            longitude, latitude = coords[0], coords[1]
            
            # Regional filtering
            include_earthquake = False
            if region == "usa":
                # USA and territories
                if -180 <= longitude <= -60 and 15 <= latitude <= 75:
                    include_earthquake = True
            elif region == "california":
                # California region
                if -125 <= longitude <= -114 and 32 <= latitude <= 42:
                    include_earthquake = True
            elif region == "alaska":
                # Alaska region
                if -180 <= longitude <= -130 and 54 <= latitude <= 72:
                    include_earthquake = True
            elif region == "pacific":
                # Pacific Ring of Fire
                if -180 <= longitude <= -110 and -60 <= latitude <= 60:
                    include_earthquake = True
            elif region == "global":
                # Global earthquakes
                include_earthquake = True
            elif region == "west_coast":
                # US West Coast
                if -130 <= longitude <= -115 and 30 <= latitude <= 50:
                    include_earthquake = True
            
            if include_earthquake:
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

def create_map(earthquakes, region="usa"):
    """Create earthquake map with enhanced hover information"""
    if not earthquakes:
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] > 0]
    if not valid_earthquakes:
        return
    
    df = pd.DataFrame(valid_earthquakes)
    
    # Add formatted datetime and enhanced hover information
    df['datetime'] = df['time'].apply(lambda x: datetime.fromtimestamp(x/1000).strftime("%m/%d/%Y %H:%M:%S UTC"))
    df['magnitude_display'] = df['magnitude'].apply(lambda x: f"M {x:.1f}")
    df['depth_display'] = df['depth'].apply(lambda x: f"{x:.1f} km")
    df['coordinates'] = df.apply(lambda row: f"{row['latitude']:.3f}°, {row['longitude']:.3f}°", axis=1)
    
    # Create magnitude categories for color coding
    df['mag_category'] = df['magnitude'].apply(lambda x: 
        'Major (5.0+)' if x >= 5.0 else
        'Light (4.0-4.9)' if x >= 4.0 else
        'Minor (3.0-3.9)' if x >= 3.0 else
        'Micro (0-2.9)'
    )
    
    # Set zoom and center based on region
    zoom_settings = {
        "usa": {"zoom": 3, "center": {"lat": 39.8, "lon": -98.5}},
        "california": {"zoom": 6, "center": {"lat": 36.7, "lon": -119.7}},
        "alaska": {"zoom": 4, "center": {"lat": 64.0, "lon": -153.0}},
        "west_coast": {"zoom": 5, "center": {"lat": 40.0, "lon": -122.0}},
        "pacific": {"zoom": 2, "center": {"lat": 0.0, "lon": -140.0}},
        "global": {"zoom": 1, "center": {"lat": 0.0, "lon": 0.0}}
    }
    
    zoom_config = zoom_settings.get(region, zoom_settings["usa"])
    
    fig = px.scatter_map(
        df,
        lat="latitude",
        lon="longitude", 
        size="magnitude",
        color="magnitude",
        hover_name="place",
        hover_data={
            "magnitude_display": True,
            "depth_display": True,
            "datetime": True,
            "coordinates": True,
            "mag_category": True,
            "magnitude": False,  # Hide raw magnitude
            "depth": False,      # Hide raw depth
            "time": False,       # Hide raw time
            "latitude": False,   # Hide raw coordinates
            "longitude": False
        },
        color_continuous_scale="Reds",
        zoom=zoom_config["zoom"],
        center=zoom_config["center"],
        height=400,
        title=f"🗺️ Earthquake Activity - {region.replace('_', ' ').title()}",
        labels={
            "magnitude_display": "Magnitude",
            "depth_display": "Depth",
            "datetime": "Event Time",
            "coordinates": "Location",
            "mag_category": "Category"
        }
    )
    
    fig.update_layout(
        map_style="open-street-map",
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_stats(earthquakes, region="USA"):
    """Show comprehensive earthquake statistics"""
    if not earthquakes:
        st.warning("⚠️ No earthquake data available for statistics")
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] > 0]
    if not valid_earthquakes:
        st.warning("⚠️ No valid earthquake data for statistics")
        return
    
    magnitudes = [eq['magnitude'] for eq in valid_earthquakes]
    depths = [eq['depth'] for eq in valid_earthquakes]
    times = [eq['time'] for eq in valid_earthquakes]
    
    # Basic Statistics Row
    st.markdown("<h4 style='text-align: center;'>📊 Basic Statistics</h4>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Events", len(valid_earthquakes))
    
    with col2:
        st.metric("Max Magnitude", f"M {max(magnitudes):.1f}")
    
    with col3:
        st.metric("Avg Magnitude", f"M {np.mean(magnitudes):.1f}")
    
    with col4:
        st.metric("Avg Depth", f"{np.mean(depths):.1f} km")
    
    # Magnitude Categories
    st.markdown("<h4 style='text-align: center;'>🌋 Magnitude Categories</h4>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    micro = len([m for m in magnitudes if 0 <= m < 3.0])
    minor = len([m for m in magnitudes if 3.0 <= m < 4.0])
    light = len([m for m in magnitudes if 4.0 <= m < 5.0])
    moderate_plus = len([m for m in magnitudes if m >= 5.0])
    
    with col1:
        st.metric("🔸 Micro (0-2.9)", micro, help="Usually not felt")
    
    with col2:
        st.metric("🔹 Minor (3.0-3.9)", minor, help="Rarely felt")
    
    with col3:
        st.metric("🟠 Light (4.0-4.9)", light, help="Often felt, little damage")
    
    with col4:
        st.metric("🔴 Moderate+ (5.0+)", moderate_plus, help="Can cause damage")
    
    # Depth Analysis
    st.markdown("<h4 style='text-align: center;'>🕳️ Depth Analysis</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    shallow = len([d for d in depths if 0 <= d < 70])
    intermediate = len([d for d in depths if 70 <= d < 300])
    deep = len([d for d in depths if d >= 300])
    
    with col1:
        st.metric("Shallow (0-70km)", shallow, help="Most damaging earthquakes")
    
    with col2:
        st.metric("Intermediate (70-300km)", intermediate, help="Moderate depth")
    
    with col3:
        st.metric("Deep (300km+)", deep, help="Rarely cause surface damage")
    
    # Recent Activity
    if times:
        latest_time = max(times)
        latest_dt = datetime.fromtimestamp(latest_time/1000)
        time_ago = datetime.now() - latest_dt
        
        st.markdown("<h4 style='text-align: center;'>⏰ Recent Activity</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Latest Event", latest_dt.strftime("%m/%d %H:%M"))
        
        with col2:
            hours_ago = int(time_ago.total_seconds() / 3600)
            st.metric("Hours Ago", f"{hours_ago}h")

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
        
        region_options = {
            "🇺🇸 USA": "usa",
            "🌴 California": "california", 
            "❄️ Alaska": "alaska",
            "🌊 US West Coast": "west_coast",
            "🌋 Pacific Ring": "pacific",
            "🌍 Global": "global"
        }
        
        selected_region = st.selectbox(
            "Region",
            options=list(region_options.keys()),
            index=0,
            help="Select geographic region to monitor"
        )
        
        region = region_options[selected_region]
    
    with col2:
        show_stats_toggle = st.checkbox("Show Statistics", value=True, help="Display detailed earthquake statistics")
        show_recent = st.checkbox("Show Recent List", value=True, help="Display list of recent earthquakes")
        show_map = st.checkbox("Show Map", value=True, help="Display earthquake map")
    
    # Fetch and display data
    with st.spinner("📡 Loading earthquake data..."):
        earthquakes = fetch_earthquake_data(feed_type, region)
    
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
        st.info(f"📊 **{selected_name}** | 🌍 **{selected_region}** | Min Magnitude: **M {min_magnitude}**")
        st.success(f"✅ Found {len(earthquakes)} earthquakes")
        
        if show_stats_toggle:
            show_stats(earthquakes, selected_region)
        
        if show_map:
            create_map(earthquakes, region)
        
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
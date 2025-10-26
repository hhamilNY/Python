"""
USGS Earthquake Monitor - Professional Mobile Web App
Advanced features with comprehensive analytics and monitoring
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import json
import os
from pathlib import Path
import logging

# Configure page
st.set_page_config(
    page_title="🌍 Advanced Earthquake Monitor", 
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Advanced CSS styling
st.markdown("""
<style>
    .main > div { 
        padding-top: 1rem; 
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton > button { 
        width: 100%; 
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .active-button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
        color: white !important;
        border: 2px solid #20c997 !important;
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    .inactive-button {
        background: linear-gradient(135deg, #6c757d 0%, #495057 100%) !important;
        color: white !important;
        border: 1px solid #6c757d !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .admin-panel {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    h1, h2, h3, h4 {
        text-align: center;
        color: #2c3e50;
    }
    .stSelectbox > div > div {
        border-radius: 20px;
    }
    .stSlider > div {
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
if 'page_views' not in st.session_state:
    st.session_state.page_views = 0
if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False

st.session_state.page_views += 1

@st.cache_data(ttl=300)
def fetch_earthquake_data(feed_type="all_hour", region="usa"):
    """Fetch earthquake data from USGS with regional filtering"""
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
                if -180 <= longitude <= -60 and 15 <= latitude <= 75:
                    include_earthquake = True
            elif region == "california":
                if -125 <= longitude <= -114 and 32 <= latitude <= 42:
                    include_earthquake = True
            elif region == "alaska":
                if -180 <= longitude <= -130 and 54 <= latitude <= 72:
                    include_earthquake = True
            elif region == "pacific":
                if -180 <= longitude <= -110 and -60 <= latitude <= 60:
                    include_earthquake = True
            elif region == "global":
                include_earthquake = True
            elif region == "west_coast":
                if -130 <= longitude <= -115 and 30 <= latitude <= 50:
                    include_earthquake = True
            
            if include_earthquake:
                earthquakes.append({
                    'magnitude': props.get('mag', 0),
                    'place': props.get('place', 'Unknown'),
                    'time': props.get('time', 0),
                    'depth': coords[2] if len(coords) > 2 else 0,
                    'longitude': longitude,
                    'latitude': latitude,
                    'alert': props.get('alert'),
                    'tsunami': props.get('tsunami', 0),
                    'url': props.get('url', '')
                })
        
        return earthquakes
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

def create_advanced_map(earthquakes, region="usa"):
    """Create enhanced earthquake map with comprehensive hover info"""
    if not earthquakes:
        st.warning("⚠️ No earthquake data available for map")
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] > 0]
    if not valid_earthquakes:
        st.warning("⚠️ No valid earthquake data for map")
        return
    
    df = pd.DataFrame(valid_earthquakes)
    
    # Enhanced data formatting
    df['datetime'] = df['time'].apply(lambda x: datetime.fromtimestamp(x/1000).strftime("%m/%d/%Y %H:%M:%S UTC"))
    df['magnitude_display'] = df['magnitude'].apply(lambda x: f"M {x:.1f}")
    df['depth_display'] = df['depth'].apply(lambda x: f"{x:.1f} km")
    df['coordinates'] = df.apply(lambda row: f"{row['latitude']:.3f}°, {row['longitude']:.3f}°", axis=1)
    df['mag_category'] = df['magnitude'].apply(lambda x: 
        'Major (5.0+)' if x >= 5.0 else
        'Light (4.0-4.9)' if x >= 4.0 else
        'Minor (3.0-3.9)' if x >= 3.0 else
        'Micro (0-2.9)'
    )
    
    # Alert status
    df['alert_status'] = df['alert'].fillna('None').apply(lambda x: 
        '🔴 Red Alert' if x == 'red' else
        '🟠 Orange Alert' if x == 'orange' else
        '🟡 Yellow Alert' if x == 'yellow' else
        '🟢 Green Alert' if x == 'green' else
        '⚪ No Alert'
    )
    
    # Regional zoom settings
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
            "alert_status": True,
            "magnitude": False,
            "depth": False,
            "time": False,
            "latitude": False,
            "longitude": False,
            "alert": False
        },
        color_continuous_scale="Reds",
        zoom=zoom_config["zoom"],
        center=zoom_config["center"],
        height=500,
        title=f"🗺️ Advanced Earthquake Monitor - {region.replace('_', ' ').title()}",
        labels={
            "magnitude_display": "Magnitude",
            "depth_display": "Depth",
            "datetime": "Event Time",
            "coordinates": "Location",
            "mag_category": "Category",
            "alert_status": "Alert Level"
        }
    )
    
    fig.update_layout(
        map_style="open-street-map",
        margin=dict(l=0, r=0, t=40, b=0),
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_advanced_stats(earthquakes, region="USA"):
    """Display comprehensive earthquake statistics with visualizations"""
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
    
    # Enhanced Statistics Dashboard
    st.markdown("<h3 style='text-align: center; color: #2c3e50;'>📊 Advanced Statistics Dashboard</h3>", unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🌍 Total Events", len(valid_earthquakes))
    
    with col2:
        st.metric("🔥 Max Magnitude", f"M {max(magnitudes):.1f}")
    
    with col3:
        st.metric("📊 Avg Magnitude", f"M {np.mean(magnitudes):.1f}")
    
    with col4:
        st.metric("🕳️ Avg Depth", f"{np.mean(depths):.1f} km")
    
    with col5:
        significant = len([m for m in magnitudes if m >= 4.0])
        st.metric("⚠️ Significant", significant)
    
    # Magnitude Distribution Chart
    st.markdown("<h4 style='text-align: center;'>📈 Magnitude Distribution</h4>", unsafe_allow_html=True)
    
    fig_hist = px.histogram(
        x=magnitudes,
        nbins=20,
        title="Earthquake Magnitude Distribution",
        labels={"x": "Magnitude", "y": "Count"},
        color_discrete_sequence=["#e74c3c"]
    )
    fig_hist.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Depth vs Magnitude Scatter
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4 style='text-align: center;'>🎯 Depth vs Magnitude</h4>", unsafe_allow_html=True)
        fig_scatter = px.scatter(
            x=depths, y=magnitudes,
            labels={"x": "Depth (km)", "y": "Magnitude"},
            color=magnitudes,
            color_continuous_scale="Reds",
            title="Earthquake Depth vs Magnitude"
        )
        fig_scatter.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.markdown("<h4 style='text-align: center;'>⏰ Timeline</h4>", unsafe_allow_html=True)
        
        # Convert timestamps to datetime for timeline
        timeline_data = []
        for i, t in enumerate(times):
            dt = datetime.fromtimestamp(t/1000)
            timeline_data.append({
                'time': dt,
                'magnitude': magnitudes[i],
                'hour': dt.strftime('%H:00')
            })
        
        df_timeline = pd.DataFrame(timeline_data)
        
        if len(df_timeline) > 0:
            # Group by hour for timeline chart
            hourly = df_timeline.groupby('hour').size().reset_index(name='count')
            
            fig_timeline = px.bar(
                hourly, x='hour', y='count',
                title="Earthquakes by Hour",
                labels={"hour": "Hour (UTC)", "count": "Count"},
                color_discrete_sequence=["#3498db"]
            )
            fig_timeline.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_timeline, use_container_width=True)

def show_admin_panel():
    """Admin dashboard with session analytics"""
    st.markdown("""
    <div class="admin-panel">
        <h3 style='margin: 0; text-align: center;'>🔧 Admin Dashboard</h3>
        <p style='margin: 0.5rem 0; text-align: center;'>Session Analytics & System Status</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Session ID", st.session_state.session_id[-8:])
    
    with col2:
        st.metric("Page Views", st.session_state.page_views)
    
    with col3:
        current_time = datetime.now().strftime("%H:%M:%S")
        st.metric("Current Time", current_time)
    
    # System status
    st.markdown("<h4 style='text-align: center;'>🖥️ System Status</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ USGS API: Connected")
        st.success("✅ Streamlit: Running")
    
    with col2:
        st.info("📡 Data Cache: 5 minutes")
        st.info("🌍 Regions: 6 available")

def main():
    """Advanced earthquake monitoring application"""
    # Enhanced header
    st.markdown("""
    <div style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin-bottom: 2rem;'>
        <h1 style='margin: 0; font-size: 2.5rem;'>🌍 Advanced Earthquake Monitor</h1>
        <p style='margin: 0.5rem 0; font-size: 1.2rem;'>Professional real-time seismic monitoring system</p>
        <p style='margin: 0; opacity: 0.8;'>Powered by USGS • Real-time Data • Global Coverage</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin toggle
    if st.sidebar.button("🔧 Toggle Admin Mode"):
        st.session_state.admin_mode = not st.session_state.admin_mode
    
    if st.session_state.admin_mode:
        show_admin_panel()
        st.markdown("---")
    
    # Data Source Selection
    st.markdown("<h3 style='text-align: center;'>📡 Data Source Selection</h3>", unsafe_allow_html=True)
    
    # Initialize session state
    if 'feed_type' not in st.session_state:
        st.session_state.feed_type = "all_hour"
    
    # Show current selection
    current_selection = {
        "all_hour": "🕐 Past Hour",
        "all_day": "📅 Past Day", 
        "all_week": "🌍 Past Week",
        "all_month": "📆 Past Month",
        "4.5_week": "🌋 Major Quakes (4.5+)",
        "significant_month": "⚠️ Significant Events"
    }
    
    selected_name = current_selection.get(st.session_state.feed_type, "Unknown")
    st.info(f"🎯 **Currently Selected:** {selected_name}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create buttons with active state styling
        if st.button("🕐 Past Hour", key="hour", 
                    type="primary" if st.session_state.feed_type == "all_hour" else "secondary"):
            st.session_state.feed_type = "all_hour"
            st.rerun()
        if st.button("📅 Past Day", key="day",
                    type="primary" if st.session_state.feed_type == "all_day" else "secondary"):
            st.session_state.feed_type = "all_day"
            st.rerun()
        if st.button("🌍 Past Week", key="week",
                    type="primary" if st.session_state.feed_type == "all_week" else "secondary"):
            st.session_state.feed_type = "all_week"
            st.rerun()
    
    with col2:
        if st.button("📆 Past Month", key="month",
                    type="primary" if st.session_state.feed_type == "all_month" else "secondary"):
            st.session_state.feed_type = "all_month"
            st.rerun()
        if st.button("🌋 Major Quakes (4.5+)", key="major",
                    type="primary" if st.session_state.feed_type == "4.5_week" else "secondary"):
            st.session_state.feed_type = "4.5_week"
            st.rerun()
        if st.button("⚠️ Significant Events", key="significant",
                    type="primary" if st.session_state.feed_type == "significant_month" else "secondary"):
            st.session_state.feed_type = "significant_month"
            st.rerun()
    
    feed_type = st.session_state.feed_type
    
    # Advanced View Controls
    st.markdown("<h3 style='text-align: center;'>🎛️ Advanced Controls</h3>", unsafe_allow_html=True)
    
    # Show current view settings (after session state is initialized)
    view_status = []
    if hasattr(st.session_state, 'show_stats') and st.session_state.show_stats:
        view_status.append("📊 Statistics")
    if hasattr(st.session_state, 'show_charts') and st.session_state.show_charts:
        view_status.append("📈 Charts")
    if hasattr(st.session_state, 'show_map') and st.session_state.show_map:
        view_status.append("🗺️ Map")
    if hasattr(st.session_state, 'show_recent') and st.session_state.show_recent:
        view_status.append("📋 Recent List")
    
    if view_status:
        st.info(f"🎮 **Active Views:** {' • '.join(view_status)}")
    else:
        st.warning("⚠️ No views enabled - select display options below")
    
    col1, col2 = st.columns(2)
    
    with col1:
        min_magnitude = st.slider(
            "🎯 Minimum Magnitude",
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
            "🌍 Geographic Region",
            options=list(region_options.keys()),
            index=0,
            help="Select geographic region to monitor"
        )
        
        region = region_options[selected_region]
    
    with col2:
        # Initialize view toggle states
        if 'show_stats' not in st.session_state:
            st.session_state.show_stats = True
        if 'show_charts' not in st.session_state:
            st.session_state.show_charts = True
        if 'show_map' not in st.session_state:
            st.session_state.show_map = True
        if 'show_recent' not in st.session_state:
            st.session_state.show_recent = True
        
        # Toggle buttons with active states
        if st.button("📊 Show Statistics", key="stats_toggle",
                    type="primary" if st.session_state.show_stats else "secondary"):
            st.session_state.show_stats = not st.session_state.show_stats
            st.rerun()
            
        if st.button("📈 Show Charts", key="charts_toggle",
                    type="primary" if st.session_state.show_charts else "secondary"):
            st.session_state.show_charts = not st.session_state.show_charts
            st.rerun()
            
        if st.button("🗺️ Show Map", key="map_toggle",
                    type="primary" if st.session_state.show_map else "secondary"):
            st.session_state.show_map = not st.session_state.show_map
            st.rerun()
            
        if st.button("📋 Show Recent List", key="recent_toggle",
                    type="primary" if st.session_state.show_recent else "secondary"):
            st.session_state.show_recent = not st.session_state.show_recent
            st.rerun()
        
        # Use session state values
        show_stats_toggle = st.session_state.show_stats
        show_charts_toggle = st.session_state.show_charts
        show_map_toggle = st.session_state.show_map
        show_recent_toggle = st.session_state.show_recent
    
    # Fetch and process data
    with st.spinner("📡 Loading advanced earthquake data..."):
        earthquakes = fetch_earthquake_data(feed_type, region)
    
    # Apply magnitude filter
    if min_magnitude > 0.0:
        earthquakes = [eq for eq in earthquakes if eq.get('magnitude', 0) >= min_magnitude]
    
    if earthquakes:
        # Status display
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
        
        # Conditional displays based on toggles
        if show_stats_toggle:
            show_advanced_stats(earthquakes, selected_region)
        
        if show_map_toggle:
            create_advanced_map(earthquakes, region)
        
        # Recent earthquakes list
        if show_recent_toggle:
            st.markdown("<h3 style='text-align: center;'>📋 Recent Earthquake Events</h3>", unsafe_allow_html=True)
            valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] > 0]
            
            for i, eq in enumerate(sorted(valid_earthquakes, key=lambda x: x['magnitude'], reverse=True)[:10]):
                time_dt = datetime.fromtimestamp(eq['time']/1000)
                time_str = time_dt.strftime("%m/%d %H:%M")
                
                # Enhanced earthquake display with color coding
                mag_color = (
                    "🔴" if eq['magnitude'] >= 5.0 else
                    "🟠" if eq['magnitude'] >= 4.0 else
                    "🟡" if eq['magnitude'] >= 3.0 else
                    "🔵"
                )
                
                alert_info = ""
                if eq.get('alert'):
                    alert_info = f" | Alert: {eq['alert'].upper()}"
                
                tsunami_info = ""
                if eq.get('tsunami'):
                    tsunami_info = " | ⚠️ TSUNAMI"
                
                st.markdown(f"""
                **{mag_color} M {eq['magnitude']:.1f}** - {eq['place']}  
                *{time_str} | Depth: {eq['depth']:.1f}km{alert_info}{tsunami_info}*
                """)
                
                if i < 9:  # Add separator except for last item
                    st.markdown("---")
    else:
        st.warning("⚠️ No earthquake data available for the selected criteria")
    
    # Enhanced footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin-top: 2rem;'>
        <p style='margin: 0; color: #6c757d;'>
            📡 <strong>Data Source:</strong> USGS Earthquake Hazards Program<br>
            🔄 <strong>Update Frequency:</strong> Real-time (5-minute cache)<br>
            💻 <strong>Built with:</strong> Streamlit • Plotly • Python
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
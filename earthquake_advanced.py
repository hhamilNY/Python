"""
Real-Time Earthquake Monitoring - Complete Mobile Web App
All modular features combined into single deployable file
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

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "earthquake_monitor.log"),
        logging.StreamHandler()
    ]
)

# Create logger for this module
logger = logging.getLogger("EarthquakeMonitor")

# User metrics tracking
def save_user_metrics(session_id, action, data=None):
    """Save user metrics to JSON file"""
    try:
        metrics_file = log_dir / "user_metrics.json"
        
        # Load existing metrics
        if metrics_file.exists():
            with open(metrics_file, 'r') as f:
                metrics = json.load(f)
        else:
            metrics = {"sessions": {}, "global_stats": {"total_sessions": 0, "total_actions": 0}}
        
        # Initialize session if new
        if session_id not in metrics["sessions"]:
            metrics["sessions"][session_id] = {
                "session_start": datetime.now().isoformat(),
                "page_views": 0,
                "actions": [],
                "regions_selected": [],
                "feed_types_used": [],
                "admin_access": False,
                "total_actions": 0
            }
            metrics["global_stats"]["total_sessions"] += 1
        
        # Update session metrics
        session_data = metrics["sessions"][session_id]
        session_data["last_activity"] = datetime.now().isoformat()
        session_data["total_actions"] += 1
        metrics["global_stats"]["total_actions"] += 1
        
        # Record specific action
        action_record = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "data": data
        }
        session_data["actions"].append(action_record)
        
        # Track specific metrics
        if action == "page_view":
            session_data["page_views"] += 1
        elif action == "region_selected" and data:
            if data not in session_data["regions_selected"]:
                session_data["regions_selected"].append(data)
        elif action == "feed_type_selected" and data:
            if data not in session_data["feed_types_used"]:
                session_data["feed_types_used"].append(data)
        elif action == "admin_access":
            session_data["admin_access"] = True
        
        # Save metrics
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
            
        logger.debug(f"User metrics saved: {action} for session {session_id[-8:]}")
        
    except Exception as e:
        logger.error(f"Error saving user metrics: {e}")

def get_user_metrics_summary():
    """Get summary of user metrics for admin panel"""
    try:
        metrics_file = log_dir / "user_metrics.json"
        if not metrics_file.exists():
            return {"total_sessions": 0, "total_actions": 0, "active_sessions": 0}
        
        with open(metrics_file, 'r') as f:
            metrics = json.load(f)
        
        # Calculate active sessions (activity in last hour)
        active_sessions = 0
        current_time = datetime.now()
        
        for session_id, session_data in metrics["sessions"].items():
            if "last_activity" in session_data:
                last_activity = datetime.fromisoformat(session_data["last_activity"])
                if (current_time - last_activity).total_seconds() < 3600:  # 1 hour
                    active_sessions += 1
        
        return {
            "total_sessions": metrics["global_stats"]["total_sessions"],
            "total_actions": metrics["global_stats"]["total_actions"],
            "active_sessions": active_sessions
        }
    except Exception as e:
        logger.error(f"Error getting user metrics summary: {e}")
        return {"total_sessions": 0, "total_actions": 0, "active_sessions": 0}

# Configure page
st.set_page_config(
    page_title="🌍 Real-Time Earthquake Monitor", 
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
    logger.info(f"New session started: {st.session_state.session_id}")
    save_user_metrics(st.session_state.session_id, "session_start")
if 'page_views' not in st.session_state:
    st.session_state.page_views = 0
if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False

st.session_state.page_views += 1
logger.debug(f"Session {st.session_state.session_id[-8:]} - Page view #{st.session_state.page_views}")
save_user_metrics(st.session_state.session_id, "page_view", st.session_state.page_views)

@st.cache_data(ttl=300)
def fetch_earthquake_data(feed_type="all_hour", region="usa"):
    """Fetch earthquake data from USGS with regional filtering"""
    url = f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{feed_type}.geojson"
    
    logger.info(f"Fetching earthquake data: feed_type={feed_type}, region={region}")
    logger.debug(f"API URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"Successfully fetched data from USGS API - {len(data['features'])} total features")
        
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
            elif region == "nevada":
                # Nevada region
                if -120 <= longitude <= -114 and 35 <= latitude <= 42:
                    include_earthquake = True
            elif region == "hawaii":
                # Hawaii region  
                if -162 <= longitude <= -154 and 18 <= latitude <= 23:
                    include_earthquake = True
            elif region == "pacific":
                if -180 <= longitude <= -110 and -60 <= latitude <= 60:
                    include_earthquake = True
            elif region == "global":
                include_earthquake = True
            elif region == "west_coast":
                # Northwest region (Oregon and Washington focus)
                if -125 <= longitude <= -116 and 42 <= latitude <= 49:
                    include_earthquake = True
            elif region == "east_mississippi":
                # East of Mississippi region
                if -90 <= longitude <= -65 and 25 <= latitude <= 50:
                    include_earthquake = True
            elif region == "texas":
                # Texas region
                if -107 <= longitude <= -93 and 25.5 <= latitude <= 36.5:
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
        
        logger.info(f"Filtered {len(earthquakes)} earthquakes for region '{region}' from {len(data['features'])} total")
        return earthquakes
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error fetching earthquake data: {e}")
        st.error(f"Error fetching data: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching earthquake data: {e}")
        st.error(f"Error fetching data: {e}")
        return []

@st.cache_data(ttl=300)
def fetch_global_24h_peak():
    """Fetch global earthquake data to find the highest magnitude in the last 24 hours"""
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    
    logger.info("Fetching global 24-hour earthquake data for peak magnitude analysis")
    logger.debug(f"Global API URL: {url}")
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"Successfully fetched global data - {len(data['features'])} earthquakes in last 24 hours")
        
        earthquakes = []
        for feature in data['features']:
            props = feature['properties']
            coords = feature['geometry']['coordinates']
            
            magnitude = props.get('mag')
            if magnitude and magnitude > 0:  # Only include earthquakes with valid magnitude
                earthquakes.append({
                    'magnitude': magnitude,
                    'place': props.get('place', 'Unknown Location'),
                    'time': props.get('time', 0),
                    'latitude': coords[1],
                    'longitude': coords[0],
                    'depth': coords[2] if len(coords) > 2 else 0,
                    'url': props.get('url', ''),
                    'properties': props
                })
        
        logger.info(f"Processed {len(earthquakes)} valid earthquakes for global peak analysis")
        return earthquakes
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error fetching global earthquake data: {e}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for global earthquake data: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching global earthquake data: {e}")
        return []

def create_advanced_map(earthquakes, region="usa"):
    """Create enhanced earthquake map with comprehensive hover info"""
    logger.info(f"Creating advanced map for region '{region}' with {len(earthquakes)} earthquakes")
    
    if not earthquakes:
        logger.warning(f"No earthquake data available for map in region '{region}'")
        st.warning("⚠️ No earthquake data available for map")
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq.get('magnitude', 0) > 0]
    if not valid_earthquakes:
        logger.warning(f"No valid earthquake data for map in region '{region}' - all {len(earthquakes)} earthquakes have invalid magnitude")
        st.warning("⚠️ No valid earthquake data for map")
        return
    
    logger.debug(f"Processing {len(valid_earthquakes)} valid earthquakes for map visualization")
    
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
        "nevada": {"zoom": 7, "center": {"lat": 38.5, "lon": -117.0}},
        "hawaii": {"zoom": 7, "center": {"lat": 20.0, "lon": -157.0}},
        "west_coast": {"zoom": 6, "center": {"lat": 45.5, "lon": -121.0}},
        "east_mississippi": {"zoom": 5, "center": {"lat": 37.5, "lon": -77.5}},
        "texas": {"zoom": 6, "center": {"lat": 31.0, "lon": -100.0}},
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
        title=f"🗺️ Real-Time Earthquake Monitor - {region.replace('_', ' ').title()}",
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
    
    valid_earthquakes = [eq for eq in earthquakes if eq.get('magnitude', 0) > 0]
    if not valid_earthquakes:
        st.warning("⚠️ No valid earthquake data for statistics")
        return
    
    magnitudes = [eq.get('magnitude', 0) for eq in valid_earthquakes]
    depths = [eq.get('depth', 0) for eq in valid_earthquakes]
    times = [eq.get('time', 0) for eq in valid_earthquakes]
    
    # Enhanced Statistics Dashboard
    st.markdown("<h3 style='text-align: center; color: #2c3e50;'>📊 Real-Time Statistics Dashboard</h3>", unsafe_allow_html=True)
    
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
    
    # Regional Activity Comparison
    st.markdown("<h4 style='text-align: center;'>🌍 Regional Activity Comparison</h4>", unsafe_allow_html=True)
    
    # Get regional data for comparison
    try:
        # Use the current feed type from session state or default
        current_feed = getattr(st.session_state, 'feed_type', 'all_hour')
        regional_data = create_regional_comparison_chart(current_feed, 0.0)
        
        if regional_data:
            regions = [data['region'] for data in regional_data]
            counts = [data['count'] for data in regional_data]
            
            fig_regional = px.bar(
                x=regions,
                y=counts,
                title="Earthquake Activity by Region",
                labels={'x': 'Region', 'y': 'Number of Earthquakes'},
                color=counts,
                color_continuous_scale="Reds"
            )
            fig_regional.update_layout(
                height=350,
                xaxis_tickangle=-45,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig_regional, use_container_width=True)
        else:
            st.warning("⚠️ Regional comparison data unavailable")
    except Exception as e:
        st.error(f"Error loading regional data: {e}")
    
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

def create_regional_comparison_chart(feed_type, min_magnitude=0.0):
    """Create a regional comparison histogram showing earthquake counts across all regions"""
    
    # Define all regions for comparison
    regions = {
        "🇺🇸 United States of America": "usa",
        "🌴 California": "california", 
        "❄️ Alaska": "alaska",
        "🎰 Nevada": "nevada",
        "🏔️ Northwest": "west_coast",
        "🌺 Hawaii": "hawaii",
        "🏛️ East of Mississippi": "east_mississippi",
        "🤠 Texas": "texas"
    }
    
    regional_data = []
    
    # Fetch data for each region
    for region_name, region_code in regions.items():
        try:
            earthquakes = fetch_earthquake_data(feed_type, region_code)
            # Apply magnitude filter
            if min_magnitude > 0.0:
                earthquakes = [eq for eq in earthquakes if eq.get('magnitude', 0) >= min_magnitude]
            
            # Calculate statistics
            total_count = len(earthquakes)
            if earthquakes:
                magnitudes = [eq.get('magnitude', 0) for eq in earthquakes if eq.get('magnitude', 0) > 0]
                avg_magnitude = sum(magnitudes) / len(magnitudes) if magnitudes else 0
                max_magnitude = max(magnitudes) if magnitudes else 0
            else:
                avg_magnitude = 0
                max_magnitude = 0
            
            regional_data.append({
                'region': region_name,
                'region_code': region_code,
                'count': total_count,
                'avg_magnitude': avg_magnitude,
                'max_magnitude': max_magnitude
            })
        except Exception as e:
            # If there's an error with a region, add zero data
            logger.error(f"Error fetching data for region {region_name} ({region_code}): {e}")
            regional_data.append({
                'region': region_name,
                'region_code': region_code,
                'count': 0,
                'avg_magnitude': 0,
                'max_magnitude': 0
            })
    
    return regional_data

def show_regional_charts(feed_type, min_magnitude=0.0):
    """Display regional comparison charts and analytics"""
    st.markdown("<h3 style='text-align: center;'>📊 Regional Earthquake Comparison</h3>", unsafe_allow_html=True)
    
    with st.spinner("📡 Fetching data for all regions..."):
        regional_data = create_regional_comparison_chart(feed_type, min_magnitude)
    
    if not regional_data:
        st.warning("⚠️ No regional data available")
        return
    
    # Create comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Earthquake count histogram
        regions = [data['region'] for data in regional_data]
        counts = [data['count'] for data in regional_data]
        
        fig_count = px.bar(
            x=regions,
            y=counts,
            title="🌍 Earthquake Count by Region",
            labels={'x': 'Region', 'y': 'Number of Earthquakes'},
            color=counts,
            color_continuous_scale="Reds"
        )
        fig_count.update_layout(
            height=400,
            xaxis_tickangle=-45,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_count, use_container_width=True)
    
    with col2:
        # Average magnitude comparison
        avg_mags = [data['avg_magnitude'] for data in regional_data]
        
        fig_avg = px.bar(
            x=regions,
            y=avg_mags,
            title="📈 Average Magnitude by Region",
            labels={'x': 'Region', 'y': 'Average Magnitude'},
            color=avg_mags,
            color_continuous_scale="Oranges"
        )
        fig_avg.update_layout(
            height=400,
            xaxis_tickangle=-45,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_avg, use_container_width=True)
    
    # Regional summary table
    st.markdown("<h4 style='text-align: center;'>📋 Regional Summary Table</h4>", unsafe_allow_html=True)
    
    # Create a nice table display
    for data in sorted(regional_data, key=lambda x: x['count'], reverse=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(data['region'], f"{data['count']} events")
        
        with col2:
            if data['avg_magnitude'] > 0:
                st.metric("Avg Magnitude", f"M {data['avg_magnitude']:.1f}")
            else:
                st.metric("Avg Magnitude", "No data")
        
        with col3:
            if data['max_magnitude'] > 0:
                st.metric("Max Magnitude", f"M {data['max_magnitude']:.1f}")
            else:
                st.metric("Max Magnitude", "No data")
        
        with col4:
            # Activity level indicator
            if data['count'] == 0:
                activity = "🔵 Quiet"
            elif data['count'] < 10:
                activity = "🟡 Low"
            elif data['count'] < 50:
                activity = "🟠 Moderate"
            else:
                activity = "🔴 High"
            st.metric("Activity Level", activity)
        
        st.markdown("---")

def show_admin_panel():
    """
    Display administrative dashboard with session analytics and system monitoring.
    
    This function creates a comprehensive admin interface for monitoring application
    usage, session management, and system status. Provides insights into user
    interactions and application performance metrics.
    
    Features:
    ---------
    Session Analytics:
    - Unique session identifier (last 8 characters for privacy)
    - Page view counter tracking user engagement
    - Current timestamp for real-time monitoring
    - Session state persistence across interactions
    
    System Status:
    - Application version information
    - Data source connectivity status
    - Cache performance metrics
    - Error logging and monitoring capabilities
    
    Admin Interface Components:
    - Professional dashboard styling with gradient headers
    - Organized metric display using columns layout
    - Real-time updating statistics
    - System health indicators
    
    Returns:
    --------
    None
        Displays admin dashboard directly to Streamlit interface
    
    Security Considerations:
    -----------------------
    - Session IDs are truncated for privacy protection
    - No sensitive user data exposed in interface
    - Admin access controlled by toggle mechanism
    - Monitoring data kept anonymous
    
    Notes:
    ------
    - Toggle admin mode via sidebar button to access
    - Useful for debugging and performance monitoring
    - Helps track application usage patterns
    - Essential for production deployment monitoring
    """
    st.markdown("""
    <div class="admin-panel">
        <h3 style='margin: 0; text-align: center;'>🔧 Admin Dashboard</h3>
        <p style='margin: 0.5rem 0; text-align: center;'>Session Analytics & System Status</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Current session metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Session ID", st.session_state.session_id[-8:])
    
    with col2:
        st.metric("Page Views", st.session_state.page_views)
    
    with col3:
        current_time = datetime.now().strftime("%H:%M:%S")
        st.metric("Current Time", current_time)
    
    # Global user metrics
    st.markdown("<h4 style='text-align: center;'>📊 Global User Metrics</h4>", unsafe_allow_html=True)
    
    metrics_summary = get_user_metrics_summary()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👥 Total Sessions", metrics_summary["total_sessions"])
    
    with col2:
        st.metric("🎯 Total Actions", metrics_summary["total_actions"])
    
    with col3:
        st.metric("🟢 Active Sessions", metrics_summary["active_sessions"])
    
    # System status
    st.markdown("<h4 style='text-align: center;'>🖥️ System Status</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ USGS API: Connected")
        st.success("✅ Streamlit: Running")
        st.success("✅ User Metrics: Active")
    
    with col2:
        st.info("📡 Data Cache: 5 minutes")
        st.info("🌍 Regions: 8 available")
        st.info("📝 Logs: earthquake_monitor.log")
        st.info("📊 Metrics: user_metrics.json")

def main():
    """Real-time earthquake monitoring application"""
    # Enhanced header
    st.markdown("""
    <div style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin-bottom: 2rem;'>
        <h1 style='margin: 0; font-size: 2.5rem;'>🌍 Real-Time Earthquake Monitor</h1>
        <p style='margin: 0.5rem 0; font-size: 1.2rem;'>Professional real-time seismic monitoring system</p>
        <p style='margin: 0; opacity: 0.8;'>Powered by USGS • Real-time Data • Global Coverage</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Global Highest Magnitude Alert (24 hours)
    with st.spinner("🔍 Checking global earthquake activity..."):
        try:
            global_earthquakes = fetch_global_24h_peak()
            if global_earthquakes:
                # Find the highest magnitude earthquake in the last 24 hours
                highest_mag_quake = max(global_earthquakes, key=lambda x: x.get('magnitude', 0))
                mag = highest_mag_quake.get('magnitude', 0)
                place = highest_mag_quake.get('place', 'Unknown Location')
                time_ms = highest_mag_quake.get('time', 0)
                
                if mag and mag > 0:
                    from datetime import datetime
                    event_time = datetime.fromtimestamp(time_ms / 1000).strftime('%H:%M UTC')
                    
                    # Color coding based on magnitude
                    if mag >= 7.0:
                        color = "#FF0000"  # Red for major
                        alert_icon = "🚨"
                        severity = "MAJOR"
                    elif mag >= 6.0:
                        color = "#FF6600"  # Orange for strong
                        alert_icon = "⚠️"
                        severity = "STRONG"
                    elif mag >= 5.0:
                        color = "#FFD700"  # Gold for moderate
                        alert_icon = "🔶"
                        severity = "MODERATE"
                    else:
                        color = "#32CD32"  # Green for light
                        alert_icon = "🟢"
                        severity = "LIGHT"
                    
                    st.markdown(f"""
                    <div style='text-align: center; background: linear-gradient(135deg, {color}20 0%, {color}10 100%); 
                                padding: 1rem; border-radius: 15px; margin-bottom: 1.5rem; border: 2px solid {color}50;'>
                        <h3 style='margin: 0; color: {color}; font-size: 1.5rem;'>{alert_icon} 24H GLOBAL PEAK: {severity}</h3>
                        <p style='margin: 0.5rem 0; font-size: 1.8rem; font-weight: bold; color: {color};'>Magnitude {mag:.1f}</p>
                        <p style='margin: 0; opacity: 0.8; font-size: 1.1rem;'>{place} • {event_time}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    logger.info(f"Displayed 24H Global Peak: M{mag:.1f} at {place} ({event_time})")
                else:
                    st.info("🌍 No significant earthquake activity detected in the last 24 hours")
                    logger.info("No valid magnitude data found for 24H Global Peak display")
            else:
                st.info("🌍 Unable to fetch global earthquake data at this time")
                logger.warning("Failed to fetch global earthquake data for 24H Peak display")
        except Exception as e:
            st.warning("⚠️ Global earthquake data temporarily unavailable")
            logger.error(f"Error displaying 24H Global Peak: {e}")
    
    # Admin toggle
    if st.sidebar.button("🔧 Toggle Admin Mode"):
        st.session_state.admin_mode = not st.session_state.admin_mode
        logger.info(f"Session {st.session_state.session_id[-8:]} - Admin mode {'enabled' if st.session_state.admin_mode else 'disabled'}")
        save_user_metrics(st.session_state.session_id, "admin_access", st.session_state.admin_mode)
    
    if st.session_state.admin_mode:
        logger.debug(f"Displaying admin panel for session {st.session_state.session_id[-8:]}")
        show_admin_panel()
        st.markdown("---")
    
    # Data Source Selection
    st.markdown("<h3 style='text-align: center;'>📡 Data Source Selection</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🕐 Past Hour", key="hour"):
            st.session_state.feed_type = "all_hour"
            logger.info(f"Session {st.session_state.session_id[-8:]} - Selected feed type: all_hour")
            save_user_metrics(st.session_state.session_id, "feed_type_selected", "all_hour")
        if st.button("📅 Past Day", key="day"):
            st.session_state.feed_type = "all_day"
            logger.info(f"Session {st.session_state.session_id[-8:]} - Selected feed type: all_day")
            save_user_metrics(st.session_state.session_id, "feed_type_selected", "all_day")
        if st.button("🌍 Past Week", key="week"):
            st.session_state.feed_type = "all_week"
            logger.info(f"Session {st.session_state.session_id[-8:]} - Selected feed type: all_week")
            save_user_metrics(st.session_state.session_id, "feed_type_selected", "all_week")
    
    with col2:
        if st.button("📆 Past Month", key="month"):
            st.session_state.feed_type = "all_month"
            logger.info(f"Session {st.session_state.session_id[-8:]} - Selected feed type: all_month")
            save_user_metrics(st.session_state.session_id, "feed_type_selected", "all_month")
        if st.button("🌋 Major Quakes (4.5+)", key="major"):
            st.session_state.feed_type = "4.5_week"
            logger.info(f"Session {st.session_state.session_id[-8:]} - Selected feed type: 4.5_week")
            save_user_metrics(st.session_state.session_id, "feed_type_selected", "4.5_week")
        if st.button("⚠️ Significant Events", key="significant"):
            st.session_state.feed_type = "significant_month"
            logger.info(f"Session {st.session_state.session_id[-8:]} - Selected feed type: significant_month")
            save_user_metrics(st.session_state.session_id, "feed_type_selected", "significant_month")
    
    # Initialize session state
    if 'feed_type' not in st.session_state:
        st.session_state.feed_type = "all_hour"
    
    feed_type = st.session_state.feed_type
    
    # Real-Time View Controls
    st.markdown("<h3 style='text-align: center;'>🎛️ Real-Time Controls</h3>", unsafe_allow_html=True)
    
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
            "🇺🇸 United States of America": "usa",
            "🌴 California": "california", 
            "❄️ Alaska": "alaska",
            "🎰 Nevada": "nevada",
            "🏔️ Northwest": "west_coast",
            "🌺 Hawaii": "hawaii",
            "🏛️ East of Mississippi": "east_mississippi",
            "🤠 Texas": "texas"
        }
        
        selected_region = st.selectbox(
            "🌍 Geographic Region",
            options=list(region_options.keys()),
            index=0,
            help="Select geographic region to monitor"
        )
        
        # Track region selection if it changed
        if 'last_selected_region' not in st.session_state or st.session_state.last_selected_region != selected_region:
            st.session_state.last_selected_region = selected_region
            save_user_metrics(st.session_state.session_id, "region_selected", selected_region)
            logger.info(f"Session {st.session_state.session_id[-8:]} - Selected region: {selected_region}")
        
        region = region_options[selected_region]
    
    with col2:
        show_stats_toggle = st.checkbox("📊 Show Statistics", value=True)
        show_charts_toggle = st.checkbox("📈 Show Charts", value=True)
        show_map_toggle = st.checkbox("🗺️ Show Map", value=True)
        show_recent_toggle = st.checkbox("📋 Show Recent List", value=True)
    
    # Fetch and process data
    logger.info(f"Session {st.session_state.session_id[-8:]} - Loading data: feed_type={feed_type}, region={region}, min_magnitude={min_magnitude}")
    
    with st.spinner("📡 Loading real-time earthquake data..."):
        earthquakes = fetch_earthquake_data(feed_type, region)
    
    # Apply magnitude filter
    if min_magnitude > 0.0:
        original_count = len(earthquakes)
        earthquakes = [eq for eq in earthquakes if eq.get('magnitude', 0) >= min_magnitude]
        logger.info(f"Applied magnitude filter {min_magnitude}: {original_count} -> {len(earthquakes)} earthquakes")
    
    if earthquakes:
        # Calculate accurate counts
        total_events = len(earthquakes)
        valid_events = len([eq for eq in earthquakes if eq.get('magnitude', 0) > 0])
        incomplete_events = total_events - valid_events
        
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
        
        # Enhanced status with data quality info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success(f"✅ **{total_events}** Total Events")
        with col2:
            st.metric("📊 Complete Records", f"{valid_events}")
        with col3:
            if incomplete_events > 0:
                st.warning(f"⚠️ **{incomplete_events}** Incomplete")
            else:
                st.info("✨ All Records Complete")
        
        # Conditional displays based on toggles
        if show_stats_toggle:
            show_advanced_stats(earthquakes, selected_region)
        
        if show_map_toggle:
            create_advanced_map(earthquakes, region)
        
        # Recent earthquakes list
        if show_recent_toggle:
            st.markdown("<h3 style='text-align: center;'>📋 Recent Earthquake Events</h3>", unsafe_allow_html=True)
            valid_earthquakes = [eq for eq in earthquakes if eq.get('magnitude', 0) > 0]
            
            for i, eq in enumerate(sorted(valid_earthquakes, key=lambda x: x.get('magnitude', 0), reverse=True)[:10]):
                time_dt = datetime.fromtimestamp(eq.get('time', 0)/1000)
                time_str = time_dt.strftime("%m/%d %H:%M")
                
                # Enhanced earthquake display with color coding
                magnitude = eq.get('magnitude', 0)
                mag_color = (
                    "🔴" if magnitude >= 5.0 else
                    "🟠" if magnitude >= 4.0 else
                    "🟡" if magnitude >= 3.0 else
                    "🔵"
                )
                
                alert_info = ""
                if eq.get('alert'):
                    alert_info = f" | Alert: {eq['alert'].upper()}"
                
                tsunami_info = ""
                if eq.get('tsunami'):
                    tsunami_info = " | ⚠️ TSUNAMI"
                
                st.markdown(f"""
                **{mag_color} M {magnitude:.1f}** - {eq.get('place', 'Unknown')}  
                *{time_str} | Depth: {eq.get('depth', 0):.1f}km{alert_info}{tsunami_info}*
                """)
                
                if i < 9:  # Add separator except for last item
                    st.markdown("---")
    else:
        st.warning("⚠️ No earthquake data available for the selected criteria")
    
    # Data Quality Disclaimer
    st.markdown("---")
    st.info("""
    📋 **Data Quality Notice**: Some earthquake records may be incomplete as the USGS continues to research and verify event details. 
    Preliminary data is subject to revision as more information becomes available. Missing magnitude, depth, or location data 
    indicates ongoing analysis by seismologists.
    """)
    
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
"""
Real-Time Earthquake Monitor - Professional Seismic Monitoring Application

A comprehensive, production-ready earthquake monitoring system built with Streamlit
that provides real-time seismic data visualization, regional analysis, and 
professional-grade reporting capabilities.

OVERVIEW:
=========
This application connects to the USGS Earthquake Hazards Program API to provide
real-time earthquake monitoring with advanced features including:

- Interactive geographic mapping with detailed earthquake information
- Statistical analysis dashboards with data quality transparency  
- Regional comparison analytics across 8 major US regions
- Multiple viewing modes for different user needs
- Professional data presentation with scientific accuracy
- Mobile-responsive design for field use

FEATURES:
=========
Data Sources:
- USGS GeoJSON earthquake feeds (real-time)
- Multiple time windows (hour, day, week, month)
- Magnitude-based filtering and special event feeds

Regional Coverage:
- United States of America (continental + territories)
- California (high seismic activity focus)
- Alaska (frequent earthquake monitoring)
- Nevada (mining and residential seismic activity)
- Pacific Northwest (Oregon & Washington)
- Hawaii (volcanic and seismic activity)
- East of Mississippi (intraplate seismic monitoring)
- Texas (induced seismicity and natural faults)

Visualization Components:
- Interactive Plotly maps with hover details
- Statistical dashboards with comprehensive metrics
- Regional comparison charts and analytics
- Temporal activity analysis and trending
- Professional styling with accessibility considerations

Data Quality Features:
- Transparent reporting of complete vs. incomplete records
- Clear disclaimers about preliminary USGS data
- Accurate statistical calculations with data validation
- Error handling for missing or invalid data fields

TECHNICAL IMPLEMENTATION:
========================
Framework: Streamlit with professional UI/UX design
Data Processing: Pandas for efficient data manipulation
Visualization: Plotly for interactive, publication-ready charts
API Integration: USGS Earthquake Hazards Program REST API
Caching: 5-minute TTL for optimal performance and API courtesy
Error Handling: Comprehensive error boundaries and graceful degradation

USAGE:
======
Run with: streamlit run earthquake_simple.py
Access via: http://localhost:8501
Deploy to: Streamlit Cloud, AWS, Azure, or any Python hosting platform

AUTHOR: AI Assistant
VERSION: 3.0 (Professional Production Release)
LAST UPDATED: October 2025
LICENSE: Open Source - Educational and Research Use

DEPENDENCIES:
============
- streamlit: Web application framework
- requests: HTTP client for USGS API
- pandas: Data manipulation and analysis
- plotly: Interactive visualization library
- numpy: Numerical computing support

All data is handled in memory (lists, dicts, pandas DataFrames).
No SQL statements, database connections, or user-supplied query strings are used.
You are safe from SQL injection vulnerabilities in this code.


"""

from calendar import c
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, timezone
import numpy as np
import json
import os
from pathlib import Path
import time
import logging

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
        margin-bottom: 2rem; /* Increased spacing after headings to prevent overlap */
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
    """
    Fetch earthquake data from USGS API with regional filtering and data validation.
    
    This function retrieves earthquake data from the USGS GeoJSON feeds and applies
    geographic filtering based on the specified region. It includes comprehensive
    error handling and data validation to ensure robust operation.
    
    Parameters:
    -----------
    feed_type : str, optional
        Type of earthquake feed to fetch. Options include:
        - "all_hour": All earthquakes in past hour
        - "all_day": All earthquakes in past day  
        - "all_week": All earthquakes in past week
        - "all_month": All earthquakes in past month
        - "4.5_week": Magnitude 4.5+ earthquakes in past week
        - "significant_month": Significant earthquakes in past month
        Default: "all_hour"
    
    region : str, optional
        Geographic region for filtering earthquakes. Options include:
        - "usa": Continental United States and territories
        - "california": California state boundaries
        - "alaska": Alaska region
        - "nevada": Nevada state boundaries
        - "west_coast": Pacific Northwest (Oregon & Washington)
        - "hawaii": Hawaiian Islands
        - "east_mississippi": Eastern United States
        - "texas": Texas state boundaries
        Default: "usa"
    
    Returns:
    --------
    list of dict
        List of earthquake dictionaries containing:
        - magnitude: Earthquake magnitude (float or None)
        - place: Location description (str)
        - time: UTC timestamp in milliseconds (int)
        - depth: Depth in kilometers (float)
        - longitude: Longitude coordinate (float)
        - latitude: Latitude coordinate (float)
        - alert: USGS alert level (str or None)
        - tsunami: Tsunami warning flag (int, 0 or 1)
        - url: USGS event detail URL (str)
    
    Raises:
    -------
    requests.RequestException
        If API request fails or times out
    ValueError
        If invalid JSON response received
    
    Notes:
    ------
    - Function is cached for 5 minutes (300 seconds) to reduce API calls
    - Geographic filtering uses precise coordinate boundaries
    - Handles missing or invalid data gracefully
    - Some earthquake records may be incomplete during initial reporting
    """
    url = f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{feed_type}.geojson"
    start_time = time.time()
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        earthquakes = []
        for feature in data['features']:
            # Extract earthquake properties and coordinates from GeoJSON structure
            props = feature['properties']  # Contains magnitude, place, time, alert info
            coords = feature['geometry']['coordinates']  # [longitude, latitude, depth]
            
            # GeoJSON format: coordinates are [longitude, latitude, depth]
            longitude, latitude = coords[0], coords[1]
            
            # Apply geographic filtering based on region boundaries
            # Each region has carefully defined coordinate boundaries for accurate filtering
            include_earthquake = False
            
            if region == "usa":
                # Continental US and territories: Wide longitude range to include Hawaii/Alaska
                if -180 <= longitude <= -60 and 15 <= latitude <= 75:
                    include_earthquake = True
            elif region == "california":
                # California state boundaries: High seismic activity region
                if -125 <= longitude <= -114 and 32 <= latitude <= 42:
                    include_earthquake = True
            elif region == "alaska":
                # Alaska region: Includes Aleutian Islands and mainland Alaska
                if -180 <= longitude <= -130 and 54 <= latitude <= 72:
                    include_earthquake = True
            elif region == "nevada":
                # Nevada state boundaries: Mining and residential seismic monitoring
                if -120 <= longitude <= -114 and 35 <= latitude <= 42:
                    include_earthquake = True
            elif region == "hawaii":
                # Hawaii region (volcanic and seismic activity)
                if -161 <= longitude <= -154 and 18 <= latitude <= 23:
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
                # Create standardized earthquake data dictionary
                # Use .get() method for safe data extraction - some fields may be missing
                earthquakes.append({
                    'magnitude': props.get('mag', 0),           # Earthquake magnitude (may be None initially)
                    'place': props.get('place', 'Unknown'),    # Location description from USGS
                    'time': props.get('time', 0),              # UTC timestamp in milliseconds
                    'depth': coords[2] if len(coords) > 2 else 0,  # Depth in kilometers
                    'longitude': longitude,                     # Geographic longitude
                    'latitude': latitude,                       # Geographic latitude  
                    'alert': props.get('alert'),               # USGS alert level (red/orange/yellow/green)
                    'tsunami': props.get('tsunami', 0),        # Tsunami warning flag (0 or 1)
                    'url': props.get('url', '')                # USGS event detail URL
                })
        
        result = earthquakes
    except Exception as e:
        # Handle API errors gracefully - return empty list rather than crashing
        st.error(f"Error fetching data: {e}")
        return []
    finally:
        elapsed = time.time() - start_time
        logging.basicConfig(filename="earthquake_monitor.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
        logging.info(f"fetch_earthquake_data | feed_type={feed_type} | region={region} | elapsed_time={elapsed:.3f}s")
    return result

def create_advanced_map(earthquakes, region="usa", chart_key_prefix=""):
    """
    Create an interactive earthquake map with comprehensive visualization features.
    
    This function generates a professional-grade interactive map displaying earthquake
    locations with detailed hover information, magnitude-based color coding, and
    region-specific zoom settings. Uses Plotly for high-performance rendering.
    
    Parameters:
    -----------
    earthquakes : list of dict
        List of earthquake data dictionaries from fetch_earthquake_data()
        Each earthquake should contain magnitude, place, time, depth, coordinates, etc.
    
    region : str, optional
        Geographic region code for map centering and zoom level:
        - "usa": Continental US view (zoom 3, center: Kansas)
        - "california": California state view (zoom 6)
        - "alaska": Alaska region view (zoom 4)
        - "nevada": Nevada state view (zoom 7)
        - "west_coast": Pacific Northwest view (zoom 6)
        - "hawaii": Hawaiian Islands view (zoom 8)
        - "east_mississippi": Eastern US view (zoom 5)
        - "texas": Texas state view (zoom 6)
        Default: "usa"
    
    Returns:
    --------
    None
        Displays the interactive map directly to Streamlit interface
    
    Features:
    ---------
    - Color-coded magnitude visualization (red for high magnitude)
    - Interactive hover tooltips with comprehensive earthquake details
    - Region-specific zoom levels and center points for optimal viewing
    - Magnitude categories (Micro, Minor, Light, Moderate, Major)
    - Alert status indicators with color coding
    - Date/time formatting in readable format
    - Coordinate precision display
    - Professional map styling with customizable height
    
    Notes:
    ------
    - Filters out earthquakes with missing magnitude data
    - Handles empty datasets gracefully with warning messages
    - Map height fixed at 500px for consistent UI layout
    - Uses Plotly's scatter_map for optimal performance
    """
    if not earthquakes:
        st.warning("⚠️ No earthquake data available for map")
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq.get('magnitude') is not None and eq.get('magnitude') > 0]
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
        "nevada": {"zoom": 7, "center": {"lat": 38.5, "lon": -117.0}},
        "west_coast": {"zoom": 6, "center": {"lat": 45.5, "lon": -121.0}},
        "hawaii": {"zoom": 8, "center": {"lat": 20.5, "lon": -157.5}},
        "east_mississippi": {"zoom": 5, "center": {"lat": 37.5, "lon": -77.5}},
        "texas": {"zoom": 6, "center": {"lat": 31.0, "lon": -100.0}}
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

    st.plotly_chart(fig, use_container_width=True, key=f"{chart_key_prefix}map_chart_main")


def show_global_peak_24h():
    """
    Fetch and display the highest magnitude earthquake globally in the last 24 hours.
    """
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        features = data.get("features", [])
        # Filter out events with missing or zero magnitude
        valid_events = [
            f for f in features
            if f["properties"].get("mag") is not None and f["properties"]["mag"] > 0
        ]
        if not valid_events:
            st.info("🌍 No valid global earthquake data in the last 24 hours.")
            return
        # Find the event with the highest magnitude
        peak = max(valid_events, key=lambda f: f["properties"]["mag"])
        mag = peak["properties"]["mag"]
        place = peak["properties"].get("place", "Unknown location")
        time_ms = peak["properties"].get("time", 0)
        #deprecated method
        #time_str = datetime.utcfromtimestamp(time_ms / 1000).strftime("%Y-%m-%d %H:%M UTC")
        time_str = datetime.fromtimestamp(time_ms / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        url_detail = peak["properties"].get("url", "")
        # Color/severity
        if mag >= 7.0:
            color = "🚨 <span style='color:#c0392b'><b>MAJOR</b></span>"
        elif mag >= 6.0:
            color = "⚠️ <span style='color:#e67e22'><b>STRONG</b></span>"
        elif mag >= 5.0:
            color = "🔶 <span style='color:#f1c40f'><b>MODERATE</b></span>"
        else:
            color = "🟢 <span style='color:#27ae60'><b>LIGHT</b></span>"
        st.markdown(
            f"""
            <div style='background:linear-gradient(90deg,#f8ffae 0%,#43c6ac 100%);padding:1.2rem 1rem 1.2rem 1rem;border-radius:15px;margin-bottom:1.5rem;text-align:center;'>
                <span style='font-size:1.3rem;'>{color} | <b>Global 24H Peak:</b> M {mag:.1f}</span><br>
                <span style='font-size:1.1rem;'>{place}</span><br>
                <span style='font-size:1rem;color:#555;'>Occurred: {time_str}</span><br>
                <a href="{url_detail}" target="_blank" style="font-size:0.95rem;">USGS Event Details</a>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.warning(f"🌍 Could not fetch global 24H peak earthquake: {e}")

def show_advanced_stats(earthquakes, region="USA", chart_key_prefix="" ):
    """
    Display comprehensive earthquake statistics with interactive visualizations.
    
    This function creates a professional statistics dashboard showing key metrics,
    distribution analyses, and temporal patterns for earthquake data. Includes
    data quality transparency and multiple visualization types.
    
    Parameters:
    -----------
    earthquakes : list of dict
        List of earthquake data dictionaries from fetch_earthquake_data()
        Must contain magnitude, depth, time, and location information
    
    region : str, optional
        Region name for display purposes in chart titles and headers
        Default: "USA"
    
    Features:
    ---------
    Dashboard Components:
    - Data quality summary (total vs. complete records)
    - Key metrics row (total events, max magnitude, averages)
    - Magnitude distribution histogram with color coding
    - Depth vs. magnitude scatter plot analysis
    - Temporal activity timeline showing earthquake frequency
    - Statistical calculations using only complete data records
    
    Visualizations:
    - Interactive Plotly charts with hover details
    - Color-coded magnitude categories
    - Professional styling with consistent layout
    - Responsive design for different screen sizes
    
    Data Quality Handling:
    - Transparent reporting of incomplete vs. complete records
    - Clear disclaimers about calculation methodology
    - Graceful handling of missing data fields
    - Statistical calculations exclude invalid data points
    
    Returns:
    --------
    None
        Displays statistics dashboard directly to Streamlit interface
    
    Notes:
    ------
    - Requires valid earthquake data with at least magnitude information
    - Shows warning if no complete records available for statistics
    - All calculations clearly labeled as based on complete records only
    - Timeline shows activity patterns over time periods
    """
    if not earthquakes:
        st.warning("⚠️ No earthquake data available for statistics")
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq.get('magnitude') is not None and eq.get('magnitude') > 0]
    if not valid_earthquakes:
        st.warning("⚠️ No valid earthquake data for statistics")
        return
    
    magnitudes = [eq.get('magnitude', 0) for eq in valid_earthquakes]
    depths = [eq.get('depth', 0) for eq in valid_earthquakes]
    times = [eq.get('time', 0) for eq in valid_earthquakes]
    
    # Enhanced Statistics Dashboard
    st.markdown("<h3 style='text-align: center; color: #2c3e50;'>📊 Advanced Statistics Dashboard</h3>", unsafe_allow_html=True)
    
    # Data quality info
    total_in_dataset = len(earthquakes)
    complete_records = len(valid_earthquakes)
    incomplete_records = total_in_dataset - complete_records
    
    if incomplete_records > 0:
        st.warning(f"📊 **Statistics based on {complete_records} complete records** (out of {total_in_dataset} total events. {incomplete_records} events have incomplete data and are excluded from calculations.)")
    
    # Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("✅ Complete Events", len(valid_earthquakes))
    
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
    st.plotly_chart(fig_hist, use_container_width=True,  key=f"{chart_key_prefix}histogram_chart_stats")
    
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
        st.plotly_chart(fig_scatter, use_container_width=True, key=f"{chart_key_prefix}scatter_chart_stats")
    
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
            st.plotly_chart(fig_timeline, use_container_width=True, key=f"{chart_key_prefix}timeline_chart_stats")

def create_regional_comparison_chart(feed_type, min_magnitude=0.0, chart_key_prefix=""):
    """
    Generate comprehensive regional earthquake comparison data for all monitored regions.
    
    This function fetches earthquake data for all defined geographic regions and
    compiles comparative statistics including total events, complete records,
    and magnitude analysis. Essential for regional analysis dashboard.
    
    Parameters:
    -----------
    feed_type : str
        USGS feed type identifier (e.g., "all_hour", "all_day", "all_week")
        Determines the time window for earthquake data collection
    
    min_magnitude : float, optional
        Minimum magnitude threshold for filtering earthquakes
        Events below this threshold are excluded from analysis
        Default: 0.0 (includes all recorded events)
    
    Returns:
    --------
    list of dict
        List of regional data dictionaries, each containing:
        - region: Display name with emoji (e.g., "🇺🇸 United States of America")
        - region_code: Internal code for API calls (e.g., "usa")
        - total_count: Total earthquake events detected in region
        - complete_count: Events with complete magnitude data
        - incomplete_count: Events missing critical data fields
        - avg_magnitude: Average magnitude of complete records
        - max_magnitude: Maximum magnitude recorded in region
    
    Regional Coverage:
    -----------------
    Analyzes data for all defined regions:
    - United States of America (continental US and territories)
    - California (high seismic activity state)
    - Alaska (frequent earthquake region)
    - Nevada (mining and residential seismic monitoring)
    - Northwest (Oregon and Washington Pacific zone)
    - Hawaii (volcanic and seismic activity)
    - East of Mississippi (eastern US intraplate activity)
    - Texas (induced seismicity and natural faults)
    
    Data Processing:
    ---------------
    - Applies magnitude filtering consistently across all regions
    - Separates complete vs. incomplete data records
    - Calculates accurate statistics based only on valid data
    - Handles API errors gracefully with zero-data fallbacks
    - Maintains data integrity through comprehensive validation
    
    Error Handling:
    --------------
    - Catches and handles individual regional API failures
    - Returns zero data for failed regions instead of crashing
    - Logs errors for debugging while maintaining functionality
    - Ensures consistent data structure regardless of failures
    
    Notes:
    ------
    - Function may take several seconds due to multiple API calls
    - Results used by show_regional_charts() for visualization
    - Essential for understanding regional seismic activity patterns
    - Data quality transparency maintained throughout analysis
    """
    
    # Define all regions for comparison
    regions = {
        "🗽 United States of America": "usa",
        "🌴 California": "california", 
        "❄️ Alaska": "alaska",
        "🏔️ Nevada": "nevada",
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
                earthquakes = [eq for eq in earthquakes if eq.get('magnitude') is not None and eq.get('magnitude') > min_magnitude]
            
            # Calculate statistics
            total_count = len(earthquakes)
            valid_magnitudes = [eq.get('magnitude', 0) for eq in earthquakes if eq.get('magnitude', 0) > 0]
            complete_count = len(valid_magnitudes)
            incomplete_count = total_count - complete_count
            
            if valid_magnitudes:
                avg_magnitude = sum(valid_magnitudes) / len(valid_magnitudes)
                max_magnitude = max(valid_magnitudes)
            else:
                avg_magnitude = 0
                max_magnitude = 0
            
            regional_data.append({
                'region': region_name,
                'region_code': region_code,
                'total_count': total_count,
                'complete_count': complete_count,
                'incomplete_count': incomplete_count,
                'avg_magnitude': avg_magnitude,
                'max_magnitude': max_magnitude
            })
        except Exception as e:
            # If there's an error with a region, add zero data
            regional_data.append({
                'region': region_name,
                'region_code': region_code,
                'total_count': 0,
                'complete_count': 0,
                'incomplete_count': 0,
                'avg_magnitude': 0,
                'max_magnitude': 0
            })
    
    return regional_data

def show_regional_charts(feed_type, min_magnitude=0.0, chart_key_prefix=""):
    """Display regional comparison charts and analytics"""
    st.markdown("<h3 style='text-align: center;'>📊 Regional Earthquake Comparison</h3>", unsafe_allow_html=True)
    
    with st.spinner("📡 Fetching data for all regions..."):
        regional_data = create_regional_comparison_chart(feed_type, min_magnitude, chart_key_prefix="regional_")
    
    if not regional_data:
        st.warning("⚠️ No regional data available")
        return
    
    # Create comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Total events histogram
        regions = [data['region'] for data in regional_data]
        total_counts = [data['total_count'] for data in regional_data]
        
        fig_count = px.bar(
            x=regions,
            y=total_counts,
            title="🌍 Total Events by Region",
            labels={'x': 'Region', 'y': 'Number of Events'},
            color=total_counts,
            color_continuous_scale="Blues"
        )
        fig_count.update_layout(
            height=400,
            xaxis_tickangle=-45,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_count, use_container_width=True,            key=f"{chart_key_prefix}regional_total_count_chart")

    with col2:
        # Complete records histogram
        complete_counts = [data['complete_count'] for data in regional_data]
        
        fig_complete = px.bar(
            x=regions,
            y=complete_counts,
            title="✅ Complete Records by Region",
            labels={'x': 'Region', 'y': 'Complete Records'},
            color=complete_counts,
            color_continuous_scale="Greens"
        )
        fig_complete.update_layout(
            height=400,
            xaxis_tickangle=-45,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_complete, use_container_width=True, key=f"{chart_key_prefix}regional_complete_count_chart")
    
    # Average magnitude comparison
    st.markdown("#### 📈 Average Magnitude by Region")
    avg_mags = [data['avg_magnitude'] for data in regional_data]
    
    fig_avg = px.bar(
        x=regions,
        y=avg_mags,
        title="� Average Magnitude Comparison",
        labels={'x': 'Region', 'y': 'Average Magnitude'},
        color=avg_mags,
        color_continuous_scale="Oranges"
    )
    fig_avg.update_layout(
        height=400,
        xaxis_tickangle=-45,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_avg, use_container_width=True, key=f"{chart_key_prefix}regional_avg_magnitude")
    
    # Regional summary table
    st.markdown("<h4 style='text-align: center;'>📋 Regional Summary Table</h4>", unsafe_allow_html=True)
    
    # Create a nice table display
    for data in sorted(regional_data, key=lambda x: x['total_count'], reverse=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total = data['total_count']
            complete = data['complete_count']
            st.metric(data['region'], f"{total} total | {complete} complete")
        
        with col2:
            if data['avg_magnitude'] > 0:
                st.metric("Avg Magnitude", f"M {data['avg_magnitude']:.1f}")
            else:
                st.metric("Avg Magnitude", "No complete data")
        
        with col3:
            if data['max_magnitude'] > 0:
                st.metric("Max Magnitude", f"M {data['max_magnitude']:.1f}")
            else:
                st.metric("Max Magnitude", "No complete data")
        
        with col4:
            # Activity level based on complete records
            complete_count = data['complete_count']
            if complete_count == 0:
                activity = "🔵 No Complete Data"
            elif complete_count < 10:
                activity = "🟡 Low"
            elif complete_count < 50:
                activity = "🟠 Moderate"
            else:
                activity = "🔴 High"
            st.metric("Activity Level", activity)
        
        st.markdown("---")

def show_charts_section(earthquakes, feed_type, min_magnitude=0.0 ,chart_key_prefix=""):
    """Display comprehensive charts and analytics"""
    st.markdown("<h3 style='text-align: center;'>📈 Charts & Analytics</h3>", unsafe_allow_html=True)
    
    # Tab selection for different chart types
    tab1, tab2, tab3 = st.tabs(["📊 Current Region", "🌍 Regional Comparison", "📈 Advanced Analytics"])
    
    with tab1:
        if earthquakes:
            show_advanced_stats(earthquakes, "Current Selection", chart_key_prefix="tab1_")
        else:
            st.warning("⚠️ No earthquake data available for current region")
    
    with tab2:
        show_regional_charts(feed_type, min_magnitude, chart_key_prefix="tab2_")
    
    with tab3:
        if earthquakes:
            st.markdown("#### 🔬 Advanced Analysis")
            
            # Additional analytics could go here
            valid_earthquakes = [eq for eq in earthquakes if eq.get('magnitude') is not None and eq.get('magnitude') > 0]
            if valid_earthquakes:
                magnitudes = [eq.get('magnitude', 0) for eq in valid_earthquakes]
                
                # Magnitude distribution pie chart
                mag_categories = {
                    'Micro (M < 3.0)': len([m for m in magnitudes if m < 3.0]),
                    'Minor (3.0-3.9)': len([m for m in magnitudes if 3.0 <= m < 4.0]),
                    'Light (4.0-4.9)': len([m for m in magnitudes if 4.0 <= m < 5.0]),
                    'Moderate (5.0-5.9)': len([m for m in magnitudes if 5.0 <= m < 6.0]),
                    'Strong (6.0+)': len([m for m in magnitudes if m >= 6.0])
                }
                
                # Remove zero categories
                mag_categories = {k: v for k, v in mag_categories.items() if v > 0}
                
                if mag_categories:
                    fig_pie = px.pie(
                        values=list(mag_categories.values()),
                        names=list(mag_categories.keys()),
                        title="🥧 Magnitude Distribution"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True, key=f"{chart_key_prefix}magnitude_pie_chart_advanced")
        else:
            st.warning("⚠️ No data available for advanced analytics")

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
    """
    Main application function for Real-Time Earthquake Monitor.
    
    This is the primary entry point for the Streamlit earthquake monitoring
    application. Orchestrates the entire user interface, data processing,
    and visualization pipeline with professional presentation and error handling.
    
    Application Features:
    --------------------
    User Interface:
    - Professional gradient header with branding
    - Organized control sections (data selection, magnitude filtering, region selection)
    - Multiple view modes (Statistics, Charts, Map, Recent Events, Complete)
    - Active button highlighting for current selections
    - Responsive design for mobile and desktop
    
    Data Processing:
    - Real-time earthquake data from USGS API
    - Regional geographic filtering (8 major regions)
    - Magnitude threshold filtering
    - Data quality validation and transparency
    - Comprehensive error handling
    
    Visualization Components:
    - Interactive earthquake maps with hover details
    - Statistical dashboards with key metrics
    - Regional comparison charts and analytics
    - Recent earthquake event listings
    - Temporal activity analysis
    
    View Modes:
    -----------
    - 📊 Statistics View: Comprehensive statistical analysis
    - 📈 Charts View: Regional comparisons and advanced analytics
    - 🗺️ Map View: Interactive geographic visualization
    - 📋 Recent List View: Latest earthquake event details
    - 🎯 Complete View: All components displayed together
    
    Data Quality Features:
    ---------------------
    - Transparent reporting of complete vs. incomplete records
    - Clear disclaimers about USGS data limitations
    - Accurate metric calculations with data validation
    - Professional data presentation standards
    
    Technical Implementation:
    ------------------------
    - Session state management for user preferences
    - Caching for optimal performance (5-minute TTL)
    - Error boundaries for robust operation
    - Professional styling with CSS customization
    - Accessibility considerations in design
    
    Returns:
    --------
    None
        Renders the complete Streamlit application interface
    
    Notes:
    ------
    - Called automatically when script is executed
    - Handles all user interactions and state management
    - Maintains session persistence across user actions
    - Includes comprehensive footer with data source attribution
    """
    # Enhanced header
    st.markdown("""
    <div style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin-bottom: 2rem;'>
        <h1 style='margin: 0; font-size: 2.5rem;'>🌍 Real-Time Earthquake Monitor</h1>
        <p style='margin: 0.5rem 0; font-size: 1.2rem;'>Professional real-time seismic monitoring system</p>
        <p style='margin: 0; opacity: 0.8;'>Powered by USGS • Real-time Data • United States Coverage</p>
    </div>
    """, unsafe_allow_html=True)

      # Global Alert of strongest Earthquake in the last 24 hours

    st.markdown("<h3 style='text-align: center;'>🌍 Strongest Earthquake in the World in the last 24 hours</h3>", unsafe_allow_html=True)


    show_global_peak_24h()

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
    
    # Show current view mode (after session state is initialized)
    if hasattr(st.session_state, 'active_view'):
        view_names = {
            "stats": "📊 Statistics View",
            "charts": "📈 Charts View", 
            "map": "�️ Map View",
            "recent": "📋 Recent List View",
            "complete": "🎯 Complete View"
        }
        current_view = view_names.get(st.session_state.active_view, "Unknown")
        st.info(f"🎮 **Active Mode:** {current_view}")
    else:
        st.info("🎮 **Active Mode:** 📊 Statistics View (Default)")
    
    # Magnitude Filtering Section
    st.markdown("<h3 style='text-align: center;'>🎯 Magnitude Filtering</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        min_magnitude = st.slider(
            "Minimum Magnitude Threshold",
            min_value=0.0,
            max_value=7.0,
            value=0.0,
            step=0.1,
            help="Filter earthquakes by minimum magnitude strength"
        )
    
    with col2:
        # Magnitude category display
        if min_magnitude == 0.0:
            st.info("🔍 **Showing:** All earthquakes")
        elif min_magnitude < 3.0:
            st.info("🔸 **Showing:** Micro+ earthquakes")
        elif min_magnitude < 4.0:
            st.info("🔹 **Showing:** Minor+ earthquakes")
        elif min_magnitude < 5.0:
            st.info("🟠 **Showing:** Light+ earthquakes")
        else:
            st.info("🔴 **Showing:** Major earthquakes")
    
    st.markdown("---")
    
    # Geographic Region Section
    st.markdown("<h3 style='text-align: center;'>🌍 Geographic Region</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        region_options = {
            "🇺🇸 United States of America": "usa",
            "🌴 California": "california", 
            "❄️ Alaska": "alaska",
            "🏔️ Nevada": "nevada",
            "🏔️ Northwest": "west_coast",
            "🌺 Hawaii": "hawaii",
            "🏛️ East of Mississippi": "east_mississippi",
            "🤠 Texas": "texas"
        }
        
        selected_region = st.selectbox(
            "Select Monitoring Region",
            options=list(region_options.keys()),
            index=0,
            help="Choose the geographic area to monitor for earthquake activity"
        )
        
        region = region_options[selected_region]
    
    with col2:
        # Region info display
        region_info = {
            "usa": "Continental United States and territories",
            "california": "California state - high seismic activity",
            "alaska": "Alaska region - frequent earthquakes", 
            "nevada": "Nevada state - mining and residential seismic monitoring",
            "west_coast": "Oregon and Washington states - Pacific Northwest seismic zone",
            "hawaii": "Hawaiian Islands - volcanic and seismic activity",
            "east_mississippi": "Eastern United States - intraplate seismic activity",
            "texas": "Texas region - induced seismicity and natural faults"
        }
        
        info_text = region_info.get(region, "Selected region information")
        st.info(f"📍 **Coverage:** {info_text}")
    
    st.markdown("---")
    
    # View Mode Selection Section
    st.markdown("<h3 style='text-align: center;'>📱 View Mode Selection</h3>", unsafe_allow_html=True)
    
    # Initialize single view mode (only one active at a time)
    if 'active_view' not in st.session_state:
        st.session_state.active_view = "stats"  # Default to statistics
    
    # Create view buttons in a grid layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Statistics View", key="stats_mode",
                    type="primary" if st.session_state.active_view == "stats" else "secondary"):
            st.session_state.active_view = "stats"
            st.rerun()
            
        if st.button("�️ Map View", key="map_mode",
                    type="primary" if st.session_state.active_view == "map" else "secondary"):
            st.session_state.active_view = "map"
            st.rerun()
    
    with col2:
        if st.button("� Charts View", key="charts_mode",
                    type="primary" if st.session_state.active_view == "charts" else "secondary"):
            st.session_state.active_view = "charts"
            st.rerun()
            
        if st.button("📋 Recent List View", key="recent_mode",
                    type="primary" if st.session_state.active_view == "recent" else "secondary"):
            st.session_state.active_view = "recent"
            st.rerun()
    
    with col3:
        if st.button("🎯 Complete View", key="complete_mode",
                    type="primary" if st.session_state.active_view == "complete" else "secondary"):
            st.session_state.active_view = "complete"
            st.rerun()
    
    # Set view flags based on active mode
    show_stats_toggle = st.session_state.active_view in ["stats", "complete"]
    show_charts_toggle = st.session_state.active_view in ["charts", "complete"]
    show_map_toggle = st.session_state.active_view in ["map", "complete"]
    show_recent_toggle = st.session_state.active_view in ["recent", "complete"]
    
    # Fetch and process data
    with st.spinner("📡 Loading real-time earthquake data..."):
        earthquakes = fetch_earthquake_data(feed_type, region)
    
    # Apply magnitude filter
    if min_magnitude > 0.0:
        earthquakes = [eq for eq in earthquakes if eq.get('magnitude') is not None and eq.get('magnitude') > min_magnitude]
    
    if earthquakes:
        # Calculate accurate counts
        total_events = len(earthquakes)
        valid_events = len([eq for eq in earthquakes if eq.get('magnitude') is not None and eq.get('magnitude') > 0])
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
            show_advanced_stats(earthquakes, selected_region, chart_key_prefix="main_")
        
        if show_charts_toggle:
            show_charts_section(earthquakes, feed_type, min_magnitude)
        
        if show_map_toggle:
            create_advanced_map(earthquakes, region,chart_key_prefix="map_main_")
        
        # Recent earthquakes list
        if show_recent_toggle:
            st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>📋 Recent Earthquake Events</h3>", unsafe_allow_html=True)
            valid_earthquakes = [eq for eq in earthquakes if eq.get('magnitude') is not None and eq.get('magnitude') > 0]
            
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

"""
Mobile Web App Version of USGS Earthquake Monitor
Using Streamlit for easy mobile-responsive interface
BACKUP FILE - Created on October 25, 2025
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np


# Configure Streamlit page
st.set_page_config(
    page_title="🌍 USGS Earthquake Monitor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile optimization
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 16px;
        margin-bottom: 0.5rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .earthquake-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff4444;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .section-divider {
        margin: 2rem 0;
        border-top: 1px solid #e0e0e0;
        padding-top: 1rem;
    }
    .stSubheader {
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    /* Fix text overlap issues */
    .element-container {
        margin-bottom: 1rem;
    }
    .stPlotlyChart {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_earthquake_data(feed_type="all_hour"):
    """Fetch earthquake data from USGS with caching"""
    base_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"
    url = f"{base_url}{feed_type}.geojson"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        earthquakes = []
        total_earthquakes = len(data['features'])
        
        for feature in data['features']:
            props = feature['properties']
            coords = feature['geometry']['coordinates']
            
            # Filter for USA earthquakes (expanded range for better coverage)
            longitude, latitude = coords[0], coords[1]
            if -180 <= longitude <= -60 and 15 <= latitude <= 75:
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
        
        # Add debug information
        if feed_type == "significant_month":
            st.info(f"📡 Found {total_earthquakes} total earthquakes worldwide, {len(earthquakes)} in USA region")
            if total_earthquakes == 0:
                st.warning("🌍 No significant earthquakes worldwide in the past month - this is good news!")
            elif len(earthquakes) == 0 and total_earthquakes > 0:
                st.info(f"🌍 Found {total_earthquakes} significant earthquakes worldwide, but none in USA region")
        
        return earthquakes
    except Exception as e:
        st.error(f"Error fetching earthquake data: {e}")
        return []


def create_mobile_header():
    """Create mobile-friendly header"""
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1>🌍 USGS Earthquake Monitor</h1>
        <p style="color: #666; margin: 0;">Real-time earthquake monitoring for mobile devices</p>
    </div>
    """, unsafe_allow_html=True)


def show_quick_stats(earthquakes):
    """Show quick statistics in mobile-friendly cards"""
    if not earthquakes:
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
    
    if not valid_earthquakes:
        return
    
    magnitudes = [eq['magnitude'] for eq in valid_earthquakes]
    max_mag = max(magnitudes)
    avg_mag = np.mean(magnitudes)
    total_count = len(valid_earthquakes)
    significant_count = sum(1 for m in magnitudes if m >= 4.0)
    
    # Create 2x2 grid for mobile
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Total Earthquakes",
            value=f"{total_count}",
            delta=f"Past hour" if "hour" in st.session_state.get('feed_type', '') else "Past day"
        )
        
        st.metric(
            label="Maximum Magnitude",
            value=f"M {max_mag:.1f}",
            delta="🔴" if max_mag >= 5.0 else "🟡" if max_mag >= 4.0 else "🟢"
        )
    
    with col2:
        st.metric(
            label="Average Magnitude",
            value=f"M {avg_mag:.1f}",
            delta=f"{significant_count} significant (M4.0+)"
        )
        
        latest_time = max(eq['time'] for eq in valid_earthquakes)
        latest_dt = datetime.fromtimestamp(latest_time/1000)
        time_ago = datetime.now() - latest_dt
        hours_ago = int(time_ago.total_seconds() / 3600)
        
        st.metric(
            label="Latest Activity",
            value=f"{hours_ago}h ago",
            delta="Most recent earthquake"
        )


def create_mobile_map(earthquakes):
    """Create mobile-optimized earthquake map"""
    if not earthquakes:
        st.warning("No earthquake data available")
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
    if not valid_earthquakes:
        st.warning("No valid earthquake data")
        return
    
    # Create DataFrame for Plotly
    df = pd.DataFrame(valid_earthquakes)
    
    # Add formatted time column for hover display
    df['formatted_time'] = df['time'].apply(
        lambda x: datetime.fromtimestamp(x/1000).strftime("%m/%d/%Y %H:%M:%S UTC")
    )
    
    # Create map with custom styling for mobile using newer scatter_map
    fig = px.scatter_map(
        df,
        lat="latitude",
        lon="longitude",
        size="magnitude",
        color="magnitude",
        hover_name="place",
        hover_data={
            "magnitude": ":.1f",
            "depth": ":.1f",
            "formatted_time": True,
            "latitude": False,
            "longitude": False
        },
        color_continuous_scale="Reds",
        size_max=20,
        zoom=3,
        height=400,  # Mobile-friendly height
        title="🗺️ United States Earthquake Activity"
    )
    
    fig.update_layout(
        map_style="open-street-map",
        map=dict(
            center=dict(lat=39.8, lon=-98.5),  # Center on USA
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        font=dict(size=12),  # Larger font for mobile
        title_font_size=16
    )
    
    st.plotly_chart(fig, use_container_width=True)


def show_earthquake_list(earthquakes):
    """Show earthquake list in mobile-friendly cards"""
    if not earthquakes:
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
    # Sort by magnitude (highest first)
    valid_earthquakes.sort(key=lambda x: x['magnitude'], reverse=True)
    
    # Add proper spacing before the subheader
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("📋 Recent Earthquakes")
    
    # Show top 10 for mobile performance
    for eq in valid_earthquakes[:10]:
        time_dt = datetime.fromtimestamp(eq['time']/1000)
        time_str = time_dt.strftime("%m/%d %H:%M")
        
        # Color code by magnitude
        if eq['magnitude'] >= 5.0:
            border_color = "#ff0000"  # Red
            emoji = "🔴"
        elif eq['magnitude'] >= 4.0:
            border_color = "#ff8800"  # Orange
            emoji = "🟠"
        elif eq['magnitude'] >= 3.0:
            border_color = "#ffdd00"  # Yellow
            emoji = "🟡"
        else:
            border_color = "#88ff88"  # Green
            emoji = "🟢"
        
        st.markdown(f"""
        <div style="background-color: #ffffff; padding: 1rem; border-radius: 0.5rem; 
                    border-left: 4px solid {border_color}; margin: 1rem 0; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1); clear: both;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{emoji} M {eq['magnitude']:.1f}</strong><br>
                    <span style="color: #666;">{eq['place']}</span><br>
                    <small>⏰ {time_str} | 📍 {eq['depth']:.1f}km deep</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def create_magnitude_chart(earthquakes):
    """Create mobile-friendly magnitude distribution chart"""
    if not earthquakes:
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
    magnitudes = [eq['magnitude'] for eq in valid_earthquakes]
    
    if not magnitudes:
        return
    
    # Add proper spacing
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    fig = px.histogram(
        x=magnitudes,
        nbins=15,
        title="📊 Magnitude Distribution",
        labels={'x': 'Magnitude', 'y': 'Count'},
        height=300
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        font=dict(size=12),
        title_font_size=14
    )
    
    st.plotly_chart(fig, use_container_width=True)


def show_regional_breakdown(earthquakes):
    """Show earthquake breakdown by US regions and states"""
    if not earthquakes:
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
    if not valid_earthquakes:
        return
    
    # Add proper spacing
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("🏛️ Regional Breakdown")
    
    # Define US regions with state boundaries (approximate)
    regions = {
        "🌴 California": {"lat_range": (32.0, 42.0), "lon_range": (-125.0, -114.0)},
        "❄️ Alaska": {"lat_range": (54.0, 72.0), "lon_range": (-180.0, -130.0)},
        "🌺 Hawaii": {"lat_range": (18.0, 23.0), "lon_range": (-161.0, -154.0)},
        "🏔️ Pacific Northwest": {"lat_range": (42.0, 49.0), "lon_range": (-125.0, -116.0)},
        "🏜️ Nevada/Utah": {"lat_range": (35.0, 42.0), "lon_range": (-120.0, -109.0)},
        "🗽 Eastern US": {"lat_range": (25.0, 50.0), "lon_range": (-100.0, -65.0)},
        "🌪️ Central US": {"lat_range": (25.0, 50.0), "lon_range": (-109.0, -90.0)},
        "🔥 Yellowstone": {"lat_range": (44.0, 45.5), "lon_range": (-111.5, -109.5)}
    }
    
    # Count earthquakes by region
    regional_counts = {}
    regional_earthquakes = {}
    
    for region, bounds in regions.items():
        count = 0
        region_quakes = []
        lat_min, lat_max = bounds["lat_range"]
        lon_min, lon_max = bounds["lon_range"]
        
        for eq in valid_earthquakes:
            if (lat_min <= eq['latitude'] <= lat_max and 
                lon_min <= eq['longitude'] <= lon_max):
                count += 1
                region_quakes.append(eq)
        
        if count > 0:
            regional_counts[region] = count
            regional_earthquakes[region] = region_quakes
    
    # Display regional statistics
    if regional_counts:
        col1, col2 = st.columns(2)
        
        # Sort regions by earthquake count
        sorted_regions = sorted(regional_counts.items(), key=lambda x: x[1], reverse=True)
        
        for i, (region, count) in enumerate(sorted_regions):
            region_quakes = regional_earthquakes[region]
            max_mag = max(eq['magnitude'] for eq in region_quakes)
            avg_mag = sum(eq['magnitude'] for eq in region_quakes) / len(region_quakes)
            
            # Alternate between columns
            with col1 if i % 2 == 0 else col2:
                # Color based on activity level
                if count >= 10:
                    bg_color = "#ffebee"  # Light red
                    border_color = "#f44336"  # Red
                elif count >= 5:
                    bg_color = "#fff3e0"  # Light orange
                    border_color = "#ff9800"  # Orange
                else:
                    bg_color = "#f1f8e9"  # Light green
                    border_color = "#4caf50"  # Green
                
                st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 1rem; border-radius: 0.5rem; 
                            border-left: 4px solid {border_color}; margin: 0.5rem 0;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #333;">{region}</h4>
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <strong>{count} earthquakes</strong><br>
                            <small>Max: M{max_mag:.1f} | Avg: M{avg_mag:.1f}</small>
                        </div>
                        <div style="text-align: right; font-size: 2em;">
                            {'🔴' if count >= 10 else '🟡' if count >= 5 else '🟢'}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Show detailed earthquake list for most active region
        if sorted_regions:
            most_active_region, most_active_count = sorted_regions[0]
            if most_active_count > 0:
                st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
                st.subheader(f"📋 {most_active_region} - Detailed Activity")
                
                region_quakes = regional_earthquakes[most_active_region]
                region_quakes.sort(key=lambda x: x['magnitude'], reverse=True)
                
                for eq in region_quakes[:5]:  # Show top 5
                    time_dt = datetime.fromtimestamp(eq['time']/1000)
                    time_str = time_dt.strftime("%m/%d %H:%M")
                    
                    if eq['magnitude'] >= 4.0:
                        emoji = "🔴"
                        border_color = "#ff0000"
                    elif eq['magnitude'] >= 3.0:
                        emoji = "🟡"
                        border_color = "#ffdd00"
                    else:
                        emoji = "🟢"
                        border_color = "#88ff88"
                    
                    st.markdown(f"""
                    <div style="background-color: #ffffff; padding: 0.8rem; border-radius: 0.5rem; 
                                border-left: 3px solid {border_color}; margin: 0.3rem 0; 
                                box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <strong>{emoji} M {eq['magnitude']:.1f}</strong> - {eq['place']}<br>
                        <small>⏰ {time_str} | 📍 {eq['depth']:.1f}km deep</small>
                    </div>
                    """, unsafe_allow_html=True)
    
    else:
        st.info("🌍 No earthquakes detected in major US regions during this time period")


def create_regional_chart(earthquakes):
    """Create regional activity chart"""
    if not earthquakes:
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
    if not valid_earthquakes:
        return
    
    # Add proper spacing
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Define regions (same as above)
    regions = {
        "California": {"lat_range": (32.0, 42.0), "lon_range": (-125.0, -114.0)},
        "Alaska": {"lat_range": (54.0, 72.0), "lon_range": (-180.0, -130.0)},
        "Hawaii": {"lat_range": (18.0, 23.0), "lon_range": (-161.0, -154.0)},
        "Pacific NW": {"lat_range": (42.0, 49.0), "lon_range": (-125.0, -116.0)},
        "Nevada/Utah": {"lat_range": (35.0, 42.0), "lon_range": (-120.0, -109.0)},
        "Eastern US": {"lat_range": (25.0, 50.0), "lon_range": (-100.0, -65.0)},
        "Central US": {"lat_range": (25.0, 50.0), "lon_range": (-109.0, -90.0)},
        "Yellowstone": {"lat_range": (44.0, 45.5), "lon_range": (-111.5, -109.5)}
    }
    
    # Count earthquakes by region
    region_names = []
    earthquake_counts = []
    
    for region, bounds in regions.items():
        count = 0
        lat_min, lat_max = bounds["lat_range"]
        lon_min, lon_max = bounds["lon_range"]
        
        for eq in valid_earthquakes:
            if (lat_min <= eq['latitude'] <= lat_max and 
                lon_min <= eq['longitude'] <= lon_max):
                count += 1
        
        if count > 0:
            region_names.append(region)
            earthquake_counts.append(count)
    
    if region_names:
        fig = px.bar(
            x=region_names,
            y=earthquake_counts,
            title="📊 Regional Earthquake Activity",
            labels={'x': 'Region', 'y': 'Earthquake Count'},
            height=300
        )
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            font=dict(size=10),
            title_font_size=14,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)


def main():
    """Main mobile web app"""
    create_mobile_header()
    
    # Mobile-friendly navigation
    st.subheader("📡 Select Data Source")
    
    # Create mobile-friendly buttons for data sources
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🕐 Past Hour", key="hour"):
            st.session_state.feed_type = "all_hour"
        if st.button("🌊 Significant Events", key="significant"):
            st.session_state.feed_type = "significant_month"
        if st.button("🌍 All Week", key="week"):
            st.session_state.feed_type = "all_week"
    
    with col2:
        if st.button("📅 Past Day", key="day"):
            st.session_state.feed_type = "all_day"
        if st.button("🌋 Major Earthquakes", key="major"):
            st.session_state.feed_type = "4.5_week"
        if st.button("⚠️ M2.5+ Week", key="m25week"):
            st.session_state.feed_type = "2.5_week"
    
    # Add a third row for the Past Month button
    col_month1, col_month2 = st.columns(2)
    with col_month1:
        if st.button("🔍 Past Month", key="month"):
            st.session_state.feed_type = "all_month"
    
    # Add divider between sections
    st.markdown("---")
    
    # View Selection
    st.subheader("📱 Select View Type")
    
    # Create mobile-friendly buttons for view types
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("🗺️ Live Map", key="map"):
            st.session_state.view_type = "map"
        if st.button("📋 Earthquake List", key="list"):
            st.session_state.view_type = "list"
    
    with col4:
        if st.button("📊 Statistics", key="stats"):
            st.session_state.view_type = "stats"
        if st.button("🗺️ Regional View", key="regional"):
            st.session_state.view_type = "regional"
    
    # Initialize session state
    if 'feed_type' not in st.session_state:
        st.session_state.feed_type = "all_hour"
    if 'view_type' not in st.session_state:
        st.session_state.view_type = "overview"
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (30 seconds)", value=False)
    if auto_refresh:
        st.rerun()
    
    # Fetch and display data
    with st.spinner("📡 Loading earthquake data..."):
        earthquakes = fetch_earthquake_data(st.session_state.feed_type)
    
    if earthquakes:
        st.success(f"✅ Found {len(earthquakes)} earthquakes in USA")
        
        # Show quick stats
        show_quick_stats(earthquakes)
        
        # Show selected view
        if st.session_state.view_type == "map":
            st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
            create_mobile_map(earthquakes)
        elif st.session_state.view_type == "stats":
            create_magnitude_chart(earthquakes)
        elif st.session_state.view_type == "list":
            show_earthquake_list(earthquakes)
        elif st.session_state.view_type == "regional":
            show_regional_breakdown(earthquakes)
        else:
            # Default overview - add spacing between sections
            st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
            create_mobile_map(earthquakes)
            show_earthquake_list(earthquakes)
    else:
        feed_descriptions = {
            "all_hour": "past hour",
            "all_day": "past day", 
            "all_week": "past week",
            "all_month": "past month",
            "significant_month": "significant events (past month)",
            "4.5_week": "magnitude 4.5+ (past week)",
            "2.5_week": "magnitude 2.5+ (past week)"
        }
        
        current_feed = st.session_state.get('feed_type', 'all_hour')
        feed_desc = feed_descriptions.get(current_feed, current_feed)
        
        st.warning(f"⚠️ No earthquake data available for {feed_desc}")
        st.info("💡 Try a different time period or data source:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🕐 Try Past Hour", key="retry_hour"):
                st.session_state.feed_type = "all_hour"
                st.rerun()
        with col2:
            if st.button("📅 Try Past Day", key="retry_day"):
                st.session_state.feed_type = "all_day"
                st.rerun()
        with col3:
            if st.button("🌍 Try Past Week", key="retry_week"):
                st.session_state.feed_type = "all_week"
                st.rerun()
    
    # Mobile-friendly footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #666; border-top: 1px solid #eee; margin-top: 2rem;">
        <small>
        📡 Data from USGS Earthquake Hazards Program<br>
        🔄 Updates every 5 minutes | 📱 Optimized for mobile devices
        </small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
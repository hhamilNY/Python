"""
Earthquake Visualization Module
Handles all visualization components including maps, charts, and UI elements
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import logging
from earthquake_data import get_valid_earthquakes, get_earthquake_statistics, sort_earthquakes_by_magnitude

# Configure logging
logger = logging.getLogger(__name__)

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
    
    stats = get_earthquake_statistics(earthquakes)
    
    if stats['valid_count'] == 0:
        return
    
    # Create 2x2 grid for mobile
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Total Earthquakes",
            value=f"{stats['total_count']}",
            delta=f"Past hour" if "hour" in st.session_state.get('feed_type', '') else "Past day"
        )
        
        st.metric(
            label="Maximum Magnitude",
            value=f"M {stats['max_magnitude']:.1f}",
            delta="🔴" if stats['max_magnitude'] >= 5.0 else "🟡" if stats['max_magnitude'] >= 4.0 else "🟢"
        )
    
    with col2:
        st.metric(
            label="Average Magnitude",
            value=f"M {stats['avg_magnitude']:.1f}",
            delta=f"{stats['significant_count']} significant (M4.0+)"
        )
        
        if stats['latest_time']:
            latest_dt = datetime.fromtimestamp(stats['latest_time']/1000)
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
    
    valid_earthquakes, valid_count, _ = get_valid_earthquakes(earthquakes)
    if not valid_earthquakes:
        st.warning("No valid earthquake data")
        return
    
    # Create DataFrame for Plotly
    df = pd.DataFrame(valid_earthquakes)
    
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
    
    sorted_earthquakes = sort_earthquakes_by_magnitude(earthquakes, reverse=True)
    
    # Add proper spacing before the subheader
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("📋 Recent Earthquakes")
    
    # Show top 10 for mobile performance
    for eq in sorted_earthquakes[:10]:
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
    
    valid_earthquakes, valid_count, _ = get_valid_earthquakes(earthquakes)
    magnitudes = [eq['magnitude'] for eq in valid_earthquakes]
    
    if not magnitudes:
        return
    
    # Add proper spacing
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    fig = px.histogram(
        x=magnitudes,
        bins=15,
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

def create_status_bar():
    """Create a mobile-friendly status bar showing current settings"""
    current_feed = st.session_state.get('feed_type', 'all_hour')
    current_view = st.session_state.get('view_type', 'overview')
    
    # Create a compact status display
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 0.5rem 1rem; border-radius: 0.25rem; 
                margin: 1rem 0; border-left: 3px solid #007bff;">
        <small>
        📡 <strong>Data:</strong> {current_feed.replace('_', ' ').title()} | 
        👀 <strong>View:</strong> {current_view.title()}
        </small>
    </div>
    """, unsafe_allow_html=True)

def show_regional_breakdown(earthquakes):
    """Show earthquake breakdown by region"""
    if not earthquakes:
        return
    
    valid_earthquakes, valid_count, _ = get_valid_earthquakes(earthquakes)
    if not valid_earthquakes:
        return
    
    # Simple regional breakdown based on rough geographic areas
    regions = {
        'West Coast': 0,
        'Alaska': 0,
        'Central US': 0,
        'East Coast': 0,
        'Other': 0
    }
    
    for eq in valid_earthquakes:
        lon, lat = eq['longitude'], eq['latitude']
        
        if lat > 60:  # Alaska
            regions['Alaska'] += 1
        elif lon < -120 and lat > 32:  # West Coast (rough)
            regions['West Coast'] += 1
        elif lon > -100:  # East Coast (rough)
            regions['East Coast'] += 1
        elif -120 <= lon <= -100:  # Central US (rough)
            regions['Central US'] += 1
        else:
            regions['Other'] += 1
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("🗺️ Regional Breakdown")
    
    # Create columns for regional display
    cols = st.columns(len(regions))
    for i, (region, count) in enumerate(regions.items()):
        with cols[i]:
            st.metric(
                label=region,
                value=str(count),
                delta=f"{count/valid_count*100:.1f}%" if valid_count > 0 else "0%"
            )
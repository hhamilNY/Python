"""
Mobile Web App Version of USGS Earthquake Monitor
Using Streamlit for easy mobile-responsive interface
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import logging
import logging.handlers
import time
import os
from functools import wraps
from visitor_metrics import get_metrics


# Configure logging with rotation
def setup_logging():
    """Setup rotating file logger with size and count limits"""
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logger
    logger = logging.getLogger('earthquake_app')
    logger.setLevel(logging.DEBUG)
    
    # Avoid duplicate handlers if logger already exists
    if not logger.handlers:
        # Create rotating file handler: 5MB max, keep 10 files
        handler = logging.handlers.RotatingFileHandler(
            filename=os.path.join(log_dir, 'earthquake_app.log'),
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=10,
            encoding='utf-8'
        )
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)8s | %(funcName)20s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
    
    return logger

# Initialize logger
logger = setup_logging()

def log_performance(func):
    """Decorator to log function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function_name = func.__name__
        
        try:
            logger.info(f"Starting {function_name}")
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"Completed {function_name} in {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Error in {function_name} after {execution_time:.3f}s: {str(e)}")
            raise
    return wrapper

def log_user_action(action, details=None):
    """Log user interactions"""
    session_id = st.session_state.get('session_id', 'unknown')
    log_msg = f"USER_ACTION | Session: {session_id} | Action: {action}"
    if details:
        log_msg += f" | Details: {details}"
    logger.info(log_msg)
    
    # Record in persistent metrics
    metrics = get_metrics()
    metrics.record_user_action(action, details)

def track_visitor():
    """Track unique visitors and page views"""
    # Get or create visitor ID (persists across browser sessions)
    visitor_id = st.session_state.get('visitor_id')
    if not visitor_id:
        import uuid
        visitor_id = str(uuid.uuid4())[:12]  # Longer ID for visitors
        st.session_state.visitor_id = visitor_id
        
        # Log new visitor
        logger.info(f"NEW_VISITOR | ID: {visitor_id} | Session: {st.session_state.get('session_id', 'unknown')}")
        
        # Record in persistent metrics
        metrics = get_metrics()
        metrics.record_new_visitor(visitor_id)
        
        # Try to get basic browser info (if available)
        user_agent = ""
        try:
            # Get user agent from streamlit context if available
            if hasattr(st, 'context') and hasattr(st.context, 'headers'):
                user_agent = st.context.headers.get('User-Agent', 'Unknown')
        except:
            user_agent = "Unknown"
        
        logger.info(f"VISITOR_INFO | ID: {visitor_id} | UserAgent: {user_agent}")
    
    # Track page view for existing or new visitor
    logger.info(f"PAGE_VIEW | Visitor: {visitor_id} | Session: {st.session_state.get('session_id', 'unknown')}")
    
    # Record page view in persistent metrics
    metrics = get_metrics()
    metrics.record_page_view(visitor_id)
    
    return visitor_id

def get_visit_stats():
    """Get visitor statistics from persistent metrics (fallback to logs)"""
    try:
        # First try persistent metrics
        metrics = get_metrics()
        stats = metrics.get_summary_stats()
        
        return {
            "unique_visitors": stats["total_unique_visitors"],
            "page_views": stats["total_page_views"],
            "new_visitors_today": stats["new_visitors_today"],
            "total_sessions": stats["total_sessions"],
            "days_active": stats["days_active"],
            "avg_page_views_per_visitor": stats["avg_page_views_per_visitor"]
        }
        
    except Exception as e:
        logger.error(f"STATS_ERROR | Failed to get persistent stats, falling back to logs: {e}")
        
        # Fallback to log parsing
        try:
            import os
            log_file = os.path.join("logs", "earthquake_app.log")
            
            if not os.path.exists(log_file):
                return {"unique_visitors": 0, "page_views": 0, "new_visitors_today": 0}
            
            unique_visitors = set()
            page_views = 0
            new_visitors_today = 0
            today = datetime.now().strftime("%Y-%m-%d")
            
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if "NEW_VISITOR" in line:
                        # Extract visitor ID from log line
                        try:
                            visitor_part = line.split("ID: ")[1].split(" |")[0]
                            unique_visitors.add(visitor_part)
                            
                            # Check if visitor is from today
                            if today in line:
                                new_visitors_today += 1
                        except:
                            pass
                    elif "PAGE_VIEW" in line:
                        page_views += 1
            
            return {
                "unique_visitors": len(unique_visitors),
                "page_views": page_views,
                "new_visitors_today": new_visitors_today
            }
        except Exception as e2:
            logger.error(f"STATS_ERROR | Failed to get stats from logs: {e2}")
            return {"unique_visitors": 0, "page_views": 0, "new_visitors_today": 0}

def get_detailed_analytics():
    """Get detailed analytics from persistent metrics (fallback to logs)"""
    try:
        # First try persistent metrics
        metrics = get_metrics()
        popular = metrics.get_popular_items()
        summary = metrics.get_summary_stats()
        
        analytics = {
            "daily_visitors": {},  # Could add daily breakdown if needed
            "popular_data_sources": popular["data_sources"],
            "popular_views": popular["views"],
            "user_actions": popular["actions"],
            "session_count": summary["total_sessions"],
            "errors": []  # Errors still come from logs
        }
        
        # Still get errors from logs since they're not stored in metrics
        try:
            import os
            log_file = os.path.join("logs", "earthquake_app.log")
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if "ERROR" in line:
                            analytics["errors"].append(line.strip())
        except:
            pass
        
        return analytics
        
    except Exception as e:
        logger.error(f"ANALYTICS_ERROR | Failed to get persistent analytics, falling back to logs: {e}")
        
        # Fallback to original log parsing
        try:
            import os
            from collections import defaultdict
            
            log_file = os.path.join("logs", "earthquake_app.log")
            if not os.path.exists(log_file):
                return {}
            
            analytics = {
                "daily_visitors": defaultdict(int),
                "popular_data_sources": defaultdict(int),
                "popular_views": defaultdict(int),
                "user_actions": defaultdict(int),
                "session_count": 0,
                "errors": []
            }
            
            sessions = set()
            
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        # Extract date
                        date_part = line.split(" |")[0].split()[0]
                        
                        if "NEW_VISITOR" in line:
                            analytics["daily_visitors"][date_part] += 1
                        
                        elif "SESSION_START" in line:
                            session_id = line.split("session: ")[1].split(" |")[0]
                            sessions.add(session_id)
                        
                        elif "data_source_change" in line:
                            source = line.split("Details: ")[1].strip()
                            analytics["popular_data_sources"][source] += 1
                        
                        elif "view_change" in line:
                            view = line.split("Details: ")[1].strip()
                            analytics["popular_views"][view] += 1
                        
                        elif "USER_ACTION" in line:
                            action = line.split("Action: ")[1].split(" |")[0]
                            analytics["user_actions"][action] += 1
                        
                        elif "ERROR" in line:
                            analytics["errors"].append(line.strip())
                            
                    except:
                        continue
            
            analytics["session_count"] = len(sessions)
            return analytics
            
        except Exception as e2:
            logger.error(f"ANALYTICS_ERROR | Failed to get analytics from logs: {e2}")
            return {}

def show_admin_dashboard():
    """Show admin analytics dashboard (hidden feature)"""
    st.sidebar.title("📊 Analytics Dashboard")
    
    # Basic stats
    stats = get_visit_stats()
    st.sidebar.metric("🌍 Unique Visitors", stats["unique_visitors"])
    st.sidebar.metric("👀 Total Page Views", stats["page_views"])
    st.sidebar.metric("🆕 New Today", stats["new_visitors_today"])
    
    # Detailed analytics
    analytics = get_detailed_analytics()
    
    if analytics:
        st.sidebar.metric("🔗 Total Sessions", analytics["session_count"])
        
        # Popular data sources
        if analytics["popular_data_sources"]:
            st.sidebar.subheader("📡 Popular Data Sources")
            for source, count in sorted(analytics["popular_data_sources"].items(), 
                                      key=lambda x: x[1], reverse=True)[:3]:
                st.sidebar.write(f"• {source}: {count}")
        
        # Popular views
        if analytics["popular_views"]:
            st.sidebar.subheader("📱 Popular Views")
            for view, count in sorted(analytics["popular_views"].items(), 
                                    key=lambda x: x[1], reverse=True)[:3]:
                st.sidebar.write(f"• {view}: {count}")
        
        # Recent errors
        if analytics["errors"]:
            with st.sidebar.expander("⚠️ Recent Errors", expanded=False):
                for error in analytics["errors"][-5:]:  # Show last 5 errors
                    st.write(f"🔴 {error[-100:]}")  # Truncate long errors


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
    .stButton > button[data-testid*="baseButton-secondary"] {
        background-color: #f0f2f6;
        border: 2px solid #e0e0e0;
    }
    .stButton > button[data-testid*="baseButton-primary"] {
        background-color: #0066cc !important;
        color: white !important;
        border: 2px solid #0066cc !important;
        box-shadow: 0 2px 4px rgba(0,102,204,0.3) !important;
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
@log_performance
def fetch_earthquake_data(feed_type="all_hour"):
    """Fetch earthquake data from USGS with caching"""
    base_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"
    url = f"{base_url}{feed_type}.geojson"
    
    logger.info(f"DATA_FETCH | Requesting data from: {url}")
    
    try:
        request_start = time.time()
        response = requests.get(url, timeout=10)
        request_time = time.time() - request_start
        
        logger.info(f"DATA_FETCH | HTTP request completed in {request_time:.3f}s | Status: {response.status_code}")
        
        response.raise_for_status()
        data = response.json()
        
        earthquakes = []
        total_earthquakes = len(data['features'])
        
        logger.info(f"DATA_FETCH | Raw data received: {total_earthquakes} earthquakes worldwide")
        
        # Track filtering metrics
        filter_start = time.time()
        usa_count = 0
        coordinate_errors = 0
        
        for feature in data['features']:
            props = feature['properties']
            coords = feature['geometry']['coordinates']
            
            try:
                # Filter for USA earthquakes (expanded range for better coverage)
                longitude, latitude = coords[0], coords[1]
                if -180 <= longitude <= -60 and 15 <= latitude <= 75:
                    usa_count += 1
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
            except (IndexError, TypeError) as e:
                coordinate_errors += 1
                logger.warning(f"DATA_FETCH | Coordinate error for earthquake: {e}")
        
        filter_time = time.time() - filter_start
        
        logger.info(f"DATA_FETCH | Filtering completed in {filter_time:.3f}s")
        logger.info(f"DATA_FETCH | Results: {total_earthquakes} worldwide → {usa_count} USA region")
        
        if coordinate_errors > 0:
            logger.warning(f"DATA_FETCH | {coordinate_errors} earthquakes had coordinate errors")
        
        # Log data quality metrics
        if usa_count > total_earthquakes:
            logger.error(f"DATA_FETCH | ANOMALY: USA count ({usa_count}) > worldwide count ({total_earthquakes})")
        
        valid_magnitudes = sum(1 for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0)
        logger.info(f"DATA_FETCH | Valid earthquakes with magnitude: {valid_magnitudes}/{usa_count}")
        
        # Add debug information for all feed types
        if len(earthquakes) != total_earthquakes:
            st.info(f"📡 Worldwide: {total_earthquakes} earthquakes | USA region: {len(earthquakes)} earthquakes")
        
        # Special handling for significant events
        if feed_type == "significant_month":
            if total_earthquakes == 0:
                st.warning("🌍 No significant earthquakes worldwide in the past month - this is good news!")
                logger.info("DATA_FETCH | No significant earthquakes worldwide in past month")
            elif len(earthquakes) == 0 and total_earthquakes > 0:
                st.info(f"🌍 Found {total_earthquakes} significant earthquakes worldwide, but none in USA region")
                logger.info(f"DATA_FETCH | {total_earthquakes} significant earthquakes worldwide, none in USA")
        
        return earthquakes
        
    except requests.exceptions.Timeout as e:
        error_msg = f"Request timeout after 10 seconds: {e}"
        logger.error(f"DATA_FETCH | {error_msg}")
        st.error(f"Error fetching earthquake data: {error_msg}")
        return []
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {e}"
        logger.error(f"DATA_FETCH | {error_msg}")
        st.error(f"Error fetching earthquake data: {error_msg}")
        return []
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON response: {e}"
        logger.error(f"DATA_FETCH | {error_msg}")
        st.error(f"Error fetching earthquake data: {error_msg}")
        return []
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        logger.error(f"DATA_FETCH | {error_msg}")
        st.error(f"Error fetching earthquake data: {error_msg}")
        return []


def create_mobile_header():
    """Create mobile-friendly header"""
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1>🌍 USGS Earthquake Monitor</h1>
        <p style="color: #666; margin: 0;">Real-time earthquake monitoring for mobile devices</p>
    </div>
    """, unsafe_allow_html=True)


def create_status_bar():
    """Create status bar showing active data source and view type"""
    # Get current selections
    current_feed = st.session_state.get('feed_type', 'all_hour')
    current_view = st.session_state.get('view_type', 'overview')
    
    # Map feed types to display names
    feed_names = {
        "all_hour": "Past Hour",
        "all_day": "Past Day", 
        "all_week": "All Week",
        "all_month": "Past Month",
        "significant_month": "Significant Events",
        "4.5_week": "Major Earthquakes",
        "2.5_week": "M2.5+ Week"
    }
    
    # Map view types to display names
    view_names = {
        "overview": "Overview",
        "map": "Live Map",
        "list": "Earthquake List",
        "stats": "Statistics",
        "regional": "Regional View"
    }
    
    feed_display = feed_names.get(current_feed, current_feed)
    view_display = view_names.get(current_view, current_view)
    
    st.markdown(f"""
    <div style="background-color: #e8f4fd; border: 1px solid #0066cc; border-radius: 0.5rem; 
                padding: 0.8rem; margin: 1rem 0; text-align: center;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div style="margin: 0.2rem;">
                <strong style="color: #0066cc;">📡 Data:</strong> 
                <span style="color: #333;">{feed_display}</span>
            </div>
            <div style="margin: 0.2rem;">
                <strong style="color: #0066cc;">📱 View:</strong> 
                <span style="color: #333;">{view_display}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


@log_performance
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


@log_performance
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
    df['event_time'] = df['time'].apply(
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
            "event_time": True,
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
    # Check for admin dashboard access via URL parameter
    try:
        query_params = st.query_params if hasattr(st, 'query_params') else {}
        show_admin = query_params.get('admin') == 'true'
    except:
        show_admin = False
    
    # Track visitor (must be called early)
    visitor_id = track_visitor()
    
    # Initialize session tracking
    if 'session_id' not in st.session_state:
        import uuid
        st.session_state.session_id = str(uuid.uuid4())[:8]
        logger.info(f"SESSION_START | New session: {st.session_state.session_id} | Visitor: {visitor_id}")
    
    # Show admin dashboard if requested
    if show_admin:
        show_admin_dashboard()
    
    create_mobile_header()
    
    # Initialize session state first
    if 'feed_type' not in st.session_state:
        st.session_state.feed_type = "all_hour"
        logger.info(f"SESSION_INIT | Default feed_type: all_hour")
    if 'view_type' not in st.session_state:
        st.session_state.view_type = "overview"
        logger.info(f"SESSION_INIT | Default view_type: overview")
    
    # Show status bar
    create_status_bar()
    
    # Optional: Show visitor stats in main app (uncomment to enable for all users)
    # with st.expander("📊 Site Statistics", expanded=False):
    #     stats = get_visit_stats()
    #     col1, col2, col3 = st.columns(3)
    #     with col1:
    #         st.metric("Total Visitors", stats["unique_visitors"])
    #     with col2:
    #         st.metric("Page Views", stats["page_views"])
    #     with col3:
    #         st.metric("New Today", stats["new_visitors_today"])
    
    # Mobile-friendly navigation
    st.subheader("📡 Select Data Source")
    
    # Create mobile-friendly buttons for data sources
    col1, col2 = st.columns(2)
    
    # Get current feed type for highlighting
    current_feed = st.session_state.get('feed_type', 'all_hour')
    
    with col1:
        if st.button("🕐 Past Hour", key="hour", type="primary" if current_feed == "all_hour" else "secondary"):
            log_user_action("data_source_change", "all_hour")
            st.session_state.feed_type = "all_hour"
        if st.button("🌊 Significant Events", key="significant", type="primary" if current_feed == "significant_month" else "secondary"):
            log_user_action("data_source_change", "significant_month")
            st.session_state.feed_type = "significant_month"
        if st.button("🌍 All Week", key="week", type="primary" if current_feed == "all_week" else "secondary"):
            log_user_action("data_source_change", "all_week")
            st.session_state.feed_type = "all_week"
    
    with col2:
        if st.button("📅 Past Day", key="day", type="primary" if current_feed == "all_day" else "secondary"):
            log_user_action("data_source_change", "all_day")
            st.session_state.feed_type = "all_day"
        if st.button("🌋 Major Earthquakes", key="major", type="primary" if current_feed == "4.5_week" else "secondary"):
            log_user_action("data_source_change", "4.5_week")
            st.session_state.feed_type = "4.5_week"
        if st.button("⚠️ M2.5+ Week", key="m25week", type="primary" if current_feed == "2.5_week" else "secondary"):
            log_user_action("data_source_change", "2.5_week")
            st.session_state.feed_type = "2.5_week"
    
    # Add a third row for the Past Month button
    col_month1, col_month2 = st.columns(2)
    with col_month1:
        if st.button("🔍 Past Month", key="month", type="primary" if current_feed == "all_month" else "secondary"):
            log_user_action("data_source_change", "all_month")
            st.session_state.feed_type = "all_month"
    
    # Add divider between sections
    st.markdown("---")
    
    # View Selection
    st.subheader("📱 Select View Type")
    
    # Create mobile-friendly buttons for view types
    col3, col4 = st.columns(2)
    
    # Get current view type for highlighting
    current_view = st.session_state.get('view_type', 'overview')
    
    with col3:
        if st.button("🌍 Overview", key="overview", type="primary" if current_view == "overview" else "secondary"):
            log_user_action("view_change", "overview")
            st.session_state.view_type = "overview"
        if st.button("🗺️ Live Map", key="map", type="primary" if current_view == "map" else "secondary"):
            log_user_action("view_change", "map")
            st.session_state.view_type = "map"
        if st.button("📋 Earthquake List", key="list", type="primary" if current_view == "list" else "secondary"):
            log_user_action("view_change", "list")
            st.session_state.view_type = "list"
    
    with col4:
        if st.button("📊 Statistics", key="stats", type="primary" if current_view == "stats" else "secondary"):
            log_user_action("view_change", "stats")
            st.session_state.view_type = "stats"
        if st.button("🗺️ Regional View", key="regional", type="primary" if current_view == "regional" else "secondary"):
            log_user_action("view_change", "regional")
            st.session_state.view_type = "regional"
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (30 seconds)", value=False)
    if auto_refresh:
        log_user_action("auto_refresh_enabled")
        st.rerun()
    
    # Fetch and display data
    logger.info(f"UI_RENDER | Fetching data: feed={st.session_state.feed_type}, view={st.session_state.view_type}")
    
    with st.spinner("📡 Loading earthquake data..."):
        earthquakes = fetch_earthquake_data(st.session_state.feed_type)
    
    if earthquakes:
        st.success(f"✅ Found {len(earthquakes)} earthquakes in USA")
        logger.info(f"UI_RENDER | Displaying {len(earthquakes)} earthquakes in {st.session_state.view_type} view")
        
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
        
        logger.warning(f"UI_RENDER | No earthquake data available for {feed_desc}")
        
        st.warning(f"⚠️ No earthquake data available for {feed_desc}")
        st.info("💡 Try a different time period or data source:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🕐 Try Past Hour", key="retry_hour"):
                log_user_action("retry_data_source", "all_hour")
                st.session_state.feed_type = "all_hour"
                st.rerun()
        with col2:
            if st.button("📅 Try Past Day", key="retry_day"):
                log_user_action("retry_data_source", "all_day")
                st.session_state.feed_type = "all_day"
                st.rerun()
        with col3:
            if st.button("🌍 Try Past Week", key="retry_week"):
                log_user_action("retry_data_source", "all_week")
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
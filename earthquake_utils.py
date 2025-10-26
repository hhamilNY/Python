"""
Earthquake Utilities Module
Handles logging setup, CSS styling, configuration helpers, and common utilities
"""

import streamlit as st
import logging
import os
from datetime import datetime

def setup_logging():
    """Set up application logging"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure logging
    log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def apply_mobile_css():
    """Apply mobile-optimized CSS styling"""
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
        /* Mobile-friendly sidebar */
        .css-1d391kg {
            width: 300px;
        }
        /* Mobile responsive adjustments */
        @media (max-width: 768px) {
            .main > div {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .stButton > button {
                font-size: 14px;
                height: 2.5rem;
            }
        }
        /* Admin mode styling */
        .admin-mode {
            border: 2px solid #ff6b6b;
            border-radius: 0.5rem;
            padding: 1rem;
            background-color: #ffe6e6;
            margin: 1rem 0;
        }
        /* Status bar styling */
        .status-bar {
            background-color: #f8f9fa;
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            margin: 1rem 0;
            border-left: 3px solid #007bff;
        }
    </style>
    """, unsafe_allow_html=True)

def configure_streamlit_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="🌍 USGS Earthquake Monitor",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': 'https://earthquake.usgs.gov/',
            'Report a bug': None,
            'About': """
            # USGS Earthquake Monitor
            
            Real-time earthquake monitoring application built with Streamlit.
            
            **Features:**
            - 📱 Mobile-optimized interface
            - 🗺️ Interactive earthquake maps
            - 📊 Real-time statistics and analytics
            - 🔧 Admin dashboard for monitoring
            - 📡 Live USGS data integration
            
            **Data Source:** USGS Earthquake Hazards Program
            """
        }
    )

def show_error_page(error_message, error_details=None):
    """Show a user-friendly error page"""
    st.error("🚨 Application Error")
    
    st.markdown(f"""
    <div style="background-color: #fff3cd; border: 1px solid #ffc107; 
                border-radius: 0.5rem; padding: 1rem; margin: 1rem 0;">
        <h4 style="color: #856404; margin: 0 0 0.5rem 0;">⚠️ Something went wrong</h4>
        <p style="margin: 0; color: #856404;">{error_message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if error_details:
        with st.expander("🔍 Technical Details", expanded=False):
            st.code(error_details)
    
    st.markdown("### 🔄 What you can try:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Page", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache cleared! Please refresh.")
    
    with col3:
        if st.button("🏠 Reset to Home", use_container_width=True):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def create_mobile_footer():
    """Create mobile-friendly footer"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #555; border-top: 1px solid #eee; margin-top: 2rem;">
        <small style="color: #666;">
        📡 Data from USGS Earthquake Hazards Program<br>
        🔄 Updates every 5 minutes | 📱 Optimized for mobile devices<br>
        🔧 Admin access: Add <code>?admin=true</code> to URL or use sidebar button
        </small>
    </div>
    """, unsafe_allow_html=True)

def format_time_ago(timestamp):
    """Format timestamp to human-readable 'time ago' format"""
    if not timestamp:
        return "Unknown"
    
    try:
        dt = datetime.fromtimestamp(timestamp/1000)
        time_ago = datetime.now() - dt
        
        if time_ago.days > 0:
            return f"{time_ago.days}d ago"
        elif time_ago.seconds > 3600:
            hours = time_ago.seconds // 3600
            return f"{hours}h ago"
        elif time_ago.seconds > 60:
            minutes = time_ago.seconds // 60
            return f"{minutes}m ago"
        else:
            return "Just now"
    except:
        return "Unknown"

def get_magnitude_color_and_emoji(magnitude):
    """Get color and emoji for magnitude level"""
    if magnitude >= 5.0:
        return "#ff0000", "🔴"  # Red
    elif magnitude >= 4.0:
        return "#ff8800", "🟠"  # Orange
    elif magnitude >= 3.0:
        return "#ffdd00", "🟡"  # Yellow
    else:
        return "#88ff88", "🟢"  # Green

def validate_earthquake_data(earthquakes):
    """Validate earthquake data structure"""
    if not earthquakes:
        return False, "No earthquake data provided"
    
    required_fields = ['magnitude', 'place', 'time', 'latitude', 'longitude', 'depth']
    
    for i, eq in enumerate(earthquakes[:5]):  # Check first 5 for performance
        for field in required_fields:
            if field not in eq:
                return False, f"Missing required field '{field}' in earthquake {i+1}"
    
    return True, "Data validation passed"

def safe_get_session_state(key, default=None):
    """Safely get session state value with default"""
    try:
        return st.session_state.get(key, default)
    except:
        return default

def initialize_session_defaults():
    """Initialize session state with safe defaults"""
    defaults = {
        'feed_type': 'all_hour',
        'view_type': 'overview',
        'min_magnitude': 0.0,
        'show_admin': False,
        'session_initialized': True
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_app_version():
    """Get application version information"""
    return {
        'version': '2.0.0',
        'build_date': '2024-10-25',
        'modules': [
            'earthquake_data',
            'earthquake_viz', 
            'earthquake_admin',
            'earthquake_utils',
            'user_session_manager',
            'app_config'
        ]
    }
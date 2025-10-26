"""
Mobile Earthquake Monitor - Main Application
Simplified main app using modular architecture

A mobile-optimized web application for real-time earthquake monitoring
using USGS data with comprehensive admin features and analytics.
"""

import streamlit as st
from datetime import datetime
import logging

# Import our custom modules
from earthquake_utils import (
    setup_logging, apply_mobile_css, configure_streamlit_page,
    show_error_page, create_mobile_footer, initialize_session_defaults
)
from earthquake_data import (
    fetch_earthquake_data, filter_earthquakes_by_magnitude, 
    get_feed_descriptions, get_valid_earthquakes
)
from earthquake_viz import (
    create_mobile_header, show_quick_stats, create_mobile_map,
    show_earthquake_list, create_magnitude_chart, create_status_bar,
    show_regional_breakdown
)
from earthquake_admin import (
    check_admin_access, show_admin_dashboard, create_sidebar_controls,
    initialize_session, log_user_action, cleanup_old_data
)

# Configure logging
logger = setup_logging()

def main():
    """
    Main application function with simplified, modular structure
    """
    try:
        # Configure Streamlit
        configure_streamlit_page()
        apply_mobile_css()
        
        # Initialize session and defaults
        initialize_session_defaults()
        initialize_session()
        
        # Check for admin access
        show_admin = check_admin_access()
        
        # Create header
        create_mobile_header()
        
        # Handle sidebar based on admin status
        if show_admin:
            show_admin_dashboard()
        else:
            create_sidebar_controls()
        
        # Show status bar
        create_status_bar()
        
        # Main navigation
        render_navigation()
        
        # Fetch and display earthquake data
        render_earthquake_data()
        
        # Footer
        create_mobile_footer()
        
        # Cleanup old data periodically
        cleanup_old_data()
        
        logger.info("APP | Main function completed successfully")
        
    except Exception as e:
        logger.error(f"APP | Main function error: {e}", exc_info=True)
        show_error_page(
            "The earthquake monitoring application encountered an error.",
            str(e)
        )

def render_navigation():
    """Render the main navigation interface"""
    # Data source selection
    st.subheader("📡 Select Data Source")
    st.info("💡 **Tip:** Tap any button below to change data source or view. The highlighted button shows your current selection.")
    
    # Create navigation buttons
    col1, col2 = st.columns(2)
    current_feed = st.session_state.get('feed_type', 'all_hour')
    
    with col1:
        if st.button("🕐 Past Hour", key="hour", type="primary" if current_feed == "all_hour" else "secondary"):
            log_user_action("data_source_change", "all_hour")
            st.session_state.feed_type = "all_hour"
            st.rerun()
            
        if st.button("🌊 Significant Events", key="significant", type="primary" if current_feed == "significant_month" else "secondary"):
            log_user_action("data_source_change", "significant_month")
            st.session_state.feed_type = "significant_month"
            st.rerun()
            
        if st.button("🌍 All Week", key="week", type="primary" if current_feed == "all_week" else "secondary"):
            log_user_action("data_source_change", "all_week")
            st.session_state.feed_type = "all_week"
            st.rerun()
    
    with col2:
        if st.button("📅 Past Day", key="day", type="primary" if current_feed == "all_day" else "secondary"):
            log_user_action("data_source_change", "all_day")
            st.session_state.feed_type = "all_day"
            st.rerun()
            
        if st.button("🌋 Major Earthquakes", key="major", type="primary" if current_feed == "4.5_week" else "secondary"):
            log_user_action("data_source_change", "4.5_week")
            st.session_state.feed_type = "4.5_week"
            st.rerun()
            
        if st.button("⚠️ M2.5+ Week", key="m25week", type="primary" if current_feed == "2.5_week" else "secondary"):
            log_user_action("data_source_change", "2.5_week")
            st.session_state.feed_type = "2.5_week"
            st.rerun()
    
    # Past Month button
    col_month1, col_month2 = st.columns(2)
    with col_month1:
        if st.button("🔍 Past Month", key="month", type="primary" if current_feed == "all_month" else "secondary"):
            log_user_action("data_source_change", "all_month")
            st.session_state.feed_type = "all_month"
            st.rerun()
    
    # View type selection
    st.markdown("---")
    st.subheader("📱 Select View Type")
    st.info("📱 **Mobile Tip:** Tap any view button to see different earthquake data displays. Blue buttons show active selections.")
    
    col3, col4 = st.columns(2)
    current_view = st.session_state.get('view_type', 'overview')
    
    with col3:
        if st.button("🌍 Overview", key="overview", type="primary" if current_view == "overview" else "secondary"):
            log_user_action("view_change", "overview")
            st.session_state.view_type = "overview"
            st.rerun()
            
        if st.button("🗺️ Live Map", key="map", type="primary" if current_view == "map" else "secondary"):
            log_user_action("view_change", "map")
            st.session_state.view_type = "map"
            st.rerun()
            
        if st.button("📋 Earthquake List", key="list", type="primary" if current_view == "list" else "secondary"):
            log_user_action("view_change", "list")
            st.session_state.view_type = "list"
            st.rerun()
    
    with col4:
        if st.button("📊 Statistics", key="stats", type="primary" if current_view == "stats" else "secondary"):
            log_user_action("view_change", "stats")
            st.session_state.view_type = "stats"
            st.rerun()
            
        if st.button("🗺️ Regional View", key="regional", type="primary" if current_view == "regional" else "secondary"):
            log_user_action("view_change", "regional")
            st.session_state.view_type = "regional"
            st.rerun()
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (30 seconds)", value=False)
    if auto_refresh:
        log_user_action("auto_refresh_enabled")
        st.rerun()

def render_earthquake_data():
    """Fetch and render earthquake data based on current selections"""
    current_feed = st.session_state.get('feed_type', 'all_hour')
    current_view = st.session_state.get('view_type', 'overview')
    
    logger.info(f"UI_RENDER | Fetching data: feed={current_feed}, view={current_view}")
    
    # Fetch data with loading spinner
    with st.spinner("📡 Loading earthquake data..."):
        earthquakes = fetch_earthquake_data(current_feed)
    
    if earthquakes:
        # Apply magnitude filter from sidebar
        min_mag = st.session_state.get('min_magnitude', 0.0)
        if min_mag > 0.0:
            earthquakes = filter_earthquakes_by_magnitude(earthquakes, min_mag)
        
        # Show data quality information
        show_data_quality_info(earthquakes, min_mag)
        
        # Show quick stats
        show_quick_stats(earthquakes)
        
        # Render selected view
        render_selected_view(earthquakes, current_view)
        
    else:
        # Show no data message with retry options
        show_no_data_message(current_feed)

def show_data_quality_info(earthquakes, min_mag):
    """Show information about data quality and filtering"""
    valid_earthquakes, valid_count, invalid_count = get_valid_earthquakes(earthquakes)
    
    if invalid_count > 0:
        filter_info = f" (filtered by magnitude ≥{min_mag})" if min_mag > 0.0 else ""
        st.success(f"✅ Found {len(earthquakes)} earthquakes in USA{filter_info} ({valid_count} with valid magnitude data, {invalid_count} pending analysis)")
        st.info(f"ℹ️ **Data Quality Note:** Displaying {valid_count} earthquakes with confirmed magnitude readings. USGS sometimes reports events with incomplete magnitude data that are excluded from analysis.")
        
        # Add expandable explanation for data filtering
        with st.expander("📊 Why are some earthquakes filtered out?", expanded=False):
            st.markdown("""
            **Data Quality Standards:**
            - ✅ **Included:** Earthquakes with magnitude > 0.0 and complete location data
            - ❌ **Excluded:** Events with null, zero, or negative magnitude values
            - 🔄 **Pending:** Some recent events may lack final magnitude analysis
            
            **Why This Matters:**
            - Ensures accurate regional comparisons and statistics
            - Prevents misleading visualizations from incomplete data
            - Maintains scientific integrity of earthquake monitoring
            
            **USGS Data Pipeline:**
            1. Initial detection and location
            2. Magnitude calculation and verification  
            3. Quality review and final publication
            
            *Events typically receive final magnitude readings within minutes to hours of detection.*
            """)
    else:
        st.success(f"✅ Found {len(earthquakes)} earthquakes in USA")
        st.info(f"ℹ️ **All Events Validated:** Displaying {valid_count} earthquakes with confirmed magnitude readings")

def render_selected_view(earthquakes, view_type):
    """Render the selected view type"""
    logger.info(f"UI_RENDER | Displaying {len(earthquakes)} earthquakes in {view_type} view")
    
    if view_type == "map":
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        create_mobile_map(earthquakes)
    elif view_type == "stats":
        create_magnitude_chart(earthquakes)
    elif view_type == "list":
        show_earthquake_list(earthquakes)
    elif view_type == "regional":
        show_regional_breakdown(earthquakes)
    else:
        # Default overview - show map and list
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        create_mobile_map(earthquakes)
        show_earthquake_list(earthquakes)

def show_no_data_message(current_feed):
    """Show message when no earthquake data is available"""
    feed_descriptions = get_feed_descriptions()
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

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"APP | Application startup error: {e}", exc_info=True)
        show_error_page(
            "Failed to start the earthquake monitoring application.",
            str(e)
        )
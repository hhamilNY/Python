"""
Earthquake Admin Module
Handles admin dashboard, analytics, session management, and user tracking
"""

import streamlit as st
import json
import os
import logging
from datetime import datetime
from user_session_manager import UserSessionManager
from app_config import AppConfig

# Configure logging
logger = logging.getLogger(__name__)

# Initialize managers
session_manager = UserSessionManager()
config = AppConfig()

def create_sidebar_controls():
    """Create sidebar controls for regular users"""
    with st.sidebar:
        st.title("🎛️ Controls")
        
        # Magnitude filter
        min_mag = st.slider(
            "Minimum Magnitude",
            min_value=0.0,
            max_value=6.0,
            value=0.0,
            step=0.1,
            help="Filter earthquakes by minimum magnitude"
        )
        st.session_state.min_magnitude = min_mag
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        # Admin access
        st.markdown("---")
        st.markdown("**🔧 Admin Access**")
        if st.button("Enable Admin Mode", use_container_width=True):
            st.session_state.show_admin = True
            st.rerun()

def show_admin_dashboard():
    """Show comprehensive admin dashboard in sidebar"""
    with st.sidebar:
        st.title("🔧 Admin Dashboard")
        
        # Quick stats
        stats = get_visit_stats()
        st.metric("Total Visitors", stats["unique_visitors"])
        st.metric("Page Views", stats["page_views"])
        st.metric("Sessions Today", stats["sessions_today"])
        
        # Admin controls
        st.markdown("---")
        st.markdown("**🎛️ Admin Controls**")
        
        if st.button("📊 View Full Analytics", use_container_width=True):
            show_analytics_page()
        
        if st.button("🗂️ View Logs", use_container_width=True):
            show_logs_page()
        
        if st.button("⚙️ Configuration", use_container_width=True):
            show_config_page()
        
        if st.button("🔄 Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache cleared!")
        
        if st.button("❌ Exit Admin Mode", use_container_width=True):
            st.session_state.show_admin = False
            st.rerun()

def get_visit_stats():
    """Get visitor statistics"""
    return session_manager.get_analytics_summary()

def track_visitor():
    """Track a visitor and return visitor ID"""
    return session_manager.track_visitor()

def log_user_action(action, details=None):
    """Log user action for analytics"""
    visitor_id = st.session_state.get('visitor_id')
    session_id = st.session_state.get('session_id')
    
    if visitor_id:
        session_manager.log_action(visitor_id, action, details)
        logger.info(f"USER_ACTION | {visitor_id} | {session_id} | {action} | {details}")

def show_analytics_page():
    """Show detailed analytics in main content area"""
    st.markdown("# 📊 Analytics Dashboard")
    
    # Get comprehensive stats
    stats = session_manager.get_analytics_summary()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Unique Visitors", stats["unique_visitors"])
    with col2:
        st.metric("Total Page Views", stats["page_views"])
    with col3:
        st.metric("Sessions Today", stats["sessions_today"])
    with col4:
        st.metric("New Visitors Today", stats["new_visitors_today"])
    
    # Recent activity
    st.markdown("## 🕐 Recent Activity")
    recent_actions = session_manager.get_recent_actions(limit=20)
    
    if recent_actions:
        for action in recent_actions:
            timestamp = datetime.fromtimestamp(action['timestamp']).strftime("%H:%M:%S")
            st.markdown(f"**{timestamp}** - {action['visitor_id']} - {action['action']} - {action.get('details', '')}")
    else:
        st.info("No recent activity")
    
    # Geographic breakdown
    st.markdown("## 🌍 Geographic Distribution")
    geo_stats = session_manager.get_geographic_stats()
    
    if geo_stats:
        for location, count in geo_stats.items():
            st.markdown(f"**{location}**: {count} visitors")
    else:
        st.info("No geographic data available")

def show_logs_page():
    """Show application logs"""
    st.markdown("# 📋 Application Logs")
    
    # Show recent log entries
    try:
        log_files = [f for f in os.listdir('.') if f.startswith('app_') and f.endswith('.log')]
        
        if log_files:
            selected_log = st.selectbox("Select Log File", log_files)
            
            if selected_log:
                with open(selected_log, 'r') as f:
                    lines = f.readlines()
                
                # Show last 100 lines
                st.text_area("Log Content", value=''.join(lines[-100:]), height=400)
        else:
            st.info("No log files found")
            
    except Exception as e:
        st.error(f"Error reading logs: {e}")

def show_config_page():
    """Show configuration management"""
    st.markdown("# ⚙️ Configuration")
    
    # Current configuration
    st.markdown("## Current Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("User Data Retention", f"{config.user_data_retention_files} files")
        st.metric("Log Retention", f"{config.log_retention_files} files")
    
    with col2:
        st.metric("Session Timeout", f"{config.session_timeout_hours}h")
        st.metric("Analytics Enabled", "Yes" if config.enable_analytics else "No")
    
    # Configuration management
    st.markdown("## Update Settings")
    
    new_user_retention = st.number_input(
        "User Data Retention (files)",
        min_value=1,
        max_value=100,
        value=config.user_data_retention_files
    )
    
    new_log_retention = st.number_input(
        "Log Retention (files)",
        min_value=1,
        max_value=50,
        value=config.log_retention_files
    )
    
    if st.button("Update Configuration"):
        config.user_data_retention_files = new_user_retention
        config.log_retention_files = new_log_retention
        config.save_config()
        st.success("Configuration updated!")
        st.rerun()

def check_admin_access():
    """Check if admin access should be granted"""
    show_admin = False
    
    # First check session state
    if st.session_state.get('show_admin', False):
        show_admin = True
    
    # Also check URL parameters
    try:
        # Method 1: Try st.query_params (newer Streamlit versions)
        if hasattr(st, 'query_params'):
            query_params = st.query_params
            if query_params.get('admin') == 'true':
                show_admin = True
                st.session_state.show_admin = True
    
        # Method 2: Try st.experimental_get_query_params (older versions)
        elif hasattr(st, 'experimental_get_query_params'):
            query_params = st.experimental_get_query_params()
            if query_params.get('admin', [''])[0] == 'true':
                show_admin = True
                st.session_state.show_admin = True
    
        # Method 3: Check browser URL directly (most compatible)
        else:
            # This will work in most Streamlit environments
            import urllib.parse
            # Get URL from browser if available
            if 'admin=true' in str(st.session_state.get('_current_url', '')):
                show_admin = True
        
        if show_admin:
            st.info("🔧 **Admin Mode Activated** - Analytics dashboard is shown in the sidebar")
            
    except Exception as e:
        show_admin = False
        logger.warning(f"ADMIN_ACCESS | URL parameter check failed: {e}")
    
    return show_admin

def initialize_session():
    """Initialize session tracking"""
    if 'session_id' not in st.session_state:
        import uuid
        st.session_state.session_id = str(uuid.uuid4())[:8]
        
    if 'visitor_id' not in st.session_state:
        st.session_state.visitor_id = track_visitor()
        
    logger.info(f"SESSION_START | Session: {st.session_state.session_id} | Visitor: {st.session_state.visitor_id}")

def cleanup_old_data():
    """Clean up old session and log data"""
    try:
        session_manager.cleanup_old_files()
        logger.info("CLEANUP | Old data cleanup completed")
    except Exception as e:
        logger.error(f"CLEANUP | Error during cleanup: {e}")
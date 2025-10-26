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
from app_config import get_app_config
from user_session_manager import get_session_manager


# Configure logging with rotation
def setup_logging():
    """
    Setup rotating file logger with size and count limits.
    
    Creates a logs directory if it doesn't exist and configures a rotating
    file handler that keeps log files under 5MB and maintains up to 10 backup files.
    
    Returns:
        logging.Logger: Configured logger instance for the earthquake app
    """
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
    """
    Decorator to log function performance metrics.
    
    Wraps functions to automatically log their execution time and any errors
    that occur during execution. Useful for monitoring app performance.
    
    Args:
        func: The function to be decorated
        
    Returns:
        function: Wrapped function with performance logging
    """
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
    """
    Log user interactions for analytics and debugging.
    
    Records user actions both in the application log and persistent metrics
    storage for later analysis. Includes session tracking.
    
    Args:
        action (str): The action performed by the user (e.g., 'data_source_change')
        details (str, optional): Additional details about the action
    """
    session_id = st.session_state.get('session_id', 'unknown')
    log_msg = f"USER_ACTION | Session: {session_id} | Action: {action}"
    if details:
        log_msg += f" | Details: {details}"
    logger.info(log_msg)
    
    # Record in persistent metrics
    metrics = get_metrics()
    metrics.record_user_action(action, details)

def track_visitor():
    """
    Enhanced visitor tracking with location, device, and security monitoring.
    
    Creates comprehensive session tracking with IP geolocation, device fingerprinting,
    and security monitoring. Integrates with both the new session manager and 
    existing metrics system for backward compatibility.
    
    Returns:
        str: Unique visitor ID (12-character UUID)
    """
    session_manager = get_session_manager()
    
    # Get or create visitor ID (persists across browser sessions)
    visitor_id = st.session_state.get('visitor_id')
    if not visitor_id:
        import uuid
        visitor_id = str(uuid.uuid4())[:12]  # Longer ID for visitors
        st.session_state.visitor_id = visitor_id
    
    # Get or create enhanced session
    session_id = st.session_state.get('session_id')
    if not session_id:
        # Try to get request information for location tracking
        request_headers = {}
        user_agent = "Unknown"
        
        try:
            # Get headers from Streamlit context if available
            if hasattr(st, 'context') and hasattr(st.context, 'headers'):
                request_headers = dict(st.context.headers)
                user_agent = request_headers.get('User-Agent', 'Unknown')
            
            # Try to get client IP from various sources
            if 'X-Forwarded-For' not in request_headers:
                # Check query params for forwarded IP (some proxy setups)
                query_params = st.experimental_get_query_params()
                if 'client_ip' in query_params:
                    request_headers['X-Forwarded-For'] = query_params['client_ip'][0]
                    
        except Exception as e:
            logger.debug(f"SESSION_INFO | Could not get request headers: {e}")
        
        # Create enhanced session with location and device tracking
        try:
            session_id, session_data = session_manager.create_session(
                visitor_id=visitor_id,
                request_headers=request_headers,
                user_agent=user_agent
            )
            st.session_state.session_id = session_id
            
            # Log enhanced session info with state for US users
            location = session_data['location']
            location_str = location.get('location_string', f"{location['city']}, {location['country']}")
            logger.info(f"NEW_ENHANCED_SESSION | ID: {session_id} | Visitor: {visitor_id} | "
                       f"Location: {location_str} | "
                       f"IP: {session_data['ip_address']} | Device: {session_data['device_id']}")
            
        except Exception as e:
            # Fallback to basic session if enhanced tracking fails
            logger.warning(f"SESSION_ERROR | Enhanced session creation failed: {e}")
            session_id = str(uuid.uuid4())[:8]
            st.session_state.session_id = session_id
            logger.info(f"NEW_BASIC_SESSION | ID: {session_id} | Visitor: {visitor_id}")
    else:
        # Update existing session activity
        try:
            session_manager.update_session_activity(session_id, 'page_view')
        except Exception as e:
            logger.debug(f"SESSION_UPDATE | Failed to update session activity: {e}")
    
    # Log page view
    logger.info(f"PAGE_VIEW | Visitor: {visitor_id} | Session: {session_id}")
    
    # Record in existing metrics system (backward compatibility)
    try:
        metrics = get_metrics()
        metrics.record_new_visitor(visitor_id)
        metrics.record_page_view(visitor_id)
        metrics.record_session(session_id)
    except Exception as e:
        logger.warning(f"METRICS_ERROR | Failed to record in existing metrics: {e}")
    
    # Periodic cleanup of old data with enhanced retention policies
    import random
    app_config = get_app_config()
    retention_config = app_config.get_retention_config()
    cleanup_frequency = retention_config['cleanup_frequency_percent']
    
    if cleanup_frequency > 0 and random.randint(1, 100) <= cleanup_frequency:
        try:
            # Use different retention for different data types
            metrics_retention_days = retention_config['metrics_retention_days']
            session_retention_days = retention_config['session_retention_days']
            
            # Cleanup both systems with appropriate retention
            metrics.cleanup_old_data(days_to_keep=metrics_retention_days)
            session_manager.cleanup_old_sessions(days_to_keep=session_retention_days)
            
            logger.info(f"ENHANCED_CLEANUP | Automatic cleanup completed: {metrics_retention_days} days metrics, {session_retention_days} days sessions, {cleanup_frequency}% frequency")
        except Exception as e:
            logger.warning(f"ENHANCED_CLEANUP | Cleanup failed: {e}")
    
    return visitor_id

def get_visit_stats():
    """
    Get visitor statistics from persistent metrics with log fallback.
    
    Attempts to retrieve visitor statistics from the persistent metrics system.
    If that fails, falls back to parsing log files for basic statistics.
    
    Returns:
        dict: Dictionary containing visitor statistics including:
            - unique_visitors: Total number of unique visitors
            - page_views: Total number of page views
            - new_visitors_today: Number of new visitors today
            - total_sessions: Total number of sessions
            - days_active: Number of days with activity
            - avg_page_views_per_visitor: Average page views per visitor
    """
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
    """
    Get detailed analytics from persistent metrics with log fallback.
    
    Retrieves comprehensive analytics data including popular data sources,
    view types, user actions, and error logs. Uses persistent metrics
    as primary source with log file parsing as fallback.
    
    Returns:
        dict: Dictionary containing detailed analytics:
            - daily_visitors: Daily visitor breakdown (dict)
            - popular_data_sources: Most used data sources (dict)
            - popular_views: Most viewed sections (dict)
            - user_actions: User action frequency (dict)
            - session_count: Total number of sessions (int)
            - errors: List of recent error messages (list)
    """
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
    """
    Show admin analytics dashboard in the sidebar (hidden feature).
    
    Displays comprehensive analytics including visitor statistics, popular
    data sources, popular views, and recent errors. Only accessible via
    URL parameter '?admin=true'. Used for monitoring app usage and
    identifying issues.
    """
    st.sidebar.title("📊 Analytics Dashboard")
    st.sidebar.info("🔍 **DEBUG:** Admin sidebar should be visible now!")
    
    # Exit admin mode button
    if st.sidebar.button("❌ Exit Admin Mode", help="Return to normal view"):
        st.session_state.show_admin = False
        st.rerun()
    
    st.sidebar.markdown("---")
    
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
    
    # Add log viewer section
    with st.sidebar.expander("📋 Recent Log Entries", expanded=False):
        try:
            log_file = os.path.join("logs", "earthquake_app.log")
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Show last 20 lines
                    recent_logs = lines[-20:] if len(lines) > 20 else lines
                
                st.write("**Last 20 log entries:**")
                for line in recent_logs:
                    st.text(line.strip())
            else:
                st.write("📄 No log file found yet")
        except Exception as e:
            st.write(f"❌ Error reading logs: {e}")
    
    # Add log download button
    with st.sidebar.expander("📥 Download Logs", expanded=False):
        try:
            log_file = os.path.join("logs", "earthquake_app.log")
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                
                st.download_button(
                    label="📥 Download Full Log File",
                    data=log_content,
                    file_name=f"earthquake_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    help="Download complete log file to your computer"
                )
                
                # Show file size and entry count
                log_size = len(log_content.encode('utf-8'))
                log_lines = len(log_content.splitlines())
                st.write(f"📊 Log file: {log_lines} entries, {log_size:,} bytes")
            else:
                st.write("📄 No log file available for download")
        except Exception as e:
            st.write(f"❌ Error preparing download: {e}")
    
    # Add visitor metrics download button
    with st.sidebar.expander("📈 Download Visitor Metrics", expanded=False):
        try:
            # Get comprehensive metrics data
            metrics = get_metrics()
            
            # Collect all metrics data
            summary_stats = metrics.get_summary_stats()
            popular_items = metrics.get_popular_items()
            
            # Create comprehensive metrics report
            metrics_report = f"""EARTHQUAKE MONITOR - VISITOR METRICS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
=================================================

SUMMARY STATISTICS:
- Total Unique Visitors: {summary_stats.get('total_unique_visitors', 0)}
- Total Page Views: {summary_stats.get('total_page_views', 0)}
- Total Sessions: {summary_stats.get('total_sessions', 0)}
- New Visitors Today: {summary_stats.get('new_visitors_today', 0)}
- Days Active: {summary_stats.get('days_active', 0)}
- Average Page Views per Visitor: {summary_stats.get('avg_page_views_per_visitor', 0):.2f}

POPULAR DATA SOURCES:
"""
            # Add popular data sources
            for source, count in popular_items.get('data_sources', {}).items():
                metrics_report += f"- {source}: {count} uses\n"
            
            metrics_report += f"""
POPULAR VIEWS:
"""
            # Add popular views
            for view, count in popular_items.get('views', {}).items():
                metrics_report += f"- {view}: {count} views\n"
            
            metrics_report += f"""
USER ACTIONS:
"""
            # Add user actions
            for action, count in popular_items.get('actions', {}).items():
                metrics_report += f"- {action}: {count} times\n"
            
            metrics_report += f"""
=================================================
This report contains visitor analytics and usage patterns
for the USGS Earthquake Monitor application.
"""
            
            # Download button for metrics
            st.download_button(
                label="📈 Download Visitor Metrics Report",
                data=metrics_report,
                file_name=f"visitor_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                help="Download comprehensive visitor analytics and usage statistics"
            )
            
            # Show metrics summary
            st.write(f"📊 **Metrics Summary:**")
            st.write(f"- {summary_stats.get('total_unique_visitors', 0)} unique visitors")
            st.write(f"- {summary_stats.get('total_page_views', 0)} page views")
            st.write(f"- {len(popular_items.get('data_sources', {}))} data sources tracked")
            st.write(f"- {len(popular_items.get('views', {}))} view types tracked")
            
        except Exception as e:
            st.write(f"❌ Error preparing metrics download: {e}")
            
        # Also add raw JSON download option for advanced users
        try:
            import json
            
            # Get raw metrics data as JSON
            raw_metrics = {
                "summary_stats": metrics.get_summary_stats(),
                "popular_items": metrics.get_popular_items(),
                "export_timestamp": datetime.now().isoformat(),
                "app_name": "earthquake_monitor"
            }
            
            json_data = json.dumps(raw_metrics, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="📋 Download Raw Metrics (JSON)",
                data=json_data,
                file_name=f"metrics_raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json", 
                help="Download raw metrics data in JSON format for analysis"
            )
            
        except Exception as e:
            st.write(f"⚠️ JSON export not available: {e}")
    
    # Add data retention policy information
    with st.sidebar.expander("🗂️ Data Retention Policy", expanded=False):
        # Get app configuration
        app_config = get_app_config()
        retention_config = app_config.get_retention_config()
        
        st.write("**📊 Current Retention Settings:**")
        st.write(f"- Daily metrics: {retention_config['metrics_retention_days']} days")
        st.write(f"- Auto-cleanup frequency: {retention_config['cleanup_frequency_percent']}% chance per visit")
        st.write("- Summary stats: Permanent")
        st.write(f"- App log files: {retention_config['log_max_size_mb']}MB + {retention_config['log_backup_count']} backups")
        st.write(f"- User data: {retention_config['user_data_retention_days']} days")
        st.write(f"- User session logs: {retention_config['user_log_backup_count']} backup files")
        st.write(f"- Session data: {retention_config['session_retention_days']} days")
        st.write(f"- Security logs: {retention_config['security_log_retention_days']} days")
        
        st.write("**⚙️ Configure Retention:**")
        
        # Basic metrics settings
        st.write("**📈 Basic Analytics:**")
        col1, col2 = st.columns(2)
        with col1:
            new_metrics_retention = st.slider(
                "Days to keep daily metrics",
                min_value=7,
                max_value=365,
                value=retention_config['metrics_retention_days'],
                step=7,
                help="Number of days to keep daily visitor/page view breakdowns"
            )
        
        with col2:
            new_cleanup_frequency = st.slider(
                "Auto-cleanup frequency (%)",
                min_value=0,
                max_value=10,
                value=retention_config['cleanup_frequency_percent'],
                step=1,
                help="Percentage chance of cleanup per visitor (0 = manual only)"
            )
        
        # Application log settings
        st.write("**📋 Application Logs:**")
        col1, col2 = st.columns(2)
        with col1:
            new_log_size = st.number_input(
                "App log file size (MB)",
                min_value=1,
                max_value=50,
                value=retention_config['log_max_size_mb'],
                help="Maximum size of each application log file"
            )
        
        with col2:
            new_log_backup_count = st.number_input(
                "App log backup files",
                min_value=1,
                max_value=30,
                value=retention_config['log_backup_count'],
                help="Number of backup application log files to keep"
            )
        
        # Enhanced user data settings
        st.write("**🔐 User Data & Sessions:**")
        col1, col2 = st.columns(2)
        with col1:
            new_user_data_retention = st.number_input(
                "User data retention (days)",
                min_value=30,
                max_value=730,
                value=retention_config['user_data_retention_days'],
                help="Number of days to keep detailed user session data"
            )
            
            new_session_retention = st.number_input(
                "Session retention (days)",
                min_value=30,
                max_value=365,
                value=retention_config['session_retention_days'],
                help="Number of days to keep active session records"
            )
        
        with col2:
            new_user_log_backups = st.number_input(
                "User session log backups",
                min_value=10,
                max_value=50,
                value=retention_config['user_log_backup_count'],
                help="Number of user session log backup files to keep"
            )
            
            new_security_log_retention = st.number_input(
                "Security log retention (days)",
                min_value=90,
                max_value=1095,
                value=retention_config['security_log_retention_days'],
                help="Number of days to keep security event logs"
            )
        
        # Apply settings button
        if st.button("💾 Apply Enhanced Retention Settings", help="Save new retention policy to mobile_config.json"):
            success = app_config.update_retention_config(
                metrics_days=new_metrics_retention,
                cleanup_frequency=new_cleanup_frequency,
                log_size_mb=new_log_size,
                log_backup_count=new_log_backup_count,
                user_data_days=new_user_data_retention,
                user_log_backups=new_user_log_backups,
                session_days=new_session_retention,
                security_log_days=new_security_log_retention
            )
            
            if success:
                st.success(f"✅ Enhanced retention policy saved to mobile_config.json!")
                st.info(f"� Basic: {new_metrics_retention} days metrics, {new_cleanup_frequency}% frequency")
                st.info(f"📋 App logs: {new_log_size}MB files, {new_log_backup_count} backups")
                st.info(f"🔐 User data: {new_user_data_retention} days, {new_user_log_backups} session log backups")
                st.info(f"🛡️ Security: {new_security_log_retention} days security logs")
                logger.info(f"ADMIN_CONFIG | Enhanced retention policy updated in mobile_config.json")
            else:
                st.error("❌ Failed to save configuration")
        
        st.write("**🔧 Manual Actions:**")
        
        # Enhanced manual cleanup with different retention policies
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧹 Clean Old Metrics", help="Remove daily data older than configured days"):
                try:
                    retention_config = app_config.get_retention_config()
                    current_retention = retention_config['metrics_retention_days']
                    metrics = get_metrics()
                    metrics.cleanup_old_data(days_to_keep=current_retention)
                    st.success(f"✅ Cleaned metrics data older than {current_retention} days!")
                    logger.info(f"ADMIN_ACTION | Manual metrics cleanup: {current_retention} days")
                except Exception as e:
                    st.error(f"❌ Metrics cleanup failed: {e}")
                    logger.error(f"ADMIN_ACTION | Manual metrics cleanup failed: {e}")
            
            if st.button("🔐 Clean Old Sessions", help="Remove session data older than configured days"):
                try:
                    retention_config = app_config.get_retention_config()
                    session_retention = retention_config['session_retention_days']
                    session_manager = get_session_manager()
                    session_manager.cleanup_old_sessions(days_to_keep=session_retention)
                    st.success(f"✅ Cleaned session data older than {session_retention} days!")
                    logger.info(f"ADMIN_ACTION | Manual session cleanup: {session_retention} days")
                except Exception as e:
                    st.error(f"❌ Session cleanup failed: {e}")
                    logger.error(f"ADMIN_ACTION | Manual session cleanup failed: {e}")
        
        with col2:
            if st.button("🔄 Reset to Defaults", help="Reset all settings to default values"):
                success = app_config.reset_to_defaults()
                if success:
                    st.success("✅ Reset to enhanced defaults in mobile_config.json!")
                    logger.info("ADMIN_CONFIG | Configuration reset to enhanced defaults")
                    st.rerun()  # Refresh to show new values
                else:
                    st.error("❌ Failed to reset configuration")
            
            if st.button("🛡️ Clean Security Logs", help="Remove old security events"):
                try:
                    retention_config = app_config.get_retention_config()
                    security_retention = retention_config['security_log_retention_days']
                    session_manager = get_session_manager()
                    # This would need a new method in session manager for security cleanup
                    st.info(f"🔍 Security logs retention: {security_retention} days")
                    logger.info(f"ADMIN_ACTION | Security log retention check: {security_retention} days")
                except Exception as e:
                    st.error(f"❌ Security log check failed: {e}")
        
        # Show current storage info
        try:
            st.write("**📁 Enhanced Storage Usage:**")
            
            # Basic metrics file
            metrics_file = "metrics/visitor_metrics.json"
            if os.path.exists(metrics_file):
                metrics_size = os.path.getsize(metrics_file)
                st.write(f"- 📊 Basic metrics: {metrics_size:,} bytes")
            else:
                st.write("- 📊 Basic metrics: Not created yet")
            
            # Enhanced session data
            sessions_file = "sessions/user_sessions.json"
            if os.path.exists(sessions_file):
                sessions_size = os.path.getsize(sessions_file)
                st.write(f"- 🔐 User sessions: {sessions_size:,} bytes")
            else:
                st.write("- 🔐 User sessions: Not created yet")
            
            # Config file
            config_summary = app_config.get_config_summary()
            st.write(f"- ⚙️ Configuration: {config_summary['file_size']:,} bytes")
            
            # Check log files size
            log_dir = "logs"
            if os.path.exists(log_dir):
                total_log_size = 0
                log_files = 0
                for file in os.listdir(log_dir):
                    if file.endswith('.log'):
                        file_path = os.path.join(log_dir, file)
                        total_log_size += os.path.getsize(file_path)
                        log_files += 1
                
                if log_files > 0:
                    st.write(f"- Log files: {total_log_size:,} bytes ({log_files} files)")
                    
                    # Show warning if approaching limits
                    max_log_storage = retention_config['log_max_size_mb'] * retention_config['log_backup_count'] * 1024 * 1024
                    if total_log_size > max_log_storage * 0.8:  # 80% of limit
                        st.warning(f"⚠️ Log files approaching {max_log_storage // (1024*1024)}MB limit")
                else:
                    st.write("- Log files: No log files yet")
            else:
                st.write("- Log files: Logs directory not created")
            
            # Show config file info
            st.write(f"- Config created: {config_summary.get('created_date', 'Unknown')[:10]}")
            st.write(f"- Config updated: {config_summary.get('last_updated', 'Unknown')[:10]}")
            
        except Exception as e:
            st.write(f"⚠️ Storage info unavailable: {e}")
            
        # Configuration export/import
        st.write("**⚙️ Configuration Management:**")
        
        # Export current settings
        col1, col2 = st.columns(2)
        
        with col1:
            config_export = app_config.export_config()
            if config_export:
                st.download_button(
                    label="📋 Export Config",
                    data=config_export,
                    file_name=f"mobile_config_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    help="Download complete configuration including all settings"
                )
        
        with col2:
            # Import configuration
            uploaded_config = st.file_uploader(
                "📁 Import Config",
                type=['json'],
                help="Upload a mobile_config.json file to restore settings"
            )
            
            if uploaded_config is not None:
                try:
                    config_content = uploaded_config.read().decode('utf-8')
                    success = app_config.import_config(config_content)
                    
                    if success:
                        st.success("✅ Configuration imported successfully!")
                        logger.info("ADMIN_CONFIG | Configuration imported from file")
                        st.rerun()  # Refresh to show new values
                    else:
                        st.error("❌ Failed to import configuration")
                        
                except Exception as e:
                    st.error(f"❌ Import error: {e}")
                    logger.error(f"ADMIN_CONFIG | Config import failed: {e}")
        
        # Show configuration file location
        st.write("**📄 Configuration File:**")
        st.code(f"Location: {app_config.config_file}")
        st.write("This file persists all your retention and app settings.")
    
    # Add Enhanced Session Analytics section
    with st.sidebar.expander("🌍 Enhanced Session Analytics", expanded=False):
        try:
            session_manager = get_session_manager()
            analytics = session_manager.get_analytics_summary()
            security = session_manager.get_security_summary()
            
            st.write("**📊 Session Overview:**")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Sessions", analytics['total_sessions'])
                st.metric("Active Sessions", analytics['active_sessions'])
                st.metric("Avg Duration", f"{analytics['average_session_duration_minutes']:.1f}m")
            
            with col2:
                st.metric("Unique Locations", analytics['unique_locations'])
                st.metric("Unique Devices", analytics['unique_devices'])
                st.metric("Security Events", analytics['security_events'])
            
            # US States tracking if available
            if 'us_states_visited' in analytics and analytics['us_states_visited'] > 0:
                st.write("**🇺🇸 US States Analytics:**")
                st.info(f"📍 Accessed from {analytics['us_states_visited']} US states")
                
                # Show list of states
                if 'us_states_list' in analytics and analytics['us_states_list']:
                    states_text = ", ".join(sorted(analytics['us_states_list']))
                    st.write(f"**States visited:** {states_text}")
            
            # Security status
            if security['recent_events_30_days'] > 0:
                st.warning(f"⚠️ {security['recent_events_30_days']} security events in last 30 days")
            else:
                st.success("✅ No recent security events")
            
            # Geographic insights
            st.write("**🗺️ Geographic Insights:**")
            if analytics['unique_locations'] > 0:
                st.info(f"📍 App accessed from {analytics['unique_locations']} different locations")
            
            if analytics['unique_devices'] > 0:
                st.info(f"📱 {analytics['unique_devices']} unique devices/browsers detected")
            
            # Session data export
            st.write("**📥 Enhanced Data Export:**")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Export Session Data", help="Download comprehensive session analytics"):
                    try:
                        export_file = session_manager.export_session_data()
                        if export_file:
                            with open(export_file, 'r', encoding='utf-8') as f:
                                session_data = f.read()
                            
                            st.download_button(
                                label="📥 Download Session Export",
                                data=session_data,
                                file_name=f"session_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json",
                                help="Complete session data with locations, devices, and security events"
                            )
                            st.success("✅ Session data prepared for download!")
                        else:
                            st.error("❌ Failed to export session data")
                    except Exception as e:
                        st.error(f"❌ Export error: {e}")
            
            with col2:
                if st.button("🧹 Cleanup Sessions", help="Remove old session data"):
                    try:
                        app_config = get_app_config()
                        retention_config = app_config.get_retention_config()
                        retention_days = retention_config['session_retention_days']
                        session_manager.cleanup_old_sessions(days_to_keep=retention_days)
                        st.success(f"✅ Cleaned sessions older than {retention_days} days!")
                        logger.info(f"ADMIN_ACTION | Manual session cleanup: {retention_days} days")
                    except Exception as e:
                        st.error(f"❌ Session cleanup failed: {e}")
            
            # Recent security events
            if security['recent_events']:
                st.write("**🔒 Recent Security Events:**")
                for event in security['recent_events'][-3:]:  # Show last 3
                    event_time = event['timestamp'][:16].replace('T', ' ')
                    st.write(f"🔴 {event_time}: {event['event_type']} ({event['severity']})")
            
        except Exception as e:
            st.write(f"⚠️ Enhanced analytics unavailable: {e}")
            st.write("💡 Session manager may not be properly initialized")


# Configure Streamlit page
st.set_page_config(
    page_title="🌍 USGS Earthquake Monitor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"  # Changed to expanded so admin features are visible
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
    """
    Fetch earthquake data from USGS API with caching and comprehensive logging.
    
    Retrieves earthquake data from the USGS GeoJSON feed, filters for USA region
    earthquakes, and performs data quality analysis. Includes detailed logging
    of the filtering process and magnitude validation.
    
    Args:
        feed_type (str): Type of earthquake feed to fetch. Options include:
            - "all_hour": All earthquakes in the past hour
            - "all_day": All earthquakes in the past day
            - "all_week": All earthquakes in the past week
            - "all_month": All earthquakes in the past month
            - "significant_month": Significant earthquakes in the past month
            - "4.5_week": Magnitude 4.5+ earthquakes in the past week
            - "2.5_week": Magnitude 2.5+ earthquakes in the past week
    
    Returns:
        list: List of earthquake dictionaries with keys:
            - magnitude: Earthquake magnitude (float)
            - place: Location description (str)
            - time: Unix timestamp in milliseconds (int)
            - depth: Depth in kilometers (float)
            - longitude: Longitude coordinate (float)
            - latitude: Latitude coordinate (float)
            - alert: Alert level if any (str or None)
            - tsunami: Tsunami warning flag (int)
            - url: USGS details URL (str)
    """
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
        
        # Detailed magnitude analysis
        valid_magnitudes = sum(1 for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0)
        null_magnitudes = sum(1 for eq in earthquakes if eq['magnitude'] is None)
        zero_magnitudes = sum(1 for eq in earthquakes if eq['magnitude'] == 0)
        negative_magnitudes = sum(1 for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] < 0)
        
        logger.info(f"DATA_FETCH | Magnitude breakdown: {valid_magnitudes} valid, {null_magnitudes} null, {zero_magnitudes} zero, {negative_magnitudes} negative")
        logger.info(f"DATA_FETCH | Total USA earthquakes: {usa_count} → Valid for display: {valid_magnitudes}")
        
        if valid_magnitudes != usa_count:
            filtered_count = usa_count - valid_magnitudes
            logger.warning(f"DATA_FETCH | {filtered_count} earthquakes filtered out due to invalid magnitude data")
        
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
    """
    Create mobile-friendly header for the earthquake monitoring app.
    
    Displays the main title and subtitle in a centered, mobile-optimized
    format using custom HTML styling.
    """
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1>🌍 USGS Earthquake Monitor</h1>
        <p style="color: #666; margin: 0;">Real-time earthquake monitoring for mobile devices</p>
    </div>
    """, unsafe_allow_html=True)


def create_status_bar():
    """
    Create status bar showing active data source and view type.
    
    Displays the currently selected earthquake data feed and view mode
    in a prominent status bar. Helps users understand what data they're
    viewing and provides visual feedback for their selections.
    """
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
    """
    Show quick statistics in mobile-friendly metric cards.
    
    Displays key earthquake statistics in a 2x2 grid layout optimized for
    mobile devices. Shows total count, maximum magnitude, average magnitude,
    and time since latest activity.
    
    Args:
        earthquakes (list): List of earthquake dictionaries from fetch_earthquake_data()
    """
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
    """
    Create mobile-optimized earthquake map using Plotly.
    
    Generates an interactive map showing earthquake locations with magnitude-based
    sizing and color coding. Optimized for mobile viewing with appropriate
    height and responsive design.
    
    Args:
        earthquakes (list): List of earthquake dictionaries with location and magnitude data
    """
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
    """
    Show earthquake list in mobile-friendly cards format.
    
    Displays earthquakes as individual cards sorted by magnitude (highest first).
    Each card shows magnitude, location, time, depth, and uses color coding
    based on magnitude level. Limited to top 10 earthquakes for mobile performance.
    
    Args:
        earthquakes (list): List of earthquake dictionaries to display
    """
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
                    <strong style="color: #222;">{emoji} M {eq['magnitude']:.1f}</strong><br>
                    <span style="color: #444;">{eq['place']}</span><br>
                    <small style="color: #666;">⏰ {time_str} | 📍 {eq['depth']:.1f}km deep</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def create_magnitude_chart(earthquakes):
    """
    Create mobile-friendly magnitude distribution histogram.
    
    Generates a histogram showing the distribution of earthquake magnitudes
    using Plotly. Helps users understand the frequency distribution of
    different magnitude levels in the current dataset.
    
    Args:
        earthquakes (list): List of earthquake dictionaries with magnitude data
    """
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
    """
    Show comprehensive earthquake breakdown by US regions and states.
    
    Analyzes earthquake distribution across 8 major US seismic regions including
    California, Alaska, Hawaii, Pacific Northwest, Nevada/Utah, Eastern US,
    Central US, and Yellowstone. Displays regional statistics, activity levels,
    quiet regions, detailed listings for most active regions, and a comprehensive
    histogram showing activity distribution across all regions.
    
    Features:
    - Regional activity cards with color-coded alerts
    - Quiet regions notification with time-period awareness
    - Detailed earthquake listings for most active region
    - Interactive histogram with color-coded activity levels
    - Educational guide for chart interpretation
    
    Args:
        earthquakes (list): List of earthquake dictionaries with coordinates and magnitude data
    """
    if not earthquakes:
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
    if not valid_earthquakes:
        return
    
    # Add proper spacing
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("🏛️ Regional Breakdown")
    
    # Add data quality notice for regional analysis
    st.info("📍 **Regional Analysis:** Only showing earthquakes with confirmed magnitude readings (M > 0.0) for accurate regional comparisons")
    
    # Add regional activity hint
    if st.session_state.get('feed_type', 'all_hour') in ['all_hour', 'all_day']:
        st.markdown("""
        💡 **Tip:** Alaska earthquakes are common but may not appear in short time periods. 
        Try "**All Week**" or "**Past Month**" data sources to see more regional activity.
        """)
    
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
        # Add Most Active Region Banner
        sorted_regions = sorted(regional_counts.items(), key=lambda x: x[1], reverse=True)
        most_active_region, most_active_count = sorted_regions[0]
        
        # Create prominent banner for most active region
        if most_active_count >= 10:
            banner_color = "#dc3545"  # Red
            banner_bg = "#f8d7da"
            alert_emoji = "🚨"
            alert_level = "HIGH ACTIVITY ALERT"
        elif most_active_count >= 5:
            banner_color = "#fd7e14"  # Orange
            banner_bg = "#fff3cd"
            alert_emoji = "⚠️"
            alert_level = "MODERATE ACTIVITY"
        else:
            banner_color = "#28a745"  # Green
            banner_bg = "#d4edda"
            alert_emoji = "📊"
            alert_level = "CURRENT ACTIVITY"
        
        # Remove emoji from region name for banner
        clean_region_name = most_active_region.split(' ', 1)[1] if ' ' in most_active_region else most_active_region
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {banner_bg} 0%, {banner_bg}dd 100%); 
                    border: 2px solid {banner_color}; border-radius: 1rem; 
                    padding: 1.5rem; margin: 1.5rem 0; text-align: center;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15);">
            <div style="display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 0.5rem;">
                <span style="font-size: 2em;">{alert_emoji}</span>
                <div style="flex-grow: 1; min-width: 200px;">
                    <h3 style="margin: 0; color: {banner_color}; font-weight: bold;">
                        {alert_level}
                    </h3>
                    <h2 style="margin: 0.5rem 0 0 0; color: #222; font-size: 1.8em;">
                        {clean_region_name} - Most Active Region
                    </h2>
                    <p style="margin: 0.5rem 0 0 0; color: #555; font-size: 1.1em;">
                        <strong>{most_active_count} earthquake{'s' if most_active_count != 1 else ''}</strong> detected in current time period
                    </p>
                    <p style="margin: 0.3rem 0 0 0; color: #777; font-size: 0.9em;">
                        Showing top 5 highest magnitude earthquakes from most active regions
                    </p>
                </div>
                <span style="font-size: 2em;">{alert_emoji}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Alaska-specific status check (fix key lookup with emoji)
        alaska_key = "❄️ Alaska"
        alaska_count = regional_counts.get(alaska_key, 0)
        if alaska_count > 0:
            st.success(f"🏔️ **Alaska Alert:** {alaska_count} earthquake{'s' if alaska_count != 1 else ''} detected in current time period!")
        else:
            # Check if Alaska is just quiet this period
            current_feed = st.session_state.get('feed_type', 'all_hour')
            if current_feed in ['all_hour', 'all_day']:
                st.info("🏔️ **Alaska Status:** No activity in current period. Try **All Week** or **Past Month** for Alaska earthquakes.")
                # Add quick access buttons for Alaska
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🌍 Try All Week", key="alaska_week"):
                        st.session_state.feed_type = "all_week"
                        st.rerun()
                with col2:
                    if st.button("🔍 Try Past Month", key="alaska_month"):
                        st.session_state.feed_type = "all_month"
                        st.rerun()
            else:
                st.warning("🏔️ **Alaska Status:** No earthquakes detected in selected time period.")
        
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
                    <h4 style="margin: 0 0 0.5rem 0; color: #222;">{region}</h4>
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <strong style="color: #333;">{count} earthquakes</strong><br>
                            <small style="color: #555;">Max: M{max_mag:.1f} | Avg: M{avg_mag:.1f}</small>
                        </div>
                        <div style="text-align: right; font-size: 2em;">
                            {'🔴' if count >= 10 else '🟡' if count >= 5 else '🟢'}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Show regions with no activity
        all_regions = list(regions.keys())
        active_regions = list(regional_counts.keys())
        inactive_regions = [region for region in all_regions if region not in active_regions]
        
        if inactive_regions:
            st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
            st.subheader("😴 Quiet Regions")
            
            # Get current time period for the message
            current_feed = st.session_state.get('feed_type', 'all_hour')
            feed_descriptions = {
                "all_hour": "past hour",
                "all_day": "past day", 
                "all_week": "past week",
                "all_month": "past month",
                "significant_month": "significant events (past month)",
                "4.5_week": "magnitude 4.5+ (past week)",
                "2.5_week": "magnitude 2.5+ (past week)"
            }
            time_period = feed_descriptions.get(current_feed, "selected time period")
            
            st.info(f"✨ The following regions had no earthquake activity during the {time_period}:")
            
            # Display inactive regions in a more compact format
            inactive_col1, inactive_col2 = st.columns(2)
            for i, region in enumerate(inactive_regions):
                with inactive_col1 if i % 2 == 0 else inactive_col2:
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 0.8rem; border-radius: 0.5rem; 
                                border-left: 3px solid #28a745; margin: 0.3rem 0; 
                                box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <span style="color: #222;"><strong>{region}</strong></span>
                            <span style="color: #28a745; font-size: 1.2em;">😌</span>
                        </div>
                        <small style="color: #666;">No activity detected</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Show detailed earthquake list with smart regional priority
        if sorted_regions:
            # Priority order: Alaska first (if active), then most active region, then other significant regions
            regions_to_show = []
            alaska_key = "❄️ Alaska"
            
            # Always prioritize Alaska if it has activity
            if alaska_key in regional_counts and regional_counts[alaska_key] > 0:
                regions_to_show.append((alaska_key, regional_counts[alaska_key], "Alaska Priority"))
            
            # Add the most active region if it's different from Alaska
            most_active_region, most_active_count = sorted_regions[0]
            if most_active_region != alaska_key and most_active_count > 0:
                regions_to_show.append((most_active_region, most_active_count, "Most Active"))
            
            # Add any other regions with significant activity (5+ earthquakes) up to 5 total regions
            for region, count in sorted_regions:
                if (region not in [r[0] for r in regions_to_show] and 
                    count >= 5 and 
                    len(regions_to_show) < 5):
                    regions_to_show.append((region, count, "High Activity"))
            
            # Display detailed activity for selected regions
            for i, (region_name, region_count, priority_reason) in enumerate(regions_to_show):
                st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
                
                # Special header styling for different priority types
                if priority_reason == "Alaska Priority":
                    st.subheader(f"🏔️ {region_name} - Top 5 Highest Magnitude Earthquakes")
                elif priority_reason == "Most Active":
                    st.subheader(f"📋 {region_name} - Top 5 Highest Magnitude Earthquakes") 
                else:
                    st.subheader(f"⚡ {region_name} - Top 3 Highest Magnitude Earthquakes")
                
                region_quakes = regional_earthquakes[region_name]
                region_quakes.sort(key=lambda x: x['magnitude'], reverse=True)
                
                # Show different numbers based on priority
                max_quakes = 5 if i == 0 else 3  # Show more for first priority region
                
                for eq in region_quakes[:max_quakes]:
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
                        <strong style="color: #222;">{emoji} M {eq['magnitude']:.1f}</strong> - <span style="color: #444;">{eq['place']}</span><br>
                        <small style="color: #666;">⏰ {time_str} | 📍 {eq['depth']:.1f}km deep</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Add summary if there are more earthquakes than shown
                if len(region_quakes) > max_quakes:
                    remaining = len(region_quakes) - max_quakes
                    st.markdown(f"<small style='color: #666;'>... and {remaining} more earthquake{'s' if remaining != 1 else ''} in {region_name} (showing highest magnitude earthquakes first)</small>", unsafe_allow_html=True)
        
        # Show regional activity histogram
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.subheader("📊 Regional Activity Histogram")
        
        # Add data explanation before histogram
        current_feed = st.session_state.get('feed_type', 'all_hour')
        feed_descriptions = {
            "all_hour": "past hour",
            "all_day": "past day", 
            "all_week": "past week",
            "all_month": "past month",
            "significant_month": "significant events (past month)",
            "4.5_week": "magnitude 4.5+ (past week)",
            "2.5_week": "magnitude 2.5+ (past week)"
        }
        time_period = feed_descriptions.get(current_feed, "selected time period")
        
        st.info(f"📊 **Magnitude Filter Applied:** Chart shows only earthquakes with magnitude > 0.0 during the {time_period}")
        
        # Prepare data for histogram including regions with zero activity
        all_region_names = []
        all_earthquake_counts = []
        colors = []
        
        for region_name in regions.keys():
            # Remove emojis from region names for cleaner chart
            clean_name = region_name.split(' ', 1)[1] if ' ' in region_name else region_name
            all_region_names.append(clean_name)
            
            count = regional_counts.get(region_name, 0)
            all_earthquake_counts.append(count)
            
            # Color coding based on activity level
            if count >= 10:
                colors.append('#f44336')  # Red
            elif count >= 5:
                colors.append('#ff9800')  # Orange
            elif count >= 1:
                colors.append('#4caf50')  # Green
            else:
                colors.append('#e0e0e0')  # Gray for no activity
        
        # Create histogram
        fig = px.bar(
            x=all_region_names,
            y=all_earthquake_counts,
            title="🌎 Regional Earthquake Activity Distribution",
            labels={'x': 'Region', 'y': 'Number of Earthquakes'},
            height=400,
            color=all_earthquake_counts,
            color_continuous_scale=[(0, '#e0e0e0'), (0.1, '#4caf50'), (0.5, '#ff9800'), (1, '#f44336')]
        )
        
        # Customize the chart
        fig.update_layout(
            margin=dict(l=0, r=0, t=40, b=0),
            font=dict(size=12),
            title_font_size=16,
            xaxis_tickangle=-45,
            showlegend=False,
            xaxis_title="US Regions",
            yaxis_title="Earthquake Count"
        )
        
        # Add value labels on bars
        fig.update_traces(
            texttemplate='%{y}',
            textposition='outside',
            textfont_size=11
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add interpretation helper
        current_feed = st.session_state.get('feed_type', 'all_hour')
        feed_descriptions = {
            "all_hour": "past hour",
            "all_day": "past day", 
            "all_week": "past week",
            "all_month": "past month",
            "significant_month": "significant events (past month)",
            "4.5_week": "magnitude 4.5+ (past week)",
            "2.5_week": "magnitude 2.5+ (past week)"
        }
        time_period = feed_descriptions.get(current_feed, "selected time period")
        
        with st.expander("📖 How to Read This Chart", expanded=False):
            st.markdown(f"""
            **Chart Colors:**
            - 🔴 **Red bars (10+ earthquakes)**: High activity regions during the {time_period}
            - 🟠 **Orange bars (5-9 earthquakes)**: Moderate activity regions
            - 🟢 **Green bars (1-4 earthquakes)**: Low activity regions  
            - ⚫ **Gray bars (0 earthquakes)**: Quiet regions with no detected activity
            
            **Data Quality Standards:**
            - ✅ **Only validated earthquakes shown** (magnitude > 0.0)
            - ❌ **Excludes incomplete data** (null, zero, or negative magnitudes)
            - 🔬 **Scientific accuracy prioritized** over raw event counts
            
            **What This Shows:**
            - Total confirmed earthquake count per region during the {time_period}
            - Relative seismic activity levels across the United States
            - Which regions are most/least seismically active right now
            
            **Why Some Events Are Filtered:**
            - USGS initially reports events before magnitude calculation is complete
            - Quality control ensures accurate regional comparisons
            - Prevents misleading statistics from preliminary data
            """)
    
    
    else:
        st.info("🌍 No confirmed earthquakes detected in major US regions during this time period")
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; 
                    border-left: 3px solid #17a2b8; margin: 1rem 0;">
            <h5 style="color: #17a2b8; margin: 0 0 0.5rem 0;">📊 Data Quality Note</h5>
            <p style="margin: 0; color: #333;">
                This analysis only includes earthquakes with confirmed magnitude readings (M > 0.0). 
                Some recently detected events may be excluded while USGS completes magnitude analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)


def create_regional_chart(earthquakes):
    """
    Create regional activity bar chart for earthquake distribution.
    
    Generates a bar chart showing earthquake counts by US region using Plotly.
    Only displays regions with earthquake activity. Used as an alternative
    visualization to the comprehensive regional breakdown.
    
    Args:
        earthquakes (list): List of earthquake dictionaries with coordinate data
    """
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


def create_sidebar_controls():
    """Create sidebar controls for earthquake monitoring settings"""
    
    # Earthquake Settings Section
    st.sidebar.title("🌍 Earthquake Settings")
    
    # Feed Type Selection
    st.sidebar.subheader("📡 Data Feed")
    current_feed = st.session_state.get('feed_type', 'all_hour')
    
    feed_options = {
        "all_hour": "🕐 Past Hour (All)",
        "all_day": "📅 Past Day (All)", 
        "all_week": "🌍 Past Week (All)",
        "significant_month": "🌊 Significant (Month)",
        "4.5_week": "🌋 Major (M4.5+ Week)"
    }
    
    selected_feed = st.sidebar.selectbox(
        "Choose data source:",
        options=list(feed_options.keys()),
        format_func=lambda x: feed_options[x],
        index=list(feed_options.keys()).index(current_feed)
    )
    
    if selected_feed != current_feed:
        st.session_state.feed_type = selected_feed
        log_user_action("data_source_change", selected_feed)
        st.rerun()
    
    # View Type Selection
    st.sidebar.subheader("📊 Display Options")
    current_view = st.session_state.get('view_type', 'overview')
    
    view_options = {
        "overview": "📋 Overview",
        "map": "🗺️ Interactive Map",
        "charts": "📈 Charts & Analytics",
        "list": "📝 Detailed List"
    }
    
    selected_view = st.sidebar.selectbox(
        "Choose view type:",
        options=list(view_options.keys()),
        format_func=lambda x: view_options[x],
        index=list(view_options.keys()).index(current_view)
    )
    
    if selected_view != current_view:
        st.session_state.view_type = selected_view
        log_user_action("view_change", selected_view)
        st.rerun()
    
    # Magnitude Filter
    st.sidebar.subheader("📏 Filters")
    min_magnitude = st.sidebar.slider(
        "Minimum Magnitude:",
        min_value=0.0,
        max_value=7.0,
        value=st.session_state.get('min_magnitude', 0.0),
        step=0.1,
        help="Filter earthquakes by minimum magnitude"
    )
    
    if min_magnitude != st.session_state.get('min_magnitude', 0.0):
        st.session_state.min_magnitude = min_magnitude
        log_user_action("filter_change", f"magnitude_{min_magnitude}")
    
    # Quick Admin Access
    st.sidebar.markdown("---")
    if st.sidebar.button("🔧 Admin Dashboard", help="Access admin features"):
        # Trigger admin mode by setting session state
        st.session_state.show_admin = True
        st.rerun()


def main():
    """
    Main mobile web app function and entry point.
    
    Orchestrates the entire earthquake monitoring web application including:
    - Visitor tracking and session management
    - Admin dashboard access control
    - Mobile-friendly navigation interface
    - Data source selection buttons
    - View type selection buttons
    - Data fetching and display coordination
    - Error handling and user feedback
    - Auto-refresh functionality
    
    The app supports multiple earthquake data feeds from USGS and various
    view modes including overview, map, list, statistics, and regional analysis.
    All interactions are logged for analytics and debugging purposes.
    """
    
    try:
        # Debug: Show that the app is starting
        st.write("🔍 **DEBUG:** App is starting...")
        st.write("🔍 **DEBUG:** Imports successful")
        
        # Check for admin dashboard access via URL parameter and session state
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
        
        # Debug: Show admin status for testing
        if show_admin:
            st.info("🔧 **Admin Mode Activated** - Analytics dashboard is shown in the sidebar")
            st.warning("👀 **LOOK LEFT:** The sidebar should contain admin controls. If you don't see it, try:")
            st.write("- **Desktop:** Look for a panel on the left side of your browser")
            st.write("- **Mobile:** Look for a hamburger menu (≡) or sidebar toggle")
            st.write("- **Browser:** Try refreshing the page or using a different browser")
            
    except Exception as e:
        show_admin = False
        logger.warning(f"ADMIN_ACCESS | URL parameter check failed: {e}")
    
    st.write("🔍 **DEBUG:** About to track visitor...")
    
    # Track visitor (must be called early)
    visitor_id = track_visitor()
    
    st.write(f"🔍 **DEBUG:** Visitor tracked: {visitor_id}")
    
    # Initialize session tracking
    if 'session_id' not in st.session_state:
        import uuid
        st.session_state.session_id = str(uuid.uuid4())[:8]
        logger.info(f"SESSION_START | New session: {st.session_state.session_id} | Visitor: {visitor_id}")
    
    st.write("🔍 **DEBUG:** About to handle admin/sidebar...")
    
    # Simple sidebar test that should always be visible
    st.sidebar.title("🧪 SIDEBAR TEST")
    st.sidebar.error("🚨 If you see this, the sidebar is working!")
    st.sidebar.success("✅ This message should be in the left sidebar panel")
    
    # Show admin dashboard if requested
    if show_admin:
        st.write("🔍 **DEBUG:** Admin mode detected, calling show_admin_dashboard()")
        show_admin_dashboard()
        st.write("🔍 **DEBUG:** show_admin_dashboard() completed")
    else:
        st.write("🔍 **DEBUG:** Regular mode, calling create_sidebar_controls()")
        # Create regular sidebar when not in admin mode
        create_sidebar_controls()
        st.write("🔍 **DEBUG:** create_sidebar_controls() completed")

    st.write("🔍 **DEBUG:** About to create mobile header...")
    
    create_mobile_header()    # Initialize session state first
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
    
    # Add user instruction for mobile interaction
    st.info("💡 **Tip:** Tap any button below to change data source or view. The highlighted button shows your current selection.")
    
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
    
    # Add user instruction for view selection
    st.info("📱 **Mobile Tip:** Tap any view button to see different earthquake data displays. Blue buttons show active selections.")
    
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
        # Apply magnitude filter from sidebar
        min_mag = st.session_state.get('min_magnitude', 0.0)
        if min_mag > 0.0:
            earthquakes = [eq for eq in earthquakes if eq.get('magnitude', 0) >= min_mag]
            logger.info(f"FILTER | Applied magnitude filter ≥{min_mag}: {len(earthquakes)} earthquakes remaining")
        
        valid_count = sum(1 for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0)
        invalid_count = len(earthquakes) - valid_count
        
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
        
        logger.info(f"UI_RENDER | Displaying {len(earthquakes)} earthquakes ({valid_count} valid) in {st.session_state.view_type} view")
        
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
    
    # Mobile-friendly footer with admin access info
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #555; border-top: 1px solid #eee; margin-top: 2rem;">
        <small style="color: #666;">
        📡 Data from USGS Earthquake Hazards Program<br>
        🔄 Updates every 5 minutes | 📱 Optimized for mobile devices<br>
        🔧 Admin access: Add <code>?admin=true</code> to URL or use sidebar button
        </small>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("🔍 **DEBUG:** App completed successfully!")
    
    except Exception as e:
        st.error(f"🚨 **Main Function Error:** {str(e)}")
        st.write("**Error Details:**")
        st.code(str(e))
        import traceback
        st.write("**Traceback:**")
        st.code(traceback.format_exc())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"🚨 **Application Error:** {str(e)}")
        st.write("**Error Details:**")
        st.code(str(e))
        import traceback
        st.write("**Traceback:**")
        st.code(traceback.format_exc())
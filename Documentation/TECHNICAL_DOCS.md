# 🌍 USGS Earthquake Monitor - Technical Documentation

## 🏗️ System Architecture

### Application Structure
```
mobile_earthquake_app.py     # Main Streamlit application
├── app_config.py           # Configuration management
├── user_session_manager.py # Enhanced session tracking
├── visitor_metrics.py      # Basic analytics
└── mobile_config.json     # Persistent settings
```

### Data Flow
```
User Request → Session Manager → USGS API → Data Processing → Visualization → User Response
     ↓              ↓              ↓             ↓              ↓
Analytics → Configuration → Caching → Cleanup → Monitoring
```

## 🔧 Core Components

### 1. Session Management (`user_session_manager.py`)
**Purpose**: Enhanced visitor tracking with location intelligence

**Key Features**:
- IP-based geolocation with US state tracking
- Device fingerprinting for unique identification
- Security event monitoring
- Thread-safe operations with file locking

**Methods**:
```python
track_visitor(request_info) → visitor_id
get_analytics_summary() → analytics_data
cleanup_old_sessions(days_to_keep) → cleanup_result
log_security_event(event_type, details) → log_entry
```

**Data Structure**:
```json
{
  "visitor_id": "unique_identifier",
  "ip_address": "xxx.xxx.xxx.xxx",
  "location": {
    "country": "United States",
    "region": "New York",
    "city": "New York",
    "us_state": "NY"
  },
  "device_info": {
    "user_agent": "browser_string",
    "screen_resolution": "1920x1080",
    "language": "en-US"
  },
  "session_data": {
    "first_visit": "2025-10-25T10:30:00Z",
    "last_visit": "2025-10-25T11:45:00Z",
    "visit_count": 5,
    "pages_viewed": 12
  }
}
```

### 2. Configuration Management (`app_config.py`)
**Purpose**: Thread-safe configuration with persistent storage

**Key Features**:
- JSON-based configuration with defaults
- Thread-safe operations with locking
- Automatic config merging and validation
- Enhanced retention policies

**Configuration Structure**:
```json
{
  "retention_policy": {
    "metrics_retention_days": 90,
    "cleanup_frequency_percent": 1,
    "log_max_size_mb": 5,
    "log_backup_count": 10,
    "user_data_retention_days": 180,
    "user_log_backup_count": 20,
    "session_retention_days": 120,
    "security_log_retention_days": 365
  },
  "app_settings": {
    "default_feed_type": "all_hour",
    "default_view_type": "overview",
    "cache_ttl_seconds": 300,
    "admin_mode_enabled": true
  }
}
```

### 3. Main Application (`mobile_earthquake_app.py`)
**Purpose**: Streamlit web application with earthquake monitoring

**Key Sections**:
- **Data Fetching**: USGS API integration with caching
- **Visualization**: Interactive maps and charts
- **User Interface**: Mobile-responsive design
- **Admin Panel**: Comprehensive management interface

## 📊 Data Management

### USGS API Integration
**Endpoints Used**:
```python
# Real-time earthquake feeds
all_hour = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
significant_month = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson"
```

**Response Caching**:
- **TTL**: 5 minutes for API responses
- **Storage**: In-memory with Streamlit cache
- **Fallback**: Graceful degradation on API failure

### Session Storage
**Files Created**:
```
sessions/
├── session_YYYYMMDD_HHMMSS.json    # Daily session logs
├── visitor_analytics.json          # Aggregated analytics
└── security_events.json           # Security monitoring
```

**Retention Policy**:
- **User Sessions**: 20 files (configurable)
- **Application Logs**: 10 files (configurable)
- **Security Events**: 365 days retention
- **Automatic Cleanup**: 1% frequency (configurable)

## 🎨 User Interface

### Responsive Design
**Mobile-First Approach**:
```css
/* Key responsive features */
- Collapsible sidebar for mobile
- Touch-friendly controls
- Adaptive chart sizing
- Progressive loading indicators
```

**Sidebar Structure**:
```
🌍 Earthquake Settings
├── Feed Type Selection
├── Magnitude Filters
└── Location Filters

📊 Admin Dashboard
├── Visitor Metrics
├── Download Functions
└── Real-time Analytics

⚙️ Configuration
├── Retention Policies
├── Cleanup Settings
└── Privacy Controls
```

### Admin Interface
**Features Available**:
- Real-time visitor metrics display
- Downloadable analytics reports
- Manual cleanup operations
- Configuration management
- Security event monitoring

## 🔐 Security Features

### Data Protection
**Privacy Controls**:
```python
# IP address handling
hash_ip_addresses: bool = False  # GDPR compliance
ip_logging_enabled: bool = True   # Privacy setting

# Session security
device_fingerprinting_enabled: bool = True
security_monitoring_enabled: bool = True
```

**Security Events Logged**:
- Multiple requests from same IP
- Unusual access patterns
- Configuration changes
- Data export operations

### Access Control
**Admin Features**:
- Configuration modification
- Data export capabilities
- Cleanup operations
- Analytics access

## 📈 Performance Optimization

### Caching Strategy
**Multiple Cache Layers**:
```python
@st.cache_data(ttl=300)  # 5-minute cache
def fetch_earthquake_data(feed_url):
    # USGS API calls cached

@st.cache_resource
def get_session_manager():
    # Singleton pattern for session manager
```

### Resource Management
**Memory Optimization**:
- Lazy loading of session data
- Automatic cleanup of old files
- Efficient data structures
- Background processing for cleanup

### Performance Monitoring
**Built-in Metrics**:
```python
# Response time tracking
request_start = time.time()
response_time = time.time() - request_start

# Memory usage monitoring
session_count = len(active_sessions)
file_count = len(session_files)
```

## 🧪 Testing Strategy

### Unit Testing
**Test Coverage**:
- Configuration management
- Session tracking functionality
- Data processing pipelines
- API integration points

### Integration Testing
**End-to-End Tests**:
- Complete user workflows
- API failure scenarios
- Mobile device compatibility
- Performance under load

### Deployment Testing
**Production Validation**:
- Streamlit Cloud deployment
- Mobile browser testing
- API connectivity verification
- Security feature validation

## 🔄 Maintenance Procedures

### Regular Maintenance
**Daily Tasks**:
- Monitor application health
- Check API response times
- Review security events

**Weekly Tasks**:
- Analyze visitor metrics
- Review configuration settings
- Update documentation

**Monthly Tasks**:
- Performance optimization review
- Security audit
- Backup verification

### Emergency Procedures
**Incident Response**:
1. **API Failure**: Automatic fallback to cached data
2. **High Load**: Built-in rate limiting and caching
3. **Security Issues**: Automatic logging and alerts
4. **Data Loss**: Restore from automatic backups

---

**Technical Specifications**:
- **Python Version**: 3.9+
- **Framework**: Streamlit 1.28+
- **Database**: JSON file storage
- **APIs**: USGS GeoJSON, ipapi.co
- **Deployment**: Streamlit Cloud

**Last Updated**: October 25, 2025  
**Version**: 1.0.0  
**Architecture Status**: ✅ Production Ready
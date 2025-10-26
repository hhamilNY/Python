# 📊 Earthquake Monitor - Logging System Documentation

## 🔧 **Overview**

The USGS Earthquake Monitor application includes a comprehensive logging system that tracks data fetching, user interactions, performance metrics, and errors. This documentation provides details about the logging capabilities and how to use them for monitoring and debugging.

## 📁 **Log File Management**

### **File Location & Structure**
- **Primary Log File**: `logs/earthquake_app.log`
- **Backup Files**: `earthquake_app.log.1`, `earthquake_app.log.2`, etc.
- **Directory**: Automatically created `logs/` folder in application root

### **Rotation Settings**
- **File Size Limit**: 5MB per log file
- **Backup Count**: 10 files maximum
- **Total Storage**: ~50MB maximum (5MB × 10 files)
- **Auto-cleanup**: Oldest files automatically deleted when limit exceeded

## 📋 **Log Format**

```
YYYY-MM-DD HH:MM:SS | LOG_LEVEL | FUNCTION_NAME | MESSAGE
```

### **Example Log Entries**
```
2025-10-25 14:30:15 |     INFO |     fetch_earthquake_data | DATA_FETCH | Requesting data from: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson
2025-10-25 14:30:15 |     INFO |     fetch_earthquake_data | DATA_FETCH | HTTP request completed in 0.234s | Status: 200
2025-10-25 14:30:15 |     INFO |     fetch_earthquake_data | DATA_FETCH | Raw data received: 1300 earthquakes worldwide
2025-10-25 14:30:15 |     INFO |     fetch_earthquake_data | DATA_FETCH | Results: 1300 worldwide → 1391 USA region
2025-10-25 14:30:15 |    ERROR |     fetch_earthquake_data | DATA_FETCH | ANOMALY: USA count (1391) > worldwide count (1300)
2025-10-25 14:30:16 |     INFO |              log_user_action | USER_ACTION | Session: a1b2c3d4 | Action: view_change | Details: map
```

## 🔍 **What Gets Logged**

### **1. 🌐 Data Fetching (`DATA_FETCH`)**
- **API Requests**: URLs, timing, HTTP status codes
- **Response Processing**: JSON parsing, data validation
- **Geographic Filtering**: Worldwide vs USA earthquake counts
- **Data Quality**: Coordinate errors, magnitude validation
- **Anomaly Detection**: Cases where USA count > worldwide count
- **Performance**: Request timing, filtering duration

### **2. 👤 User Actions (`USER_ACTION`)**
- **Session Management**: New session starts with unique IDs
- **Navigation**: Data source changes (Past Hour, All Week, etc.)
- **View Changes**: Overview, Live Map, Statistics, etc.
- **Feature Usage**: Auto-refresh toggles, retry attempts
- **User Journey**: Complete interaction tracking

### **3. 🌍 Visitor Tracking (`NEW_VISITOR`, `PAGE_VIEW`)**
- **Unique Visitors**: Each visitor gets persistent 12-character ID
- **Page Views**: Every page load and interaction tracked
- **Session Correlation**: Visitors linked to sessions
- **Browser Information**: User agent strings when available
- **Return Visits**: Distinguishes new vs returning visitors

### **4. ⚡ Performance Metrics (`PERFORMANCE`)**
- **Function Execution Times**: All major operations timed
- **API Response Times**: Network request duration
- **Data Processing**: Filtering and transformation timing
- **Visualization Rendering**: Chart and map creation performance
- **Cache Performance**: Hit/miss patterns (implicit through timing)

### **5. 🎯 Session Tracking (`SESSION`)**
- **Session Initialization**: New user sessions
- **State Management**: Default settings applied
- **User Preferences**: Feed type and view selections
- **Session Duration**: Implicit through log timestamps

### **6. ⚠️ Error Tracking**
- **Network Errors**: Timeouts, connection failures
- **API Errors**: HTTP error responses, invalid JSON
- **Data Processing Errors**: Coordinate parsing failures
- **Application Errors**: Unexpected exceptions with stack traces

## 📊 **Log Categories & Levels**

### **Log Levels**
- **DEBUG**: Detailed diagnostic information
- **INFO**: General application flow and metrics
- **WARNING**: Potential issues or anomalies
- **ERROR**: Error conditions that need attention

### **Message Categories**
- **`DATA_FETCH`**: All earthquake data retrieval operations
- **`USER_ACTION`**: User interface interactions
- **`SESSION_START`**: New user session beginnings
- **`SESSION_INIT`**: Default state initialization
- **`UI_RENDER`**: User interface rendering operations
- **`PERFORMANCE`**: Execution timing information

## 🔧 **Configuration**

### **Logging Setup**
```python
def setup_logging():
    """Setup rotating file logger with size and count limits"""
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logger with rotation
    handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, 'earthquake_app.log'),
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=10,
        encoding='utf-8'
    )
```

### **Performance Decorator**
```python
@log_performance
def function_name():
    # Automatically logs start time, completion time, and any errors
```

## 📈 **Monitoring & Analysis**

### **Key Metrics to Monitor**
1. **API Performance**: Request response times and success rates
2. **Data Anomalies**: Cases where USA count exceeds worldwide count
3. **User Engagement**: Most popular data sources and views
4. **Error Rates**: Network failures, parsing errors
5. **Performance Trends**: Function execution times over time

### **Useful Log Searches**
```bash
# Find all data anomalies
grep "ANOMALY" logs/earthquake_app.log

# Monitor API performance
grep "HTTP request completed" logs/earthquake_app.log

# Track user behavior
grep "USER_ACTION" logs/earthquake_app.log

# Check error rates
grep "ERROR" logs/earthquake_app.log

# Performance analysis
grep "Completed.*in.*s" logs/earthquake_app.log

# Visitor tracking
grep "NEW_VISITOR" logs/earthquake_app.log

# Page view analysis
grep "PAGE_VIEW" logs/earthquake_app.log

# Popular data sources
grep "data_source_change" logs/earthquake_app.log

# Popular views
grep "view_change" logs/earthquake_app.log
```

## 📊 **Visitor Analytics**

### **Analytics Dashboard**
Access the admin dashboard by adding `?admin=true` to the app URL:
```
http://localhost:8501?admin=true
```

The dashboard shows:
- **📊 Unique Visitors**: Total number of different people who visited
- **👀 Page Views**: Total interactions with the app
- **🆕 New Today**: Visitors who visited for the first time today
- **🔗 Sessions**: Number of browser sessions
- **📡 Popular Data Sources**: Most selected earthquake feeds
- **📱 Popular Views**: Most used view types
- **⚠️ Recent Errors**: Latest error messages

### **Analytics Report Generator**
Run the standalone analytics script:
```bash
python analytics_report.py
```

This generates:
- **Text Report**: Human-readable analytics summary
- **JSON Data**: Machine-readable data for further analysis
- **Daily Activity**: Visitor patterns by day
- **Hourly Patterns**: Peak usage times
- **Performance Metrics**: Function execution times
- **Error Analysis**: Error rates and recent issues

### **Visitor Tracking Features**
- **🔒 Privacy-First**: No personal data collected
- **🆔 Anonymous IDs**: Random 12-character visitor identifiers
- **📱 Cross-Session**: Visitors tracked across browser sessions
- **📊 Usage Patterns**: Data source and view preferences
- **⏰ Activity Times**: Peak usage analysis
- **🌍 Global Reach**: No geographic restrictions

### **Performance Benchmarks**
- **API Requests**: Typically 0.1-0.5 seconds
- **Data Filtering**: Usually < 0.1 seconds
- **Visualization Rendering**: 0.1-0.3 seconds for maps
- **Total Page Load**: Should be < 2 seconds end-to-end

## 🚨 **Common Issues to Monitor**

### **Data Quality Issues**
- **Coordinate Errors**: Invalid latitude/longitude values
- **Missing Magnitudes**: Earthquakes without magnitude data
- **Count Anomalies**: USA count > worldwide count (geographic filtering issue)

### **Performance Issues**
- **Slow API Responses**: > 1 second request times
- **High Error Rates**: > 5% failure rate on API calls
- **Memory Usage**: Large dataset processing performance

### **User Experience Issues**
- **High Retry Rates**: Users frequently clicking retry buttons
- **Short Sessions**: Users leaving quickly (< 30 seconds)
- **Error Encounters**: Users experiencing frequent errors

## 🔒 **Privacy & Security**

### **Data Protection**
- **No Personal Data**: Only session IDs (8-character UUIDs) logged
- **No IP Addresses**: User identification not tracked
- **Local Storage**: All logs stored locally, not transmitted
- **Automatic Cleanup**: Old logs automatically deleted

### **Log File Security**
- **Local Access Only**: Logs stored in application directory
- **UTF-8 Encoding**: Proper character encoding for international data
- **File Permissions**: Standard file system permissions apply

## 🛠️ **Troubleshooting**

### **Log File Issues**
- **Missing Logs**: Check if `logs/` directory exists and is writable
- **Large Files**: Rotation should automatically handle, check backup count
- **Permission Errors**: Ensure application has write access to log directory

### **Performance Debugging**
- **Slow API**: Check network connection and USGS service status
- **High Memory Usage**: Monitor large dataset processing in logs
- **UI Responsiveness**: Review rendering function performance times

## 📝 **Log Maintenance**

### **Regular Maintenance**
- **Monitor Disk Usage**: 50MB maximum, but check periodically
- **Review Error Patterns**: Weekly analysis of error logs
- **Performance Trends**: Monthly review of timing metrics
- **Data Quality**: Regular checks for anomalies

### **Log Analysis Tools**
- **Text Editors**: Basic log viewing and searching
- **Command Line**: `grep`, `awk`, `sed` for pattern analysis
- **Log Analyzers**: Consider tools like Logstash for advanced analysis
- **Custom Scripts**: Python scripts for specific log analysis needs

---

## 📞 **Support**

For questions about the logging system or help with log analysis, refer to the main application documentation or create an issue in the project repository.

**Last Updated**: October 25, 2025
**Version**: 1.0
**Application**: USGS Earthquake Monitor Mobile Web App
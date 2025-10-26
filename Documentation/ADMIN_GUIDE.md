# 🌍 USGS Earthquake Monitor - Admin Guide

## 🔐 Admin Panel Access

### Accessing Admin Features
**Location**: Left sidebar in the application  
**Requirements**: No special authentication required  
**Mobile Access**: Via hamburger menu (≡) on mobile devices  

### Admin Panel Structure
```
📊 Admin Dashboard
├── 👥 Visitor Metrics        # Real-time user analytics
├── 📁 Download Functions     # Data export capabilities
├── 🔧 Manual Actions         # Cleanup and maintenance
└── ⚙️ Configuration         # System settings
```

## 👥 Visitor Analytics

### Real-Time Metrics Display

#### Current Session Statistics
```
Active Visitors: X users currently online
Total Sessions: XXX unique visitors today
Average Session: X.X minutes per visit
Page Views: XXX total pages viewed
```

#### Geographic Analytics
- **Visitor Locations**: Countries and regions
- **US State Tracking**: Detailed US visitor breakdown
- **IP Geolocation**: Automatic location detection
- **Location Trends**: Geographic usage patterns

#### Device Analytics
- **Browser Types**: Chrome, Safari, Firefox breakdown
- **Operating Systems**: iOS, Android, Windows, macOS
- **Screen Resolutions**: Device compatibility data
- **Mobile vs Desktop**: Usage platform statistics

### Enhanced Session Tracking

#### Session Data Collected
```json
{
  "visitor_id": "unique_identifier",
  "location": {
    "country": "United States",
    "region": "California", 
    "city": "San Francisco",
    "us_state": "CA"
  },
  "device_info": {
    "user_agent": "browser_string",
    "screen_resolution": "1920x1080",
    "language": "en-US"
  },
  "session_metrics": {
    "visit_count": 5,
    "total_time": 1800,
    "pages_viewed": 12,
    "last_activity": "2025-10-25T11:45:00Z"
  }
}
```

## 📁 Data Export Functions

### Available Downloads

#### 1. Visitor Metrics Export
**File**: `visitor_metrics_YYYYMMDD_HHMMSS.json`  
**Content**: Complete visitor analytics  
**Format**: JSON with full session data  
**Size**: Varies based on visitor count  

#### 2. Session Analytics Export
**File**: `session_analytics_YYYYMMDD_HHMMSS.csv`  
**Content**: Tabular session data  
**Format**: CSV for spreadsheet analysis  
**Columns**: ID, Location, Device, Sessions, Duration  

#### 3. Enhanced Analytics Export
**File**: `enhanced_analytics_YYYYMMDD_HHMMSS.json`  
**Content**: Comprehensive analytics with US state data  
**Format**: Structured JSON  
**Features**: Geographic breakdowns, trend analysis  

### Export Process
1. **Click Download Button**: Choose desired export format
2. **Processing**: System prepares export file
3. **Download**: Browser downloads file automatically
4. **Success Message**: Confirmation of successful export

### Export Data Structure
```json
{
  "export_metadata": {
    "export_time": "2025-10-25T12:00:00Z",
    "data_range": "2025-10-01 to 2025-10-25",
    "record_count": 1234,
    "export_type": "full_analytics"
  },
  "visitor_summary": {
    "total_visitors": 1234,
    "unique_countries": 45,
    "us_states_count": 28,
    "avg_session_duration": 456
  },
  "detailed_sessions": [...],
  "geographic_breakdown": {...},
  "device_analytics": {...}
}
```

## 🔧 Manual Administrative Actions

### Data Cleanup Operations

#### 1. Clean Old Metrics
**Function**: Remove daily metrics older than configured retention  
**Default**: 90 days retention  
**Action**: `🧹 Clean Old Metrics` button  
**Result**: Frees disk space, maintains performance  

#### 2. Clean Old Sessions
**Function**: Remove session data older than configured retention  
**Default**: 120 days retention  
**Action**: `🔐 Clean Old Sessions` button  
**Result**: Privacy compliance, storage optimization  

#### 3. Security Log Cleanup
**Function**: Remove old security events  
**Default**: 365 days retention  
**Action**: `🛡️ Clean Security Logs` button  
**Result**: Maintains security audit trail within limits  

### Configuration Reset
**Function**: Reset all settings to default values  
**Action**: `🔄 Reset to Defaults` button  
**Warning**: This action cannot be undone  
**Result**: Fresh configuration state  

## ⚙️ Configuration Management

### Retention Policy Settings

#### Data Retention Controls
```
📊 Metrics Retention
├── Days to keep daily metrics: 7-365 days (default: 90)
├── Auto-cleanup frequency: 0-10% (default: 1%)
└── Storage optimization: Automatic

📁 Log File Settings  
├── App log file size: 1-50 MB (default: 5MB)
├── App log backup files: 1-30 files (default: 10)
└── Rotation: Automatic when size limit reached

🔐 User Data Settings
├── User data retention: 30-730 days (default: 180)
├── User session log backups: 10-50 files (default: 20)
└── Privacy compliance: Configurable

🛡️ Security Settings
├── Security log retention: 90-1095 days (default: 365)
├── Event monitoring: Always enabled
└── Audit trail: Comprehensive logging
```

#### Configuration Changes
**Process**:
1. **Adjust Sliders**: Modify retention values
2. **Click Update**: Apply new configuration
3. **Confirmation**: System confirms changes
4. **Immediate Effect**: New settings active immediately

### Storage Management

#### Current Storage Usage Display
```
📁 Enhanced Storage Usage:
├── 📊 Basic metrics: XX,XXX bytes
├── 🔐 Enhanced sessions: XX,XXX bytes  
├── 📋 Configuration: X,XXX bytes
├── 🛡️ Security logs: XX,XXX bytes
└── 💾 Total storage: XXX,XXX bytes
```

#### Storage Optimization
- **Automatic Cleanup**: Based on configured frequency
- **Compression**: Efficient data storage formats
- **Archival**: Old data moved to compressed archives
- **Monitoring**: Real-time storage usage tracking

## 🛡️ Security Monitoring

### Security Events Tracked

#### Event Types
```
🔴 High Priority Events
├── Multiple rapid requests from single IP
├── Unusual access patterns
├── Configuration changes
└── Data export operations

🟡 Medium Priority Events  
├── Failed API requests
├── Session anomalies
├── Geographic access patterns
└── Device fingerprint changes

🟢 Low Priority Events
├── Normal user sessions
├── Successful data loads
├── Regular cleanup operations
└── Configuration reads
```

#### Recent Security Events Display
```
🔒 Recent Security Events:
├── 2025-10-25 11:30: CONFIG_CHANGE (MEDIUM)
├── 2025-10-25 11:15: DATA_EXPORT (HIGH)  
└── 2025-10-25 11:00: NORMAL_SESSION (LOW)
```

### Security Best Practices

#### Monitoring Guidelines
- **Regular Review**: Check security events daily
- **Unusual Patterns**: Investigate high-priority events
- **Configuration Changes**: Monitor admin actions
- **Data Exports**: Track all download operations

#### Privacy Compliance
- **Data Minimization**: Collect only necessary data
- **Retention Limits**: Respect configured retention periods
- **User Rights**: Support data deletion requests
- **Anonymization**: Option to hash IP addresses

## 📊 Performance Monitoring

### System Health Indicators

#### Performance Metrics
```
⚡ Application Performance
├── Response Time: Average API response time
├── Memory Usage: Current application memory
├── Active Sessions: Real-time user count
└── Data Freshness: Last USGS API update

🔄 Background Operations
├── Cleanup Operations: Last cleanup execution
├── Configuration Updates: Recent changes
├── Error Rates: System error frequency
└── API Health: USGS API status
```

#### Optimization Recommendations
- **Regular Cleanup**: Schedule automatic cleanup
- **Monitor Growth**: Track data storage trends
- **Performance Tuning**: Adjust cache settings
- **Capacity Planning**: Monitor usage patterns

## 🚨 Troubleshooting

### Common Admin Issues

#### Export Functions Not Working
**Symptoms**: Download buttons don't respond  
**Causes**: Browser security, network issues  
**Solutions**:
- Check browser popup blockers
- Verify network connectivity  
- Try different browser
- Check JavaScript console for errors

#### Configuration Changes Not Saving
**Symptoms**: Settings revert after refresh  
**Causes**: File permissions, storage issues  
**Solutions**:
- Check application logs
- Verify file system permissions
- Restart application if needed
- Review error messages

#### High Storage Usage
**Symptoms**: Excessive disk space consumption  
**Causes**: Retention settings too high  
**Solutions**:
- Reduce retention periods
- Run manual cleanup operations
- Monitor cleanup frequency
- Review data growth patterns

### Emergency Procedures

#### Data Recovery
1. **Identify Issue**: Determine what data is affected
2. **Check Backups**: Review automatic backup files
3. **Restore Process**: Use most recent valid backup
4. **Verify Integrity**: Confirm data restoration success

#### Performance Issues
1. **Identify Bottleneck**: Check performance metrics
2. **Immediate Actions**: Run cleanup operations
3. **Configuration Adjust**: Modify retention settings
4. **Monitor Results**: Track performance improvements

---

**Admin Quick Reference**:
- **Emergency Cleanup**: Use manual cleanup buttons
- **Configuration Backup**: Export settings before changes
- **Security Review**: Check events daily
- **Performance**: Monitor storage and response times

**Last Updated**: October 25, 2025  
**Version**: 1.0.0  
**Admin Guide Status**: ✅ Complete
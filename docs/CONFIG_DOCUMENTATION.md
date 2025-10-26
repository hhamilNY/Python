# Mobile Earthquake App - Configuration Documentation

## 📋 Configuration System Overview

The Mobile Earthquake App uses a comprehensive configuration system based on `mobile_config.json` that allows you to modify app behavior without changing code.

## 📄 Configuration Files

### **mobile_config.json** - Main Configuration
- **Location:** Root directory of the app
- **Format:** JSON
- **Purpose:** Stores all app settings including retention policies, logging configuration, and feature flags
- **Auto-created:** Yes, with default values if missing

### **app_config.py** - Configuration Manager
- **Purpose:** Handles loading, saving, and managing configuration
- **Features:** Thread-safe operations, automatic defaults, import/export functionality

## ⚙️ Configuration Structure

```json
{
  "retention_policy": {
    "metrics_retention_days": 90,
    "cleanup_frequency_percent": 1,
    "log_max_size_mb": 5,
    "log_backup_count": 10
  },
  "app_settings": {
    "default_feed_type": "all_hour",
    "default_view_type": "overview", 
    "cache_ttl_seconds": 300,
    "admin_mode_enabled": true
  },
  "analytics": {
    "visitor_tracking_enabled": true,
    "performance_logging_enabled": true,
    "error_reporting_enabled": true
  },
  "metadata": {
    "config_version": "1.0",
    "created_date": "2025-10-25T14:30:52.123456",
    "last_updated": "2025-10-25T15:45:12.654321",
    "app_version": "1.0.0"
  }
}
```

## 🗂️ Retention Policy Configuration

### **metrics_retention_days** (Integer)
- **Default:** 90
- **Range:** 7-365 days
- **Purpose:** How long to keep daily visitor/page view breakdowns
- **Note:** Summary statistics are always kept permanently

### **cleanup_frequency_percent** (Integer)
- **Default:** 1
- **Range:** 0-10 percent
- **Purpose:** Chance of automatic cleanup per visitor
- **0 = Manual cleanup only**

### **log_max_size_mb** (Integer)
- **Default:** 5
- **Range:** 1-50 MB
- **Purpose:** Maximum size of each log file before rotation
- **Effect:** When exceeded, creates new log file and archives old one

### **log_backup_count** (Integer)
- **Default:** 10
- **Range:** 1-20 files
- **Purpose:** Number of archived log files to keep
- **Total Storage:** `log_max_size_mb × log_backup_count`

## 🚀 App Settings Configuration

### **default_feed_type** (String)
- **Default:** "all_hour"
- **Options:** "all_hour", "all_day", "all_week", "all_month", "significant_month", "4.5_week", "2.5_week"
- **Purpose:** Default earthquake data source when app loads

### **default_view_type** (String)
- **Default:** "overview"
- **Options:** "overview", "map", "list", "stats", "regional"
- **Purpose:** Default view mode when app loads

### **cache_ttl_seconds** (Integer)
- **Default:** 300 (5 minutes)
- **Range:** 60-3600 seconds
- **Purpose:** How long to cache USGS earthquake data

### **admin_mode_enabled** (Boolean)
- **Default:** true
- **Purpose:** Enable/disable admin dashboard access
- **Security:** Set to false to disable admin features

## 📊 Analytics Configuration

### **visitor_tracking_enabled** (Boolean)
- **Default:** true
- **Purpose:** Enable/disable visitor ID tracking and page view counting

### **performance_logging_enabled** (Boolean)
- **Default:** true
- **Purpose:** Enable/disable function execution time logging

### **error_reporting_enabled** (Boolean)
- **Default:** true
- **Purpose:** Enable/disable error logging and reporting

## 🔧 Configuration Management

### **Admin Panel Access**
1. Go to: `https://mobileearthquake.streamlit.app/?admin=true`
2. Expand: **🗂️ Data Retention Policy**
3. Adjust settings using sliders and inputs
4. Click: **💾 Apply Retention Settings**

### **Export Configuration**
- Click **📋 Export Config** in admin panel
- Downloads complete configuration as JSON
- Filename: `mobile_config_export_YYYYMMDD_HHMMSS.json`

### **Import Configuration**
- Use **📁 Import Config** file uploader in admin panel
- Upload any valid mobile_config.json file
- Settings apply immediately after successful import

### **Reset to Defaults**
- Click **🔄 Reset to Defaults** in admin panel
- Restores all settings to original default values
- Creates backup timestamp in metadata

## 📁 File Locations

### **Development/Local:**
```
project_root/
├── mobile_config.json          # Main configuration
├── mobile_earthquake_app.py     # Main app
├── app_config.py               # Configuration manager
├── visitor_metrics.py          # Metrics storage
├── logs/                       # Log files directory
│   ├── earthquake_app.log      # Current log
│   ├── earthquake_app.log.1    # Backup log 1
│   └── ...                     # Additional backups
└── metrics/                    # Metrics directory
    └── visitor_metrics.json    # Visitor data
```

### **Streamlit Cloud:**
```
/app/
├── mobile_config.json          # Configuration (auto-created)
├── mobile_earthquake_app.py     # Main app
├── app_config.py               # Configuration manager
├── logs/                       # Logs (temporary storage)
└── metrics/                    # Metrics (temporary storage)
```

## ⚠️ Important Notes

### **Streamlit Cloud Considerations:**
- Configuration file persists across app restarts
- Log files are temporary (lost on redeployment)
- Metrics files are temporary (lost on redeployment)
- Use export/download features to preserve data

### **Configuration Validation:**
- Invalid JSON files will fall back to defaults
- Missing sections are automatically added
- Type validation ensures correct data types
- Thread-safe operations prevent corruption

### **Backup Recommendations:**
1. **Export configuration** regularly via admin panel
2. **Download log files** for long-term storage
3. **Export visitor metrics** for historical analysis
4. **Store configs in version control** for deployment consistency

## 🔍 Troubleshooting

### **Configuration Not Loading:**
1. Check if `mobile_config.json` exists in app root
2. Verify JSON syntax is valid
3. Check app logs for configuration errors
4. Use **🔄 Reset to Defaults** if corrupted

### **Settings Not Applying:**
1. Ensure you clicked **💾 Apply Retention Settings**
2. Check for success/error messages in admin panel
3. Verify file permissions (if running locally)
4. Check app logs for save errors

### **Admin Panel Not Accessible:**
1. Verify URL includes `?admin=true`
2. Check `admin_mode_enabled` in configuration
3. Try the fallback **🔧 Admin Dashboard** sidebar button
4. Check for browser cache issues

## 📈 Performance Impact

### **Configuration Loading:**
- **Frequency:** Once per app session
- **Performance:** Minimal (< 1ms for typical config)
- **Caching:** Configuration cached in memory

### **Auto-Cleanup:**
- **Frequency:** Based on `cleanup_frequency_percent`
- **Performance:** Runs in background, minimal impact
- **Timing:** Triggered during visitor tracking

### **Log Rotation:**
- **Frequency:** When log file exceeds `log_max_size_mb`
- **Performance:** Brief pause during rotation
- **Impact:** Negligible for typical usage

## 🎯 Best Practices

### **Retention Settings:**
- **Short-term projects:** 30-60 days retention
- **Long-term monitoring:** 90-180 days retention
- **Research/analysis:** 365 days retention
- **Storage-constrained:** 7-30 days with higher cleanup frequency

### **Log Settings:**
- **Development:** 1-2MB files, 5-10 backups
- **Production:** 5-10MB files, 10-20 backups
- **High-traffic:** Consider external log aggregation

### **Configuration Management:**
- **Version control:** Store baseline configs in Git
- **Environment-specific:** Use different configs per environment
- **Regular backups:** Export configurations monthly
- **Documentation:** Comment configuration changes in commit messages
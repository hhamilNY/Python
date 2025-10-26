# Mobile Earthquake App - Documentation

## 📚 Documentation Index

### **Configuration Management**
- **[CONFIG_DOCUMENTATION.md](CONFIG_DOCUMENTATION.md)** - Comprehensive guide to the configuration system
  - Configuration file structure and options
  - Admin panel usage instructions
  - Retention policy settings
  - Troubleshooting and best practices

### **Enhanced Session Management**
- **[ENHANCED_SESSION_GUIDE.md](ENHANCED_SESSION_GUIDE.md)** - Complete guide to the enhanced session tracking
  - Location tracking and IP geolocation
  - Device fingerprinting and security monitoring
  - Privacy controls and GDPR compliance
  - Advanced analytics and reporting

### **App Documentation**
- **Main App:** `mobile_earthquake_app.py` - Streamlit-based earthquake monitoring application
- **Configuration Manager:** `app_config.py` - Thread-safe JSON configuration management
- **Analytics:** `visitor_metrics.py` - Basic visitor tracking and metrics collection
- **Session Manager:** `user_session_manager.py` - Enhanced session tracking with location and security

## 🚀 Quick Start

1. **Deploy to Streamlit Cloud** - The app auto-creates configuration files
2. **Access Admin Panel** - Visit `https://mobileearthquake.streamlit.app/?admin=true`
3. **Configure Settings** - Use the admin panel to adjust retention policies and app behavior
4. **Export Data** - Download logs and metrics for analysis

## 📖 Key Features

- **Real-time Earthquake Data** from USGS
- **Mobile-Responsive Design** 
- **Enhanced Location Tracking** with IP geolocation
- **Device Fingerprinting** and security monitoring
- **Configurable Data Retention** (7-365 days)
- **Visitor Analytics** with geographic insights
- **Admin Dashboard** with comprehensive controls
- **Persistent Configuration** via JSON files
- **Privacy Controls** and GDPR compliance options

## 🔧 Configuration Files

- `mobile_config.json` - Main configuration (auto-created)
- `sessions/user_sessions.json` - Enhanced session tracking (auto-created)
- `docs/CONFIG_DOCUMENTATION.md` - Complete configuration guide
- `docs/ENHANCED_SESSION_GUIDE.md` - Session management guide

## 📊 Data Management

- **Logs:** Rotated based on size and count settings
- **Basic Metrics:** Cleaned up based on retention policy
- **Enhanced Sessions:** Location and device tracking with security monitoring
- **Configuration:** Persistent across app restarts
- **Privacy:** Configurable data collection and retention policies

## 🌐 Live App

**URL:** https://mobileearthquake.streamlit.app/  
**Admin:** https://mobileearthquake.streamlit.app/?admin=true

## 💡 Support

For configuration questions, refer to:
- **[CONFIG_DOCUMENTATION.md](CONFIG_DOCUMENTATION.md)** - Complete configuration reference
- **[ENHANCED_SESSION_GUIDE.md](ENHANCED_SESSION_GUIDE.md)** - Session management and privacy controls

Both guides include:
- Complete parameter reference
- Step-by-step admin panel guide
- Troubleshooting solutions
- Performance optimization tips
- Privacy and security considerations
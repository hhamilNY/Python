# Mobile Earthquake App - Documentation

## 📚 Documentation Index

### **Configuration Management**
- **[CONFIG_DOCUMENTATION.md](CONFIG_DOCUMENTATION.md)** - Comprehensive guide to the configuration system
  - Configuration file structure and options
  - Admin panel usage instructions
  - Retention policy settings
  - Troubleshooting and best practices

### **App Documentation**
- **Main App:** `mobile_earthquake_app.py` - Streamlit-based earthquake monitoring application
- **Configuration Manager:** `app_config.py` - Thread-safe JSON configuration management
- **Analytics:** `visitor_metrics.py` - Visitor tracking and metrics collection

## 🚀 Quick Start

1. **Deploy to Streamlit Cloud** - The app auto-creates configuration files
2. **Access Admin Panel** - Visit `https://mobileearthquake.streamlit.app/?admin=true`
3. **Configure Settings** - Use the admin panel to adjust retention policies and app behavior
4. **Export Data** - Download logs and metrics for analysis

## 📖 Key Features

- **Real-time Earthquake Data** from USGS
- **Mobile-Responsive Design** 
- **Configurable Data Retention** (7-365 days)
- **Visitor Analytics** with export capabilities
- **Admin Dashboard** with comprehensive controls
- **Persistent Configuration** via JSON files

## 🔧 Configuration Files

- `mobile_config.json` - Main configuration (auto-created)
- `docs/CONFIG_DOCUMENTATION.md` - Complete configuration guide

## 📊 Data Management

- **Logs:** Rotated based on size and count settings
- **Metrics:** Cleaned up based on retention policy
- **Configuration:** Persistent across app restarts

## 🌐 Live App

**URL:** https://mobileearthquake.streamlit.app/  
**Admin:** https://mobileearthquake.streamlit.app/?admin=true

## 💡 Support

For configuration questions, refer to [CONFIG_DOCUMENTATION.md](CONFIG_DOCUMENTATION.md) which includes:
- Complete parameter reference
- Step-by-step admin panel guide
- Troubleshooting solutions
- Performance optimization tips
# 🌍 USGS Earthquake Monitor - Deployment Guide

## 📋 Overview
This guide covers the deployment and maintenance of the USGS Earthquake Monitoring application with enhanced user session management and admin features.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Streamlit Cloud account (for hosted deployment)
- GitHub repository access

### Required Dependencies
```
streamlit
requests
pandas
plotly
ipapi
```

## 🔧 Deployment Options

### Option 1: Streamlit Cloud (Recommended)
1. **Fork/Clone Repository**
   ```bash
   git clone https://github.com/hhamilNY/Python.git
   cd object
   ```

2. **Deploy to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `mobile_earthquake_app.py` as the main file
   - Deploy automatically

3. **Environment Setup**
   - Streamlit Cloud handles dependencies automatically
   - No additional configuration required

### Option 2: Local Development
1. **Install Dependencies**
   ```bash
   pip install streamlit requests pandas plotly ipapi
   ```

2. **Run Locally**
   ```bash
   streamlit run mobile_earthquake_app.py
   ```

3. **Access Application**
   - Local URL: `http://localhost:8501`
   - Network URL: `http://[your-ip]:8501`

## 📱 Mobile Optimization

### Responsive Design Features
- **Mobile-first layout** with collapsed sidebar by default
- **Touch-friendly controls** for earthquake data filtering
- **Optimized charts** for small screens
- **Progressive loading** for better mobile performance

### iOS/Android Testing
- **Chrome Mobile**: Full compatibility
- **Safari iOS**: Tested and working
- **Android Chrome**: Full functionality
- **Mobile browsers**: Responsive design adapts automatically

## 🔐 Security Configuration

### Data Protection
- **IP Address Hashing**: Optional for GDPR compliance
- **Session Encryption**: Secure visitor tracking
- **Rate Limiting**: Built-in protection against abuse
- **Privacy Settings**: Configurable data collection

### Admin Access
- **Sidebar Controls**: Administrative features in left panel
- **Download Protection**: Secure data export functionality
- **Configuration Management**: Real-time settings updates

## 📊 Performance Optimization

### Caching Strategy
- **USGS API Caching**: 5-minute TTL for earthquake data
- **Session Caching**: Persistent visitor tracking
- **Configuration Caching**: In-memory settings storage

### Resource Management
- **Automatic Cleanup**: Configurable data retention policies
- **Background Processing**: Non-blocking cleanup operations
- **Memory Optimization**: Efficient data structure usage

## 🔄 Update Process

### Automatic Updates (Streamlit Cloud)
1. **Code Changes**: Push to GitHub repository
2. **Auto-Deploy**: Streamlit Cloud detects changes
3. **Zero Downtime**: Seamless application updates

### Manual Updates (Local)
1. **Pull Changes**: `git pull origin master`
2. **Restart Application**: `Ctrl+C` then `streamlit run mobile_earthquake_app.py`

## 🛠️ Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.9+

# Install missing dependencies
pip install -r requirements.txt

# Run with debug output
streamlit run mobile_earthquake_app.py --logger.level debug
```

#### API Connection Issues
- **USGS API**: Check internet connection and API status
- **IP Geolocation**: Verify ipapi.co accessibility
- **Fallback Mode**: Application works offline with cached data

#### Mobile Display Issues
- **Clear Browser Cache**: Force refresh on mobile
- **Check Network**: Ensure stable internet connection
- **Browser Compatibility**: Use Chrome or Safari for best results

### Performance Issues
- **Memory Usage**: Monitor with built-in metrics
- **Response Time**: Check network connectivity
- **Data Loading**: Verify USGS API response times

## 📈 Monitoring

### Built-in Analytics
- **Visitor Metrics**: Real-time user tracking
- **Performance Monitoring**: Response time analytics
- **Error Reporting**: Automatic issue detection
- **Usage Statistics**: Comprehensive usage reports

### Health Checks
- **API Status**: Automatic USGS API monitoring
- **Data Freshness**: Real-time earthquake data validation
- **System Resources**: Memory and performance tracking

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set custom cache TTL
STREAMLIT_CACHE_TTL=300

# Optional: Set debug mode
STREAMLIT_DEBUG=true
```

### Application Settings
- **Retention Policies**: User data (20 files), Logs (10 files)
- **Cleanup Frequency**: 1% automatic cleanup
- **Session Timeout**: 120 days default
- **Security Logs**: 365 days retention

## 📞 Support

### Getting Help
- **Documentation**: Check `/Documentation/` folder
- **Issues**: Create GitHub issue for bugs
- **Features**: Submit feature requests via GitHub

### Emergency Contacts
- **Critical Issues**: Check Streamlit Cloud status
- **Data Loss**: Restore from automatic backups
- **Security Issues**: Review security logs in admin panel

---

**Last Updated**: October 25, 2025  
**Version**: 1.0.0  
**Deployment Status**: ✅ Production Ready
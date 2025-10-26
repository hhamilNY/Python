"""
Earthquake Data Module
Handles USGS API integration, data fetching, and processing
"""

import requests
import streamlit as st
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_earthquake_data(feed_type="all_hour"):
    """
    Fetch earthquake data from USGS with caching
    
    Args:
        feed_type (str): Type of earthquake feed to fetch
        
    Returns:
        list: List of earthquake dictionaries
    """
    base_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"
    url = f"{base_url}{feed_type}.geojson"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        earthquakes = []
        for feature in data['features']:
            props = feature['properties']
            coords = feature['geometry']['coordinates']
            
            # Filter for USA earthquakes (including territories)
            longitude, latitude = coords[0], coords[1]
            if -180 <= longitude <= -60 and 15 <= latitude <= 75:
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
        
        logger.info(f"DATA_FETCH | Successfully fetched {len(earthquakes)} earthquakes from {feed_type}")
        return earthquakes
        
    except Exception as e:
        logger.error(f"DATA_FETCH | Error fetching earthquake data: {e}")
        st.error(f"Error fetching earthquake data: {e}")
        return []

def filter_earthquakes_by_magnitude(earthquakes, min_magnitude=0.0):
    """
    Filter earthquakes by minimum magnitude
    
    Args:
        earthquakes (list): List of earthquake dictionaries
        min_magnitude (float): Minimum magnitude threshold
        
    Returns:
        list: Filtered list of earthquakes
    """
    if min_magnitude <= 0.0:
        return earthquakes
    
    filtered = [eq for eq in earthquakes if eq.get('magnitude', 0) >= min_magnitude]
    logger.info(f"DATA_FILTER | Applied magnitude filter ≥{min_magnitude}: {len(filtered)} earthquakes remaining")
    return filtered

def get_valid_earthquakes(earthquakes):
    """
    Get earthquakes with valid magnitude data
    
    Args:
        earthquakes (list): List of earthquake dictionaries
        
    Returns:
        tuple: (valid_earthquakes, valid_count, invalid_count)
    """
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
    valid_count = len(valid_earthquakes)
    invalid_count = len(earthquakes) - valid_count
    
    return valid_earthquakes, valid_count, invalid_count

def get_earthquake_statistics(earthquakes):
    """
    Calculate basic statistics for earthquake data
    
    Args:
        earthquakes (list): List of earthquake dictionaries
        
    Returns:
        dict: Statistics including max, avg magnitude, etc.
    """
    valid_earthquakes, valid_count, invalid_count = get_valid_earthquakes(earthquakes)
    
    if not valid_earthquakes:
        return {
            'total_count': len(earthquakes),
            'valid_count': 0,
            'invalid_count': invalid_count,
            'max_magnitude': 0,
            'avg_magnitude': 0,
            'significant_count': 0,
            'latest_time': None
        }
    
    magnitudes = [eq['magnitude'] for eq in valid_earthquakes]
    
    return {
        'total_count': len(earthquakes),
        'valid_count': valid_count,
        'invalid_count': invalid_count,
        'max_magnitude': max(magnitudes),
        'avg_magnitude': sum(magnitudes) / len(magnitudes),
        'significant_count': sum(1 for m in magnitudes if m >= 4.0),
        'latest_time': max(eq['time'] for eq in valid_earthquakes)
    }

def sort_earthquakes_by_magnitude(earthquakes, reverse=True):
    """
    Sort earthquakes by magnitude
    
    Args:
        earthquakes (list): List of earthquake dictionaries
        reverse (bool): If True, sort descending (highest first)
        
    Returns:
        list: Sorted list of earthquakes
    """
    valid_earthquakes, _, _ = get_valid_earthquakes(earthquakes)
    return sorted(valid_earthquakes, key=lambda x: x['magnitude'], reverse=reverse)

def get_feed_descriptions():
    """
    Get human-readable descriptions for earthquake feeds
    
    Returns:
        dict: Feed type to description mapping
    """
    return {
        "all_hour": "past hour",
        "all_day": "past day", 
        "all_week": "past week",
        "all_month": "past month",
        "significant_month": "significant events (past month)",
        "4.5_week": "magnitude 4.5+ (past week)",
        "2.5_week": "magnitude 2.5+ (past week)"
    }
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
from datetime import datetime
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon
import time
import os
import sys


import os
import sys

# Global status tracking
current_status = {
    'active_option': None,
    'last_data_source': None,
    'total_earthquakes': 0,
    'session_start': datetime.now()
}

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_status_bar():
    """Display current status information"""
    print("="*80)
    print("📊 STATUS BAR")
    print("="*80)
    
    if current_status['active_option']:
        print(f"🟢 Active Option: {current_status['active_option']}")
    else:
        print("⚪ No active monitoring option")
    
    if current_status['last_data_source']:
        print(f"📡 Last Data Source: {current_status['last_data_source']}")
    
    print(f"🔢 Total Earthquakes Processed: {current_status['total_earthquakes']}")
    
    session_duration = datetime.now() - current_status['session_start']
    hours = session_duration.seconds // 3600
    minutes = (session_duration.seconds % 3600) // 60
    print(f"⏰ Session Duration: {hours:02d}:{minutes:02d}")
    print("="*80)
    print()

def highlight_option(option_num, current_selection=None):
    """Return highlighted option text"""
    options = {
        1: "🕐 Past Hour - All earthquakes in the last hour",
        2: "📅 Past Day - All earthquakes in the last day", 
        3: "🌊 Significant Events - Major earthquakes (M4.5+)",
        4: "📊 Live Monitor - Real-time earthquake dashboard",
        5: "🗺️ Geographic Distribution - USA earthquake map",
        6: "🏔️ Regional Analysis - Earthquakes by specific region"
    }
    
    if current_selection == option_num:
        return f"➤ {option_num}. {options[option_num]} ⭐ [SELECTED]"
    else:
        return f"  {option_num}. {options[option_num]}"

def update_status(option_name, data_source=None, earthquake_count=0):
    """Update the global status"""
    current_status['active_option'] = option_name
    if data_source:
        current_status['last_data_source'] = data_source
    current_status['total_earthquakes'] += earthquake_count

def earthquake_monitor():
    """USGS Earthquake Monitoring System for USA"""
    clear_screen()
    
    print("🌍 Welcome to USGS Earthquake Monitor, Henry!")
    print("="*80)
    print("🔍 ENHANCED EARTHQUAKE MONITORING SYSTEM")
    print("="*80)
    
    # Display status bar
    display_status_bar()
    
    print("📋 MONITORING OPTIONS:")
    print("="*80)
    
    # Show menu with highlighting
    selected_option = None
    
    # Display all options
    for i in range(1, 7):
        print(highlight_option(i, selected_option))
    
    print("="*80)
    print("💡 Enter your choice (1-6) or 'q' to quit")
    print("="*80)
    
    while True:
        try:
            user_input = input("\n🎯 Choose monitoring option: ").strip().lower()
            
            if user_input == 'q':
                print("\n� Thank you for using Earthquake Monitor! Stay safe, Henry!")
                return
            
            choice = int(user_input)
            if 1 <= choice <= 6:
                # Clear screen and show selected option
                clear_screen()
                print("� USGS Earthquake Monitor - Processing Selection...")
                print("="*80)
                
                # Display selected option with highlighting
                for i in range(1, 7):
                    print(highlight_option(i, choice))
                
                print("="*80)
                print(f"✅ Loading: {highlight_option(choice).split('. ')[1].split(' ⭐')[0]}...")
                print("="*80)
                
                break
            else:
                print("❌ Please enter a number between 1 and 6, or 'q' to quit.")
        except ValueError:
            print("❌ Please enter a valid number or 'q' to quit.")
    
    # Execute the selected option with status updates
    if choice == 1:
        update_status("Past Hour Monitor", "USGS All Hour Feed")
        monitor_past_hour()
    elif choice == 2:
        update_status("Past Day Monitor", "USGS All Day Feed")
        monitor_past_day()
    elif choice == 3:
        update_status("Significant Events Monitor", "USGS Significant Feed")
        monitor_significant_events()
    elif choice == 4:
        update_status("Live Monitor Dashboard", "USGS Real-time Feed")
        live_earthquake_monitor()
    elif choice == 5:
        update_status("Geographic Distribution", "USGS All Day Feed")
        geographic_distribution()
    elif choice == 6:
        update_status("Regional Analysis", "USGS All Day Feed")
        regional_analysis()
    
    # After completion, show option to return to menu
    print("\n" + "="*80)
    print("🔄 OPTIONS:")
    print("="*80)
    choice = input("Press Enter to return to main menu, or 'q' to quit: ").strip().lower()
    if choice != 'q':
        earthquake_monitor()  # Return to main menu
    else:
        print("\n👋 Thank you for using Earthquake Monitor! Stay safe, Henry!")


def add_us_map_background(ax):
    """Add simple US state boundaries as background"""
    # Simplified US state boundary coordinates (major states)
    # This is a basic approximation for visualization
    
    # California outline
    ca_coords = [[-124.4, 32.5], [-124.4, 42.0], [-120.0, 42.0], [-117.0, 34.0], [-117.0, 32.5], [-124.4, 32.5]]
    california = Polygon(ca_coords, fill=True, facecolor='wheat', edgecolor='darkgray', linewidth=1, alpha=0.5)
    ax.add_patch(california)
    
    # Texas outline (simplified)
    tx_coords = [[-106.6, 25.8], [-93.5, 25.8], [-93.5, 36.5], [-103.0, 36.5], [-106.6, 31.8], [-106.6, 25.8]]
    texas = Polygon(tx_coords, fill=True, facecolor='wheat', edgecolor='darkgray', linewidth=1, alpha=0.5)
    ax.add_patch(texas)
    
    # Florida outline
    fl_coords = [[-87.6, 24.5], [-80.0, 24.5], [-80.0, 31.0], [-87.6, 31.0], [-87.6, 24.5]]
    florida = Polygon(fl_coords, fill=True, facecolor='wheat', edgecolor='darkgray', linewidth=1, alpha=0.5)
    ax.add_patch(florida)
    
    # New York outline
    ny_coords = [[-79.8, 40.5], [-71.8, 40.5], [-71.8, 45.0], [-79.8, 45.0], [-79.8, 40.5]]
    newyork = Polygon(ny_coords, fill=True, facecolor='wheat', edgecolor='darkgray', linewidth=1, alpha=0.5)
    ax.add_patch(newyork)
    
    # Washington state outline
    wa_coords = [[-124.8, 45.5], [-116.9, 45.5], [-116.9, 49.0], [-124.8, 49.0], [-124.8, 45.5]]
    washington = Polygon(wa_coords, fill=True, facecolor='wheat', edgecolor='darkgray', linewidth=1, alpha=0.5)
    ax.add_patch(washington)
    
    # Nevada outline
    nv_coords = [[-120.0, 35.0], [-114.0, 35.0], [-114.0, 42.0], [-120.0, 42.0], [-120.0, 35.0]]
    nevada = Polygon(nv_coords, fill=True, facecolor='wheat', edgecolor='darkgray', linewidth=1, alpha=0.5)
    ax.add_patch(nevada)
    
    # Colorado outline
    co_coords = [[-109.0, 37.0], [-102.0, 37.0], [-102.0, 41.0], [-109.0, 41.0], [-109.0, 37.0]]
    colorado = Polygon(co_coords, fill=True, facecolor='wheat', edgecolor='darkgray', linewidth=1, alpha=0.5)
    ax.add_patch(colorado)
    
    # Alaska outline (simplified)
    ak_coords = [[-170.0, 54.0], [-130.0, 54.0], [-130.0, 71.0], [-170.0, 71.0], [-170.0, 54.0]]
    alaska = Polygon(ak_coords, fill=True, facecolor='wheat', edgecolor='darkgray', linewidth=1, alpha=0.5)
    ax.add_patch(alaska)
    
    # Hawaii outline (positioned in view)
    hi_coords = [[-161.0, 18.5], [-154.5, 18.5], [-154.5, 22.5], [-161.0, 22.5], [-161.0, 18.5]]
    hawaii = Polygon(hi_coords, fill=True, facecolor='wheat', edgecolor='darkgray', linewidth=1, alpha=0.5)
    ax.add_patch(hawaii)
    
    # Add state labels
    ax.text(-119, 36, 'CA', fontsize=9, ha='center', va='center', alpha=0.9, color='black', fontweight='bold')
    ax.text(-99, 31, 'TX', fontsize=9, ha='center', va='center', alpha=0.9, color='black', fontweight='bold')
    ax.text(-83, 27, 'FL', fontsize=9, ha='center', va='center', alpha=0.9, color='black', fontweight='bold')
    ax.text(-75, 42.5, 'NY', fontsize=9, ha='center', va='center', alpha=0.9, color='black', fontweight='bold')
    ax.text(-121, 47, 'WA', fontsize=9, ha='center', va='center', alpha=0.9, color='black', fontweight='bold')
    ax.text(-117, 38.5, 'NV', fontsize=9, ha='center', va='center', alpha=0.9, color='black', fontweight='bold')
    ax.text(-105.5, 39, 'CO', fontsize=9, ha='center', va='center', alpha=0.9, color='black', fontweight='bold')
    ax.text(-150, 62, 'AK', fontsize=9, ha='center', va='center', alpha=0.9, color='black', fontweight='bold')
    ax.text(-157.5, 20.5, 'HI', fontsize=9, ha='center', va='center', alpha=0.9, color='black', fontweight='bold')


def fetch_earthquake_data(feed_type="all_hour"):
    """Fetch earthquake data from USGS"""
    base_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"
    url = f"{base_url}{feed_type}.geojson"
    
    try:
        print("📡 Fetching earthquake data from USGS...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        earthquakes = []
        for feature in data['features']:
            props = feature['properties']
            coords = feature['geometry']['coordinates']
            
            # Filter for USA earthquakes (approximate coordinates)
            longitude, latitude = coords[0], coords[1]
            if -180 <= longitude <= -60 and 15 <= latitude <= 75:  # USA bounds
                earthquakes.append({
                    'magnitude': props.get('mag', 0),
                    'place': props.get('place', 'Unknown'),
                    'time': props.get('time', 0),
                    'depth': coords[2] if len(coords) > 2 else 0,
                    'longitude': longitude,
                    'latitude': latitude,
                    'alert': props.get('alert'),
                    'tsunami': props.get('tsunami', 0)
                })
        
        print(f"✅ Found {len(earthquakes)} earthquakes in USA")
        return earthquakes
    
    except requests.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing data: {e}")
        return []


def monitor_past_hour():
    """Monitor earthquakes from the past hour"""
    print("\n🕐 Monitoring Past Hour Earthquakes...")
    print("📡 Fetching data from USGS All Hour feed...")
    
    earthquakes = fetch_earthquake_data("all_hour")
    if not earthquakes:
        print("❌ No earthquake data available.")
        return
    
    # Update status with earthquake count
    earthquake_count = len(earthquakes)
    current_status['total_earthquakes'] += earthquake_count
    
    print(f"✅ Successfully retrieved {earthquake_count} earthquakes")
    print("📊 Generating analysis charts...")
    
    # Extract data for plotting
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
    magnitudes = [eq['magnitude'] for eq in valid_earthquakes]
    depths = [eq['depth'] for eq in valid_earthquakes if eq['depth'] > 0]
    times = [datetime.fromtimestamp(eq['time']/1000) for eq in valid_earthquakes]
    
    print(f"📈 Creating visualizations for {len(valid_earthquakes)} valid earthquakes...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('🕐 Past Hour Earthquake Analysis - Status: ACTIVE', fontsize=14, fontweight='bold')
    
    # Magnitude histogram
    if magnitudes:
        ax1.hist(magnitudes, bins=15, alpha=0.7, color='red', edgecolor='black')
        ax1.set_title(f'Magnitude Distribution ({len(magnitudes)} events)')
        ax1.set_xlabel('Magnitude')
        ax1.set_ylabel('Count')
        ax1.grid(True, alpha=0.3)
        
        # Add magnitude statistics
        mean_mag = np.mean(magnitudes)
        max_mag = max(magnitudes)
        ax1.axvline(mean_mag, color='blue', linestyle='--', label=f'Mean: {mean_mag:.2f}')
        ax1.axvline(max_mag, color='orange', linestyle='--', label=f'Max: {max_mag:.2f}')
        ax1.legend()
    
    # Depth vs Magnitude scatter
    valid_depth_earthquakes = [eq for eq in valid_earthquakes if eq['depth'] > 0]
    if valid_depth_earthquakes:
        scatter_depths = [eq['depth'] for eq in valid_depth_earthquakes]
        scatter_mags = [eq['magnitude'] for eq in valid_depth_earthquakes]
        scatter = ax2.scatter(scatter_mags, scatter_depths, alpha=0.6, c=scatter_mags, 
                            cmap='Reds', s=50)
        
        # Add hover annotations for depth vs magnitude plot
        depth_annotations = []
        for i, eq in enumerate(valid_depth_earthquakes):
            place = eq['place']
            time_str = datetime.fromtimestamp(eq['time']/1000).strftime('%m/%d/%Y %H:%M:%S UTC')
            mag = eq['magnitude']
            depth = eq['depth']
            
            annotation_text = f"Location: {place}\nMagnitude: {mag:.1f}\nDepth: {depth:.1f} km\nTime: {time_str}"
            
            annot = ax2.annotate(annotation_text, (mag, depth),
                               xytext=(10, 10), textcoords='offset points',
                               bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.9),
                               fontsize=8, ha='left', va='bottom',
                               visible=False)
            depth_annotations.append(annot)
        
        # Create hover function for depth plot
        def on_hover_depth(event):
            if event.inaxes == ax2:
                # Check if mouse is over any point
                contains, info = scatter.contains(event)
                if contains:
                    # Get the index of the point
                    point_index = info['ind'][0]
                    
                    # Hide all annotations first
                    for annot in depth_annotations:
                        annot.set_visible(False)
                    
                    # Show annotation for hovered point
                    depth_annotations[point_index].set_visible(True)
                    fig.canvas.draw()
                else:
                    # Hide all annotations if not hovering over any point
                    for annot in depth_annotations:
                        annot.set_visible(False)
                    fig.canvas.draw()
        
        # Connect hover event for depth plot
        fig.canvas.mpl_connect('motion_notify_event', on_hover_depth)
        
        ax2.set_title('Magnitude vs Depth')
        ax2.set_xlabel('Magnitude')
        ax2.set_ylabel('Depth (km)')
        ax2.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax2, label='Magnitude')
    
    # Timeline
    if times and magnitudes:
        timeline_scatter = ax3.scatter(times, magnitudes, alpha=0.7, c='blue', s=40)
        
        # Add hover annotations for timeline plot
        timeline_annotations = []
        for i, eq in enumerate(valid_earthquakes):
            place = eq['place']
            time_str = datetime.fromtimestamp(eq['time']/1000).strftime('%m/%d/%Y %H:%M:%S UTC')
            mag = eq['magnitude']
            time_dt = datetime.fromtimestamp(eq['time']/1000)
            
            annotation_text = f"Location: {place}\nMagnitude: {mag:.1f}\nTime: {time_str}"
            
            annot = ax3.annotate(annotation_text, (time_dt, mag),
                               xytext=(10, 10), textcoords='offset points',
                               bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.9),
                               fontsize=8, ha='left', va='bottom',
                               visible=False)
            timeline_annotations.append(annot)
        
        # Create hover function for timeline plot
        def on_hover_timeline(event):
            if event.inaxes == ax3:
                # Check if mouse is over any point
                contains, info = timeline_scatter.contains(event)
                if contains:
                    # Get the index of the point
                    point_index = info['ind'][0]
                    
                    # Hide all annotations first
                    for annot in timeline_annotations:
                        annot.set_visible(False)
                    
                    # Show annotation for hovered point
                    timeline_annotations[point_index].set_visible(True)
                    fig.canvas.draw()
                else:
                    # Hide all annotations if not hovering over any point
                    for annot in timeline_annotations:
                        annot.set_visible(False)
                    fig.canvas.draw()
        
        # Connect hover event for timeline plot
        fig.canvas.mpl_connect('motion_notify_event', on_hover_timeline)
        
        ax3.set_title('Earthquake Timeline')
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Magnitude')
        ax3.grid(True, alpha=0.3)
        # Format x-axis for datetime
        import matplotlib.dates as mdates
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
    
    # Alert levels
    alert_levels = [eq['alert'] for eq in earthquakes if eq['alert']]
    if alert_levels:
        alert_counts = {}
        for alert in alert_levels:
            alert_counts[alert] = alert_counts.get(alert, 0) + 1
        
        colors = {'green': 'green', 'yellow': 'yellow', 'orange': 'orange', 'red': 'red'}
        bars = ax4.bar(alert_counts.keys(), alert_counts.values(), 
                      color=[colors.get(k, 'gray') for k in alert_counts.keys()])
        ax4.set_title('Alert Levels')
        ax4.set_ylabel('Count')
        ax4.grid(True, alpha=0.3)
    else:
        ax4.text(0.5, 0.5, 'No Alert Data', ha='center', va='center', 
                transform=ax4.transAxes, fontsize=12)
    
    plt.tight_layout()
    plt.suptitle('USGS Earthquake Monitor - Past Hour', fontsize=16, y=0.98)
    plt.show()
    
    # Status completion message
    print("\n" + "="*80)
    print("✅ PAST HOUR ANALYSIS COMPLETED")
    print("="*80)
    print(f"📊 Analysis Status: COMPLETE")
    print(f"📈 Earthquakes Processed: {len(valid_earthquakes)} events")
    print(f"🔍 Data Source: USGS All Hour Feed")
    print(f"⏰ Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)


def monitor_past_day():
    """Monitor earthquakes from the past day"""
    print("\n📅 Monitoring Past Day Earthquakes...")
    print("📡 Fetching data from USGS All Day feed...")
    
    earthquakes = fetch_earthquake_data("all_day")
    if not earthquakes:
        print("❌ No earthquake data available.")
        return
    
    # Update status with earthquake count
    earthquake_count = len(earthquakes)
    current_status['total_earthquakes'] += earthquake_count
    
    print(f"✅ Successfully retrieved {earthquake_count} earthquakes")
    print("📊 Generating daily analysis...")
    
    magnitudes = [eq['magnitude'] for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('📅 Past Day Earthquake Analysis - Status: ACTIVE', fontsize=14, fontweight='bold')
    
    # Magnitude distribution
    if magnitudes:
        ax1.hist(magnitudes, bins=20, alpha=0.7, color='blue', edgecolor='black')
        ax1.set_title(f'24-Hour Magnitude Distribution\n({len(magnitudes)} events)')
        ax1.set_xlabel('Magnitude')
        ax1.set_ylabel('Count')
        ax1.grid(True, alpha=0.3)
        
        # Statistics
        stats_text = f'Mean: {np.mean(magnitudes):.2f}\n'
        stats_text += f'Max: {max(magnitudes):.2f}\n'
        stats_text += f'Min: {min(magnitudes):.2f}\n'
        stats_text += f'Std: {np.std(magnitudes):.2f}'
        ax1.text(0.7, 0.7, stats_text, transform=ax1.transAxes, 
                bbox=dict(boxstyle="round", facecolor='wheat', alpha=0.8))
    
    # Magnitude categories
    if magnitudes:
        categories = {'Minor (2.0-2.9)': 0, 'Light (3.0-3.9)': 0, 
                     'Moderate (4.0-4.9)': 0, 'Strong (5.0-5.9)': 0, 
                     'Major (6.0+)': 0}
        
        for mag in magnitudes:
            if 2.0 <= mag < 3.0:
                categories['Minor (2.0-2.9)'] += 1
            elif 3.0 <= mag < 4.0:
                categories['Light (3.0-3.9)'] += 1
            elif 4.0 <= mag < 5.0:
                categories['Moderate (4.0-4.9)'] += 1
            elif 5.0 <= mag < 6.0:
                categories['Strong (5.0-5.9)'] += 1
            elif mag >= 6.0:
                categories['Major (6.0+)'] += 1
        
        colors = ['lightblue', 'yellow', 'orange', 'red', 'darkred']
        bars = ax2.bar(range(len(categories)), categories.values(), color=colors)
        ax2.set_title('Earthquake Categories (Past 24h)')
        ax2.set_xticks(range(len(categories)))
        ax2.set_xticklabels(categories.keys(), rotation=45, ha='right')
        ax2.set_ylabel('Count')
        ax2.grid(True, alpha=0.3)
        
        # Add count labels on bars
        for bar, count in zip(bars, categories.values()):
            if count > 0:
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        str(count), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    # Status completion message
    print("\n" + "="*80)
    print("✅ PAST DAY ANALYSIS COMPLETED")
    print("="*80)
    print(f"📊 Analysis Status: COMPLETE")
    print(f"📈 Earthquakes Processed: {len(magnitudes)} events")
    print(f"🔍 Data Source: USGS All Day Feed")
    print(f"⏰ Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)


def monitor_significant_events():
    """Monitor significant earthquake events"""
    print("\n🌊 Monitoring Significant Earthquake Events...")
    print("📡 Fetching data from USGS Significant Events feed...")
    
    earthquakes = fetch_earthquake_data("significant_month")
    if not earthquakes:
        print("❌ No significant earthquake data available.")
        return
    
    # Filter for recent significant events
    significant = [eq for eq in earthquakes if eq['magnitude'] >= 4.5]
    
    # Update status with earthquake count
    earthquake_count = len(significant)
    current_status['total_earthquakes'] += earthquake_count
    
    if not significant:
        print("✅ No significant earthquakes (M4.5+) found recently - Good news!")
        return
    
    print(f"⚠️ Found {earthquake_count} significant earthquakes (M4.5+)")
    print("📊 Generating significance analysis...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.suptitle('🌊 Significant Earthquake Events - Status: MONITORING', fontsize=14, fontweight='bold')
    
    magnitudes = [eq['magnitude'] for eq in significant]
    places = [eq['place'][:30] + '...' if len(eq['place']) > 30 else eq['place'] 
              for eq in significant]
    times = [datetime.fromtimestamp(eq['time']/1000) for eq in significant]
    
    # Create timeline plot
    colors = ['red' if mag >= 6.0 else 'orange' if mag >= 5.0 else 'yellow' 
              for mag in magnitudes]
    sizes = [mag * 20 for mag in magnitudes]
    
    # Convert times to matplotlib dates for proper plotting
    import matplotlib.dates as mdates
    mdates_times = mdates.date2num(times)
    
    scatter = ax.scatter(mdates_times, magnitudes, c=colors, s=sizes, alpha=0.7, edgecolors='black')
    
    # Add labels for major events
    for i, (time, mag, place) in enumerate(zip(mdates_times, magnitudes, places)):
        if mag >= 5.0:  # Label major earthquakes
            ax.annotate(f'M{mag:.1f}\n{place}', (time, mag), 
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, ha='left', va='bottom',
                       bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.7))
    
    ax.set_title('Significant Earthquake Events (M4.5+)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date/Time')
    ax.set_ylabel('Magnitude')
    ax.grid(True, alpha=0.3)
    
    # Format x-axis for dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    # Add legend
    legend_elements = [plt.scatter([], [], c='yellow', s=100, label='M4.5-4.9'),
                      plt.scatter([], [], c='orange', s=100, label='M5.0-5.9'),
                      plt.scatter([], [], c='red', s=100, label='M6.0+')]
    ax.legend(handles=legend_elements, loc='upper left')
    
    plt.tight_layout()
    plt.show()
    
    # Status completion message
    print("\n" + "="*80)
    print("✅ SIGNIFICANT EVENTS ANALYSIS COMPLETED")
    print("="*80)
    print(f"📊 Analysis Status: COMPLETE")
    print(f"⚠️ Significant Earthquakes Found: {earthquake_count} events (M4.5+)")
    print(f"🔍 Data Source: USGS Significant Events Feed")
    print(f"⏰ Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)


def live_earthquake_monitor():
    """Live earthquake monitoring dashboard"""
    print("\n📊 Starting Live Earthquake Monitor...")
    print("🔄 Real-time updates every 30 seconds")
    print("⚠️ Press Ctrl+C or close window to stop monitoring")
    print("📡 Connecting to USGS live data feed...")
    
    # Update status for live monitoring
    current_status['active_option'] = "Live Monitor Dashboard - REAL-TIME"
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('📊 Live Earthquake Dashboard - Status: REAL-TIME MONITORING', fontsize=14, fontweight='bold')
    
    def update_dashboard(frame):
        earthquakes = fetch_earthquake_data("all_hour")
        
        # Clear all subplots
        for ax in [ax1, ax2, ax3, ax4]:
            ax.clear()
        
        if not earthquakes:
            ax1.text(0.5, 0.5, 'No Data Available', ha='center', va='center',
                    transform=ax1.transAxes, fontsize=14)
            return []
        
        magnitudes = [eq['magnitude'] for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
        depths = [eq['depth'] for eq in earthquakes if eq['depth'] > 0]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Live magnitude histogram
        artists = []
        if magnitudes:
            n, bins, patches = ax1.hist(magnitudes, bins=10, alpha=0.7, color='red', edgecolor='black')
            ax1.set_title(f'Live Magnitude Distribution\nUpdated: {current_time}')
            ax1.set_xlabel('Magnitude')
            ax1.set_ylabel('Count')
            ax1.grid(True, alpha=0.3)
            artists.extend(patches)
        
        # Recent activity (last 10 earthquakes)
        if earthquakes:
            recent = sorted(earthquakes, key=lambda x: x['time'], reverse=True)[:10]
            recent_mags = [eq['magnitude'] for eq in recent]
            recent_times = [datetime.fromtimestamp(eq['time']/1000) for eq in recent]
            
            line, = ax2.plot(range(len(recent_mags)), recent_mags, 'bo-', linewidth=2, markersize=6)
            ax2.set_title('Last 10 Earthquakes')
            ax2.set_xlabel('Event (most recent first)')
            ax2.set_ylabel('Magnitude')
            ax2.grid(True, alpha=0.3)
            ax2.invert_xaxis()  # Most recent on left
            artists.append(line)
        
        # Depth distribution
        if depths:
            n, bins, patches = ax3.hist(depths, bins=15, alpha=0.7, color='blue', edgecolor='black')
            ax3.set_title('Depth Distribution')
            ax3.set_xlabel('Depth (km)')
            ax3.set_ylabel('Count')
            ax3.grid(True, alpha=0.3)
            artists.extend(patches)
        
        # Statistics panel
        if magnitudes:
            stats_text = f'Total Events: {len(earthquakes)}\n'
            stats_text += f'USA Events: {len(magnitudes)}\n'
            stats_text += f'Max Magnitude: {max(magnitudes):.2f}\n'
            stats_text += f'Avg Magnitude: {np.mean(magnitudes):.2f}\n'
            stats_text += f'Major (M5.0+): {sum(1 for m in magnitudes if m >= 5.0)}\n'
            stats_text += f'Moderate (M4.0+): {sum(1 for m in magnitudes if m >= 4.0)}'
            
            text = ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, fontsize=12,
                    verticalalignment='top', fontfamily='monospace',
                    bbox=dict(boxstyle="round", facecolor='lightblue', alpha=0.8))
            ax4.set_title('Live Statistics')
            ax4.axis('off')
            artists.append(text)
        
        return artists
    
    anim = FuncAnimation(fig, update_dashboard, interval=30000, repeat=True)  # 30 seconds
    plt.tight_layout()
    plt.suptitle('USGS Live Earthquake Monitor - USA', fontsize=16, y=0.98)
    plt.show()


def geographic_distribution():
    """Show geographic distribution of earthquakes"""
    print("\n🗺️ Analyzing Geographic Distribution...")
    print("📡 Fetching geographical earthquake data...")
    
    earthquakes = fetch_earthquake_data("all_day")
    if not earthquakes:
        print("❌ No earthquake data available.")
        return
    
    # Update status with earthquake count
    earthquake_count = len(earthquakes)
    current_status['total_earthquakes'] += earthquake_count
    
    print(f"✅ Retrieved {earthquake_count} earthquakes for geographic analysis")
    print("🗺️ Generating US earthquake distribution map...")
    
    # Extract coordinates and magnitudes - ensure all arrays match
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
    lats = [eq['latitude'] for eq in valid_earthquakes]
    lons = [eq['longitude'] for eq in valid_earthquakes]
    mags = [eq['magnitude'] for eq in valid_earthquakes]
    
    print(f"📍 Plotting {len(valid_earthquakes)} earthquakes on map...")
    
    # Show Geographic Map first
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    fig1.suptitle('🗺️ Geographic Distribution - Status: MAPPING', fontsize=14, fontweight='bold')
    
    # Set ocean background color
    ax1.set_facecolor('lightblue')
    
    # Add US map background
    add_us_map_background(ax1)
    
    # Geographic scatter plot
    if lats and lons and mags:
        # Size based on magnitude, color based on magnitude
        sizes = [max(20, mag * 15) for mag in mags]
        scatter = ax1.scatter(lons, lats, c=mags, s=sizes, alpha=0.6, 
                            cmap='Reds', edgecolors='black', linewidth=0.5)
        
        # Create hover annotations
        annotations = []
        for i, (lon, lat, mag, eq) in enumerate(zip(lons, lats, mags, valid_earthquakes)):
            # Create invisible annotation for each point
            place = eq['place']
            time_str = datetime.fromtimestamp(eq['time']/1000).strftime('%m/%d/%Y %H:%M:%S UTC')
            depth = eq['depth']
            
            annotation_text = f"Location: {place}\nMagnitude: {mag:.1f}\nDepth: {depth:.1f} km\nTime: {time_str}"
            
            annot = ax1.annotate(annotation_text, (lon, lat),
                               xytext=(10, 10), textcoords='offset points',
                               bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.9),
                               fontsize=8, ha='left', va='bottom',
                               visible=False)
            annotations.append(annot)
        
        # Create hover function
        def on_hover(event):
            if event.inaxes == ax1:
                # Check if mouse is over any point
                contains, info = scatter.contains(event)
                if contains:
                    # Get the index of the point
                    point_index = info['ind'][0]
                    
                    # Hide all annotations first
                    for annot in annotations:
                        annot.set_visible(False)
                    
                    # Show annotation for hovered point
                    annotations[point_index].set_visible(True)
                    fig1.canvas.draw()
                else:
                    # Hide all annotations if not hovering over any point
                    for annot in annotations:
                        annot.set_visible(False)
                    fig1.canvas.draw()
        
        # Connect hover event
        fig1.canvas.mpl_connect('motion_notify_event', on_hover)
        
        ax1.set_title('United States Earthquake Locations (Past 24h)', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Longitude')
        ax1.set_ylabel('Latitude')
        ax1.grid(True, alpha=0.3)
        
        # Add state boundaries (includes Hawaii and Alaska)
        ax1.set_xlim(-175, -65)
        ax1.set_ylim(15, 75)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax1)
        cbar.set_label('Magnitude')
        
        # Add major earthquake annotations
        for lon, lat, mag in zip(lons, lats, mags):
            if mag >= 4.0:
                ax1.annotate(f'M{mag:.1f}', (lon, lat), xytext=(3, 3), 
                           textcoords='offset points', fontsize=8,
                           bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.show()
    
    # Show Regional Analysis second
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    
    # Regional activity
    regions = {'California': 0, 'Alaska': 0, 'Nevada': 0, 'Hawaii': 0, 'Other': 0}
    
    for eq in valid_earthquakes:
        place = eq['place'].lower()
        if 'california' in place or 'ca' in place:
            regions['California'] += 1
        elif 'alaska' in place or 'ak' in place:
            regions['Alaska'] += 1
        elif 'nevada' in place or 'nv' in place:
            regions['Nevada'] += 1
        elif 'hawaii' in place or 'hi' in place:
            regions['Hawaii'] += 1
        else:
            regions['Other'] += 1
    
    # Regional bar chart
    region_names = list(regions.keys())
    region_counts = list(regions.values())
    bars = ax2.bar(region_names, region_counts, 
                  color=['gold', 'lightblue', 'lightgreen', 'coral', 'lightgray'])
    ax2.set_title('Earthquake Activity by Region', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Number of Earthquakes')
    ax2.grid(True, alpha=0.3)
    
    # Add count labels on bars
    for bar, count in zip(bars, region_counts):
        if count > 0:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()


def regional_analysis():
    """Detailed analysis of earthquakes by specific region"""
    print("\n🏔️ Regional Earthquake Analysis...")
    print("📡 Preparing regional seismic data analysis...")
    print("="*80)
    print("🗺️ AVAILABLE SEISMIC REGIONS:")
    print("="*80)
    print("1. 🌴 California - West Coast seismic zone")
    print("2. ❄️ Alaska - Arctic seismic activity")
    print("3. 🏜️ Nevada - Basin and Range region")
    print("4. 🌺 Hawaii - Volcanic earthquake zone")
    print("5. 🗽 Pacific Northwest - Oregon & Washington")
    print("6. 🏔️ Yellowstone Region - Montana, Wyoming, Idaho")
    print("7. 🌪️ New Madrid - Central/Eastern US")
    print("8. 🏛️ East Coast - Atlantic seismic zone")
    print("="*80)
    print("💡 Each region has unique geological characteristics and earthquake patterns")
    print("="*80)
    
    while True:
        try:
            region_choice = int(input("Choose region to analyze (1-8): "))
            if 1 <= region_choice <= 8:
                break
            else:
                print("Please enter a number between 1 and 8.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Define region parameters
    regions = {
        1: {
            'name': 'California',
            'keywords': ['california', 'ca', 'san francisco', 'los angeles', 'san diego', 'oakland'],
            'bounds': {'lat': (32.0, 42.0), 'lon': (-125.0, -114.0)},
            'emoji': '🌴'
        },
        2: {
            'name': 'Alaska', 
            'keywords': ['alaska', 'ak', 'anchorage', 'fairbanks'],
            'bounds': {'lat': (54.0, 71.5), 'lon': (-180.0, -130.0)},
            'emoji': '❄️'
        },
        3: {
            'name': 'Nevada',
            'keywords': ['nevada', 'nv', 'las vegas', 'reno'],
            'bounds': {'lat': (35.0, 42.0), 'lon': (-120.0, -114.0)},
            'emoji': '🏜️'
        },
        4: {
            'name': 'Hawaii',
            'keywords': ['hawaii', 'hi', 'mauna', 'kilauea', 'hilo'],
            'bounds': {'lat': (18.5, 22.5), 'lon': (-161.0, -154.5)},
            'emoji': '🌺'
        },
        5: {
            'name': 'Pacific Northwest',
            'keywords': ['oregon', 'washington', 'or', 'wa', 'seattle', 'portland'],
            'bounds': {'lat': (42.0, 49.0), 'lon': (-125.0, -116.0)},
            'emoji': '🗽'
        },
        6: {
            'name': 'Yellowstone Region',
            'keywords': ['yellowstone', 'montana', 'wyoming', 'idaho', 'mt', 'wy', 'id'],
            'bounds': {'lat': (42.0, 49.0), 'lon': (-117.0, -104.0)},
            'emoji': '🏔️'
        },
        7: {
            'name': 'New Madrid Zone',
            'keywords': ['missouri', 'arkansas', 'tennessee', 'kentucky', 'mo', 'ar', 'tn', 'ky'],
            'bounds': {'lat': (35.0, 40.0), 'lon': (-95.0, -85.0)},
            'emoji': '🌪️'
        },
        8: {
            'name': 'East Coast',
            'keywords': ['virginia', 'north carolina', 'south carolina', 'georgia', 'va', 'nc', 'sc', 'ga'],
            'bounds': {'lat': (32.0, 40.0), 'lon': (-85.0, -75.0)},
            'emoji': '🏛️'
        }
    }
    
    selected_region = regions[region_choice]
    print(f"\n{selected_region['emoji']} Analyzing {selected_region['name']} Region...")
    
    # Fetch earthquake data
    earthquakes = fetch_earthquake_data("all_week")  # Get more data for regional analysis
    if not earthquakes:
        print("No earthquake data available.")
        return
    
    # Filter earthquakes for selected region
    regional_earthquakes = []
    for eq in earthquakes:
        place = eq['place'].lower()
        lat, lon = eq['latitude'], eq['longitude']
        
        # Check if earthquake matches region by location name or coordinates
        name_match = any(keyword in place for keyword in selected_region['keywords'])
        coord_match = (selected_region['bounds']['lat'][0] <= lat <= selected_region['bounds']['lat'][1] and
                      selected_region['bounds']['lon'][0] <= lon <= selected_region['bounds']['lon'][1])
        
        if name_match or coord_match:
            regional_earthquakes.append(eq)
    
    if not regional_earthquakes:
        print(f"No earthquakes found in {selected_region['name']} region recently.")
        return
    
    print(f"✅ Found {len(regional_earthquakes)} earthquakes in {selected_region['name']}")
    
    # Extract data for analysis
    valid_earthquakes = [eq for eq in regional_earthquakes if eq['magnitude'] is not None and eq['magnitude'] > 0]
    magnitudes = [eq['magnitude'] for eq in valid_earthquakes]
    depths = [eq['depth'] for eq in valid_earthquakes if eq['depth'] > 0]
    times = [datetime.fromtimestamp(eq['time']/1000) for eq in valid_earthquakes]
    
    # Create comprehensive regional analysis
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 7))
    fig.subplots_adjust(hspace=0.35, wspace=0.3)
    
    # Magnitude distribution
    if magnitudes:
        ax1.hist(magnitudes, bins=15, alpha=0.7, color='darkblue', edgecolor='black')
        ax1.set_title(f'{selected_region["emoji"]} {selected_region["name"]} - Magnitude Distribution')
        ax1.set_xlabel('Magnitude')
        ax1.set_ylabel('Count')
        ax1.grid(True, alpha=0.3)
        
        # Add statistics
        mean_mag = np.mean(magnitudes)
        max_mag = max(magnitudes)
        ax1.axvline(mean_mag, color='red', linestyle='--', label=f'Mean: {mean_mag:.2f}')
        ax1.axvline(max_mag, color='orange', linestyle='--', label=f'Max: {max_mag:.2f}')
        ax1.legend()
    
    # Depth analysis
    if depths:
        ax2.hist(depths, bins=15, alpha=0.7, color='brown', edgecolor='black')
        ax2.set_title('Depth Distribution')
        ax2.set_xlabel('Depth (km)')
        ax2.set_ylabel('Count')
        ax2.grid(True, alpha=0.3)
        
        # Depth categories
        shallow = sum(1 for d in depths if d <= 10)
        intermediate = sum(1 for d in depths if 10 < d <= 70)
        deep = sum(1 for d in depths if d > 70)
        
        depth_text = f'Shallow (≤10km): {shallow}\n'
        depth_text += f'Intermediate (10-70km): {intermediate}\n'
        depth_text += f'Deep (>70km): {deep}'
        ax2.text(0.65, 0.85, depth_text, transform=ax2.transAxes,
                bbox=dict(boxstyle="round", facecolor='wheat', alpha=0.8))
    
    # Timeline activity
    if times and magnitudes:
        import matplotlib.dates as mdates
        ax3.scatter(times, magnitudes, alpha=0.7, c='green', s=50)
        ax3.set_title('Recent Activity Timeline')
        ax3.set_xlabel('Date/Time')
        ax3.set_ylabel('Magnitude')
        ax3.grid(True, alpha=0.3)
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
    
    # Regional statistics summary
    if magnitudes:
        stats_text = f'📊 {selected_region["name"]} Earthquake Statistics\n\n'
        stats_text += f'Total Events: {len(valid_earthquakes)}\n'
        stats_text += f'Average Magnitude: {np.mean(magnitudes):.2f}\n'
        stats_text += f'Maximum Magnitude: {max(magnitudes):.2f}\n'
        stats_text += f'Minimum Magnitude: {min(magnitudes):.2f}\n'
        stats_text += f'Standard Deviation: {np.std(magnitudes):.2f}\n\n'
        
        # Activity levels
        major = sum(1 for m in magnitudes if m >= 5.0)
        moderate = sum(1 for m in magnitudes if 4.0 <= m < 5.0)
        light = sum(1 for m in magnitudes if 3.0 <= m < 4.0)
        minor = sum(1 for m in magnitudes if m < 3.0)
        
        stats_text += f'Major (M5.0+): {major}\n'
        stats_text += f'Moderate (M4.0-4.9): {moderate}\n'
        stats_text += f'Light (M3.0-3.9): {light}\n'
        stats_text += f'Minor (<M3.0): {minor}'
        
        ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes, fontsize=8,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round", facecolor='lightcyan', alpha=0.8))
        ax4.set_title('Regional Summary')
        ax4.axis('off')
    
    plt.suptitle(f'{selected_region["emoji"]} {selected_region["name"]} Earthquake Analysis', 
                 fontsize=14, y=0.96)
    plt.show()


def main():
    """Main entry point"""
    try:
        earthquake_monitor()
    except KeyboardInterrupt:
        print("\n\n👋 Earthquake monitoring stopped. Stay safe, Henry!")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("Please check your internet connection and try again.")


if __name__ == "__main__":
    main()
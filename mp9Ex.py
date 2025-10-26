import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time


def real_time_data_stream():
    """Enhanced real-time data streaming with multiple data sources"""
    print("🎉 Welcome to Real-Time Data Stream Demo, Henry!")
    print("="*50)
    print("📈 REAL-TIME DATA STREAM")
    print("="*50)
    print("Data Sources:")
    print("1. 🌊 Sine Wave with Noise")
    print("2. 📊 Random Walk")
    print("3. 🔥 Temperature Sensor Simulation")
    print("4. 📡 All Three Combined")
    print("="*50)
    
    # Get user choice
    while True:
        try:
            choice = int(input("Choose data source (1-4): "))
            if 1 <= choice <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Configure based on choice
    if choice == 1:
        stream_sine_wave()
    elif choice == 2:
        stream_random_walk()
    elif choice == 3:
        stream_temperature_sensor()
    elif choice == 4:
        stream_multiple_sources()


def stream_sine_wave():
    """Stream sine wave with realistic noise"""
    print("\n🌊 Streaming Sine Wave with Noise...")
    print("Press Ctrl+C or close window to stop.")
    
    fig, ax = plt.subplots(figsize=(9, 4.5))  # Reduced from (10.8, 5.4)
    
    x_data = []
    y_data = []
    
    def animate(frame):
        current_time = frame * 0.1
        x_data.append(current_time)
        
        # Sine wave with random noise and occasional spikes
        base_signal = np.sin(current_time)
        noise = np.random.normal(0, 0.15)
        spike = 0.5 if np.random.random() < 0.02 else 0  # 2% chance of spike
        
        y_data.append(base_signal + noise + spike)
        
        # Keep rolling window of 100 points
        if len(x_data) > 100:
            x_data.pop(0)
            y_data.pop(0)
        
        ax.clear()
        ax.plot(x_data, y_data, 'b-', linewidth=2, alpha=0.8, label='Signal')
        ax.scatter(x_data[-1:], y_data[-1:], color='red', s=80, zorder=5, label='Current')
        
        # Add signal statistics
        if len(y_data) > 10:
            mean_val = np.mean(y_data[-20:])  # Rolling mean
            std_val = np.std(y_data[-20:])    # Rolling std
            ax.axhline(mean_val, color='green', linestyle='--', alpha=0.7, label=f'Mean: {mean_val:.2f}')
            ax.fill_between(x_data, mean_val - std_val, mean_val + std_val, alpha=0.2, color='green')
        
        ax.set_title('Real-Time Sine Wave Signal', fontsize=14, fontweight='bold')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        # Dynamic scaling
        if len(x_data) > 1:
            ax.set_xlim(min(x_data), max(x_data))
            ax.set_ylim(min(y_data) - 0.5, max(y_data) + 0.5)
    
    anim = FuncAnimation(fig, animate, frames=1000, interval=50, repeat=True)
    plt.tight_layout()
    plt.show()


def stream_random_walk():
    """Stream random walk data"""
    print("\n📊 Streaming Random Walk Data...")
    print("Press Ctrl+C or close window to stop.")
    
    fig, ax = plt.subplots(figsize=(9, 4.5))  # Reduced from (10.8, 5.4)
    
    x_data = []
    y_data = []
    current_value = 0
    
    def animate(frame):
        nonlocal current_value
        
        x_data.append(frame)
        
        # Random walk: small random steps
        step = np.random.normal(0, 0.1)
        current_value += step
        y_data.append(current_value)
        
        # Keep rolling window
        if len(x_data) > 150:
            x_data.pop(0)
            y_data.pop(0)
        
        ax.clear()
        ax.plot(x_data, y_data, 'purple', linewidth=2, alpha=0.8, label='Random Walk')
        ax.scatter(x_data[-1:], y_data[-1:], color='orange', s=80, zorder=5, label='Current Position')
        
        # Add trend line for recent data
        if len(y_data) > 30:
            recent_x = np.array(x_data[-30:])
            recent_y = np.array(y_data[-30:])
            z = np.polyfit(recent_x, recent_y, 1)
            p = np.poly1d(z)
            ax.plot(recent_x, p(recent_x), 'r--', alpha=0.8, label=f'Trend: {z[0]:.3f}')
        
        ax.set_title('Real-Time Random Walk', fontsize=14, fontweight='bold')
        ax.set_xlabel('Step')
        ax.set_ylabel('Position')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        
        if len(x_data) > 1:
            ax.set_xlim(min(x_data), max(x_data))
            ax.set_ylim(min(y_data) - 1, max(y_data) + 1)
    
    anim = FuncAnimation(fig, animate, frames=2000, interval=80, repeat=True)
    plt.tight_layout()
    plt.show()


def stream_temperature_sensor():
    """Stream simulated temperature sensor data"""
    print("\n🔥 Streaming Temperature Sensor Data...")
    print("Press Ctrl+C or close window to stop.")
    
    fig, ax = plt.subplots(figsize=(9, 4.5))  # Reduced from (10.8, 5.4)
    
    x_data = []
    y_data = []
    base_temp = 20.0  # Room temperature
    
    def animate(frame):
        current_time = frame * 0.2
        x_data.append(current_time)
        
        # Simulate daily temperature cycle with noise
        daily_cycle = 5 * np.sin(current_time * 0.1)  # Slow daily variation
        noise = np.random.normal(0, 0.5)  # Sensor noise
        
        # Occasional temperature events
        if np.random.random() < 0.01:  # 1% chance
            event = np.random.choice([-3, 3])  # Heating/cooling event
        else:
            event = 0
        
        temperature = base_temp + daily_cycle + noise + event
        y_data.append(temperature)
        
        # Keep rolling window
        if len(x_data) > 80:
            x_data.pop(0)
            y_data.pop(0)
        
        ax.clear()
        
        # Color-code temperature ranges
        colors = []
        for temp in y_data:
            if temp < 18:
                colors.append('blue')    # Cold
            elif temp > 25:
                colors.append('red')     # Hot
            else:
                colors.append('green')   # Comfortable
        
        ax.scatter(x_data, y_data, c=colors, s=30, alpha=0.7)
        ax.plot(x_data, y_data, 'gray', linewidth=1, alpha=0.5)
        ax.scatter(x_data[-1:], y_data[-1:], color='black', s=100, zorder=5, 
                  label=f'Current: {y_data[-1]:.1f}°C')
        
        # Temperature zones
        ax.axhspan(18, 25, alpha=0.1, color='green', label='Comfort Zone')
        ax.axhspan(15, 18, alpha=0.1, color='blue', label='Cool')
        ax.axhspan(25, 30, alpha=0.1, color='red', label='Warm')
        
        ax.set_title('Real-Time Temperature Monitor', fontsize=14, fontweight='bold')
        ax.set_xlabel('Time (minutes)')
        ax.set_ylabel('Temperature (°C)')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        if len(x_data) > 1:
            ax.set_xlim(min(x_data), max(x_data))
            ax.set_ylim(min(y_data) - 2, max(y_data) + 2)
    
    anim = FuncAnimation(fig, animate, frames=1500, interval=100, repeat=True)
    plt.tight_layout()
    plt.show()


def stream_multiple_sources():
    """Stream multiple data sources in subplots"""
    print("\n📡 Streaming Multiple Data Sources...")
    print("Press Ctrl+C or close window to stop.")
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6))  # Reduced from (9, 7) for laptop
    
    # Data containers
    time_data = []
    sine_data = []
    walk_data = []
    temp_data = []
    
    walk_value = 0
    base_temp = 20.0
    
    def animate(frame):
        nonlocal walk_value
        
        current_time = frame * 0.1
        time_data.append(current_time)
        
        # Generate data for all three sources
        # 1. Sine wave with noise
        sine_val = np.sin(current_time) + np.random.normal(0, 0.1)
        sine_data.append(sine_val)
        
        # 2. Random walk
        walk_value += np.random.normal(0, 0.05)
        walk_data.append(walk_value)
        
        # 3. Temperature
        temp_val = base_temp + 3 * np.sin(current_time * 0.2) + np.random.normal(0, 0.3)
        temp_data.append(temp_val)
        
        # Keep rolling window
        window_size = 100
        if len(time_data) > window_size:
            time_data.pop(0)
            sine_data.pop(0)
            walk_data.pop(0)
            temp_data.pop(0)
        
        # Clear all subplots
        ax1.clear()
        ax2.clear()
        ax3.clear()
        
        # Plot 1: Sine Wave
        ax1.plot(time_data, sine_data, 'b-', linewidth=2, label='Sine Signal')
        ax1.scatter(time_data[-1:], sine_data[-1:], color='red', s=60, zorder=5)
        ax1.set_title('Signal Monitor', fontweight='bold')
        ax1.set_ylabel('Amplitude')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Random Walk
        ax2.plot(time_data, walk_data, 'purple', linewidth=2, label='Random Walk')
        ax2.scatter(time_data[-1:], walk_data[-1:], color='orange', s=60, zorder=5)
        ax2.set_title('Position Tracker', fontweight='bold')
        ax2.set_ylabel('Position')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Temperature
        ax3.plot(time_data, temp_data, 'green', linewidth=2, label='Temperature')
        ax3.scatter(time_data[-1:], temp_data[-1:], color='red', s=60, zorder=5)
        ax3.axhline(20, color='gray', linestyle='--', alpha=0.5, label='Target')
        ax3.set_title('Temperature Monitor', fontweight='bold')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('°C')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Set consistent x-axis
        if len(time_data) > 1:
            for ax in [ax1, ax2, ax3]:
                ax.set_xlim(min(time_data), max(time_data))
    
    anim = FuncAnimation(fig, animate, frames=2000, interval=75, repeat=True)
    plt.tight_layout()
    plt.show()


def main():
    """Main entry point"""
    try:
        real_time_data_stream()
    except KeyboardInterrupt:
        print("\n\n👋 Stream stopped. Thanks for watching the data, Henry!")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("Please try again.")


if __name__ == "__main__":
    main()
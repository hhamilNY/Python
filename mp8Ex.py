import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def main_menu():
    """Display the main menu and get user choice"""
    print("\n" + "="*40)
    print("🎨 INTERACTIVE MATPLOTLIB DEMO")
    print("="*40)
    print("1. 📊 Interactive Plots")
    print("2. 🎬 Animated Wave")
    print("3. 🎯 Click Plot")
    print("4. 📈 Real-time Data Stream")
    print("5. 🎨 Custom Function")
    print("6. 🎮 Subplot Grid")
    print("7. 🔢 Distribution Explorer")
    print("0. ❌ Exit")
    print("="*40)
    
    while True:
        try:
            choice = int(input("Enter choice (0-7): "))
            if 0 <= choice <= 7:
                return choice
            else:
                print("Please enter a number between 0 and 7.")
        except ValueError:
            print("Please enter a valid number.")


def interactive_plots():
    """Create plots with user customization"""
    print("\n📊 Creating Interactive Plots...")
    
    plot_type = input("Choose plot type (sine/cosine/both) [both]: ").lower() or "both"
    
    colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33F5']
    x = np.linspace(0, 4*np.pi, 500)
    
    fig, ax = plt.subplots(figsize=(7.5, 4.5))  # Reduced from (10, 6)
    
    if plot_type in ['sine', 'both']:
        ax.plot(x, np.sin(x), label='Sine Wave', color=colors[0], linewidth=2)
    
    if plot_type in ['cosine', 'both']:
        ax.plot(x, np.cos(x), label='Cosine Wave', color=colors[1], linewidth=2)
    
    ax.set_title(f'Interactive {plot_type.title()} Plot', fontsize=14)
    ax.set_xlabel('X Values')
    ax.set_ylabel('Y Values')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()


def animated_wave():
    """Create an animated wave"""
    print("\n🎬 Creating Animated Wave...")
    
    fig, ax = plt.subplots(figsize=(7.5, 4.5))  # Reduced from (10, 6)
    x = np.linspace(0, 4*np.pi, 500)
    line, = ax.plot([], [], 'b-', linewidth=2)
    
    ax.set_xlim(0, 4*np.pi)
    ax.set_ylim(-2, 2)
    ax.set_title('Animated Sine Wave')
    ax.grid(True, alpha=0.3)
    
    def animate(frame):
        y = np.sin(x + frame * 0.1)
        line.set_data(x, y)
        return line,
    
    anim = FuncAnimation(fig, animate, frames=100, interval=50, repeat=True)
    plt.show()


def click_plot():
    """Create a plot where users can click to add points"""
    print("\n🎯 Click Plot - Click to add points!")
    
    fig, ax = plt.subplots(figsize=(6, 4.5))  # Reduced from (8, 6)
    points_x, points_y = [], []
    
    def on_click(event):
        if event.inaxes != ax:
            return
        points_x.append(event.xdata)
        points_y.append(event.ydata)
        ax.clear()
        ax.scatter(points_x, points_y, c='red', s=50)
        if len(points_x) > 1:
            ax.plot(points_x, points_y, 'b--', alpha=0.5)
        ax.set_title(f'Click Plot - {len(points_x)} points')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.grid(True, alpha=0.3)
        plt.draw()
    
    fig.canvas.mpl_connect('button_press_event', on_click)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title('Click anywhere to add points!')
    ax.grid(True, alpha=0.3)
    plt.show()


def real_time_data_stream():
    """Simulate real-time data streaming"""
    print("\n📈 Real-time Data Stream...")
    print("Watch live data updates! Press Ctrl+C or close window to stop.")
    
    fig, ax = plt.subplots(figsize=(9, 4.5))  # Reduced from (12, 6)
    
    x_data = []
    y_data = []
    
    def animate(frame):
        # Simulate real-time data with some noise
        x_data.append(frame * 0.1)
        y_data.append(np.sin(frame * 0.1) + np.random.normal(0, 0.2))
        
        # Keep only last 50 points for better visualization
        if len(x_data) > 50:
            x_data.pop(0)
            y_data.pop(0)
        
        ax.clear()
        ax.plot(x_data, y_data, 'g-', linewidth=2, label='Live Data')
        ax.scatter(x_data[-1:], y_data[-1:], color='red', s=100, zorder=5)
        
        ax.set_title('Real-time Data Stream', fontsize=14)
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Dynamic axis scaling
        if len(x_data) > 1:
            ax.set_xlim(min(x_data) - 0.5, max(x_data) + 0.5)
            ax.set_ylim(min(y_data) - 0.5, max(y_data) + 0.5)
    
    anim = FuncAnimation(fig, animate, frames=500, interval=100, repeat=True)
    plt.show()


def custom_function():
    """Allow user to plot custom functions"""
    print("\n🎨 Custom Function Plotter")
    print("Examples: sin(x), x**2, exp(-x), cos(2*x)")
    
    try:
        func_str = input("Enter function: ")
        x = np.linspace(-5, 5, 500)
        
        safe_dict = {
            'x': x, 'sin': np.sin, 'cos': np.cos, 'exp': np.exp,
            'log': np.log, 'sqrt': np.sqrt, 'pi': np.pi
        }
        
        y = eval(func_str, {"__builtins__": {}}, safe_dict)
        
        plt.figure(figsize=(6, 4.5))  # Reduced from (8, 6)
        plt.plot(x, y, linewidth=2, label=f'y = {func_str}')
        plt.title(f'y = {func_str}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
        
    except Exception as e:
        print(f"Error: {e}")


def subplot_grid():
    """Create subplot grid"""
    print("\n🎮 Subplot Grid")
    
    fig, axes = plt.subplots(2, 2, figsize=(7.5, 6))  # Reduced from (10, 8)
    x = np.linspace(0, 10, 100)
    
    functions = [
        (np.sin(x), "Sine", "#FF5733"),
        (np.cos(x), "Cosine", "#33FF57"),
        (x**2/20, "Quadratic", "#3357FF"),
        (np.exp(-x/3), "Exponential", "#FF33F5")
    ]
    
    for i, (y, name, color) in enumerate(functions):
        row, col = i // 2, i % 2
        axes[row, col].plot(x, y, color=color, linewidth=2)
        axes[row, col].set_title(name)
        axes[row, col].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def distribution_explorer():
    """Explore statistical distributions"""
    print("\n🔢 Distribution Explorer")
    
    distributions = {
        '1': ('Normal', lambda: np.random.normal(0, 1, 1000)),
        '2': ('Uniform', lambda: np.random.uniform(-3, 3, 1000)),
        '3': ('Exponential', lambda: np.random.exponential(1, 1000))
    }
    
    print("1. Normal  2. Uniform  3. Exponential")
    choice = input("Choose (1-3): ")
    
    if choice in distributions:
        name, generator = distributions[choice]
        data = generator()
        
        plt.figure(figsize=(7.5, 4.5))  # Reduced from (10, 6)
        plt.hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title(f'{name} Distribution')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        plt.show()


def main():
    """Main program loop"""
    print("🎉 Welcome to Interactive Matplotlib Demo, Henry!")
    
    while True:
        choice = main_menu()
        
        if choice == 0:
            print("\n👋 Goodbye!")
            break
        elif choice == 1:
            interactive_plots()
        elif choice == 2:
            animated_wave()
        elif choice == 3:
            click_plot()
        elif choice == 4:
            real_time_data_stream()
        elif choice == 5:
            custom_function()
        elif choice == 6:
            subplot_grid()
        elif choice == 7:
            distribution_explorer()
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
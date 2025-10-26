import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np  


# Figure = The entire canvas 
# Axes = A part of the figure where data is plotted (a plot or graph)
# Axis = The x-axis and y-axis of the plot     

# Create a figure and axis
fig, ax = plt.subplots(nrows=2,   # number of rows
                       ncols=2)   # number of columns
# Create data for plotting

x = np.linspace(0, 10, 100)  # 100 points from 0 to 10
y = np.sin(x)                 # Sine of each x point

# Plot data on the first subplot (top-left)
ax[0, 0].plot(x, y, label="Sine Wave", color="#FF5733")  # Plot sine wave
# Customize the first subplot
ax[0, 0].set_title("Sine Wave Plot")  # Set the title of the axes
ax[0, 0].set_xlabel("X-axis Label")   # Set the x-axis label
ax[0, 0].set_ylabel("Y-axis Label")   # Set the y-axis label
ax[0, 0].legend()                    # Show legend

# Let's add plots to the other subplots as well
# Top-right: Cosine wave
y2 = np.cos(x)
ax[0, 1].plot(x, y2, label="Cosine Wave", color="#33FF57")
ax[0, 1].set_title("Cosine Wave Plot")
ax[0, 1].set_xlabel("X-axis Label")
ax[0, 1].set_ylabel("Y-axis Label")
ax[0, 1].legend()

# Bottom-left: Quadratic function
y3 = x**2
ax[1, 0].plot(x, y3, label="Quadratic", color="#3357FF")
ax[1, 0].set_title("Quadratic Function")
ax[1, 0].set_xlabel("X-axis Label")
ax[1, 0].set_ylabel("Y-axis Label")
ax[1, 0].legend()

# Bottom-right: Exponential decay
y4 = np.exp(-x/3)
ax[1, 1].plot(x, y4, label="Exponential Decay", color="#FF33F5")
ax[1, 1].set_title("Exponential Decay")
ax[1, 1].set_xlabel("X-axis Label")
ax[1, 1].set_ylabel("Y-axis Label")
ax[1, 1].legend()

# Adjust layout to prevent overlapping
plt.tight_layout()

# Save the plot instead of showing it
plt.savefig('matplotlib_example.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'matplotlib_example.png'")

# Show the plot
#plt.show()

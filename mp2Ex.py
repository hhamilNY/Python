import matplotlib.pyplot as plt
import numpy as np  

#grid() function = Adds grid lines to the plot for better readability and visualization of data points.

# Create a simple plot
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])
plt.grid(axis="y", # both or x ``
         linewidth=2,  # Set the width of the grid lines
         linestyle="--",  # Dashed lines  dasdot, dashed
         color="0.95")  # Light gray grid lines for x-axis
plt.plot(x, y)
plt.show()
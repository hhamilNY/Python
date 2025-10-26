import matplotlib.pyplot as plt
import numpy as np  

# scatter graph = Show the relationship between two variables
#                 Helps to idetify a correlation (+, -, None)

# Create data for the scatter plot  
#x = np.array([1, 2, 3, 4, 5])
#y = np.array([2, 3, 5, 7, 11]) 
# Using random data points for scatter plot
np.random.seed(0)  # For reproducibility
x = np.random.rand(35)
y = np.random.rand(35)  
np.random.seed(1)  # For reproducibility
x2 = np.random.rand(20)
y2 = np.random.rand(20)

# Create a scatter plot
plt.scatter(x, y, 
            color="#FF5733",   # Set the color of the points
            marker="o",          # Circle marker
            s=100,               # Size of the points
            alpha=0.7,           # Transparency of the points
            edgecolors="black",  # Border color of the points
            label= "Class A")    # Label for legend
plt.scatter(x2, y2, 
            color="#7E33FF",   # Set the color of the points
            marker="o",          # Circle marker
            s=100,               # Size of the points
            alpha=0.7,           # Transparency of the points
            edgecolors="black",   # Border color of the points
            label= "Class B")    # Label for legend


plt.title("Scatter Plot Example")
plt.xlabel("X-axis Label")
plt.ylabel("Y-axis Label")
plt.legend()
plt.show()

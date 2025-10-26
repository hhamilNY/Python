import matplotlib.pyplot as plt
import numpy as np  

# Histogram = A visual representation of the distribution of numerical data.    
#             It divides the data into bins and shows the frequency of data points in each bin.
# Create data for the histogram
#data = np.random.randn(1000)  # Generate 1000 random data points from a normal distribution 
# Using random data points for histogram
np.random.seed(0)  # For reproducibility
data = np.random.normal(loc=80, scale=1, size=1000)  # Mean=0, StdDev=1, 1000 points  
# Create a histogram
plt.hist(data,
            bins=30,                # Number of bins
            color="#3498DB",      # Color of the bars
            edgecolor="black",      # Color of the bar edges
            alpha=0.7)              # Transparency of the bars
plt.title("Histogram Example")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()

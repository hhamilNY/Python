import matplotlib.pyplot as plt
import numpy as np  


# Bar Chart = Circular chart into slices to show percentages of the total.
#              Good for visualizing distribution among categories.


# Create data for the pie chart
categories = "Freshmen", "Sophomores", "Juniors", "Seniors"
values = np.array([50, 30, 15, 5]) 
#can replace color list in the plt.pie() function call
#colors = ["#FF9999", "#66B3FF", "#99FF99", "#FFCC99"]   
# Create a pie chart
plt.pie(values, 
        labels=categories, 
        autopct="%1.1f%%",  # Display percentage on each slice
        startangle=180,     # Rotate the start of the pie chart
        colors=["#FF9999", "#66B3FF", "#99FF99", "#FFCC99"],
        shadow=True,
        explode=(0, 0, 0.1, 0))  # Custom colors for each slice


plt.title("Student Distribution by Class Year")
# plt.show()  # Comment out for auto-close option
plt.show(block=False)  # Non-blocking show
plt.pause(5)  # Display for 5 seconds
plt.close()  # Auto-close after 5 seconds

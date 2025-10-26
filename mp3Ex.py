import matplotlib.pyplot as plt
import numpy as np  

# Bar chart = A graphical representation of data using rectangular bars to show the frequency or value of different categories.


# Create data for the bar chart
categories = ["Grain", "Vegetables", "Fruits", "Dairy", "Meat"]
values = [10, 15, 7, 12, 5]
# Create a bar chart
#plt.bar(categories, values, color=["#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#8E44AD"])  
plt.barh(categories, values, color=["#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#8E44AD"])          


plt.title("Food Categories Bar Chart")  
plt.xlabel("Food Categories")
plt.ylabel("Values")
plt.show()


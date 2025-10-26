import numpy as np 
import sys
from zipfile import PyZipFile 
from timeit import timeit 

line_break: str = "*" * 20
print(line_break)

print(f'{np.__version__  = }')

my_list: list[int] = [1,2,3,4,5]

print()
print(my_list)
print(line_break)

my_list = my_list * 2  

print()
print(my_list)
print(line_break)

arr = np.array([1,2,3,4,5])

print(arr)
print(type(arr)) 
print(line_break)

arr2 = arr * 2

print()
print(arr2) 
print(f'Array multiplied by 2: {arr2}')
print(line_break)

array = np.array(['A'])

print()
print(array) 
print(type(array))
print (f'{array.ndim =}')
print (f'{array.shape = }')
print(line_break)


array2 = np.array([['A','B','C'], ['D','E','F']])

print()
print(array2)
print(type(array2))
print (f'{array2.ndim =}')
print (f'{array2.shape = }')
print(line_break)


array3 = np.array([[[1,2,3], [4,5,6]], [[7,8,9], [10,11,12]]])

print()
print(array3)
print(type(array3))  
print (f'{array3.ndim = }')
print(f'{array3.shape = }')
print(line_break)

#numpy arrays need to be balanced in terms of number of elements in each dimension, otherwise it wiil create an error()

array4 = np.array([[['A', 'B', 'C',], ['D', 'E', 'F'], ['G', 'H', 'I']],
                   [['J', 'K', 'L'], ['M', 'N', 'O'], ['P', 'Q', 'R']],
                   [['S', 'T', 'U'], ['V', 'W', 'X'], ['Y', 'Z', '0']]] )  

print()
print(array4)
print(type(array4))
print (f'{array4.ndim = }')
print (f'{array4.shape = }')
print(line_break)

# Multidimensional array indexing is faster than chain indexing


# chain indexing
print(f'{array4[1][2][0] = }')

# single indexing
print(f'{array4[1,2,0] = }')

# Performance comparison between list and numpy array multiplication
# globals() was used to resolve  NameError. The issue is in the timeit performance comparison section. The timeit function creates its own execution context, so it can't see the my_list variable that's defined in the global scope 

print(line_break)
print("Performance comparison with SMALL arrays (5 elements):")
print("List vs NumPy - multiplication by 2")
list_time_small = timeit(stmt="[x * 2 for x in my_list]", globals=globals(), number=100_000)
numpy_time_small = timeit(stmt="arr * 2", globals=globals(), number=100_000)
print(f"Small list multiplication time: {list_time_small:.5f} seconds")
print(f"Small numpy array multiplication time: {numpy_time_small:.5f} seconds")
print(f"Speedup factor: {list_time_small/numpy_time_small:.2f}x")
print(line_break)

# Create large datasets for performance comparison
print("Creating large datasets (1 million elements)...")
large_list = list(range(1_000_000))
large_numpy_array = np.array(large_list)
print(f"Large list size: {len(large_list):,} elements")
print(f"Large numpy array shape: {large_numpy_array.shape}")
print(line_break)

print("Performance comparison with LARGE arrays (1 million elements):")
print("List vs NumPy - multiplication by 2")
large_list_time = timeit(stmt="[x * 2 for x in large_list]", globals=globals(), number=10)
large_numpy_time = timeit(stmt="large_numpy_array * 2", globals=globals(), number=10)
print(f"Large list multiplication time: {large_list_time:.5f} seconds")
print(f"Large numpy array multiplication time: {large_numpy_time:.5f} seconds")
print(f"NumPy speedup factor: {large_list_time/large_numpy_time:.2f}x")
print(line_break)

print("Memory usage comparison:")
import sys
list_memory = sys.getsizeof(large_list) + sum(sys.getsizeof(x) for x in large_list)
numpy_memory = large_numpy_array.nbytes
print(f"Large list memory usage: {list_memory:,} bytes ({list_memory/1024/1024:.2f} MB)")
print(f"Large numpy array memory usage: {numpy_memory:,} bytes ({numpy_memory/1024/1024:.2f} MB)")
print(f"Memory efficiency: {list_memory/numpy_memory:.2f}x less memory with NumPy")
print(line_break)

# Creating a Zip file using numpy's PyZipFile
zip_filename = 'example.zip'
with PyZipFile(zip_filename, 'w') as zip_file:
    zip_file.write('numpyEx.py')    
print(f'Created zip file: {zip_filename}')
print(line_break)

print("Contents of the created zip file:")
with PyZipFile(zip_filename, 'r') as zip_file:
    zip_file.printdir()
print(line_break)
# Clean up the created zip file
import os
os.remove(zip_filename)
print(f'Removed zip file: {zip_filename}')
print(line_break)



# slicing
# array[start:stop:step]


print("Slicing examples:")

# 1D array slicing
print("1D array slicing:")
print(f'{array[1:4] = }')
print(f'{array[:3] = }')
print(f'{array[-2:] = }')
print(line_break)

# 2D array slicing
print("2D array slicing:")
print(f'{array2[0, 1] = }')
print(f'{array2[1, :] = }')
print(f'{array2[:, 2] = }')
print(line_break)

# 3D array slicing
print("3D array slicing:")
print(f'{array3[0, 1, 2] = }')
print(f'{array3[1, :, :] = }')
print(f'{array3[:, 0, :] = }')
print(line_break)

# column slicing in 2D array

print(f'{array2 = }')

print("Column slicing in 2D array:")
print(f'{array2[:, 0] = }')
print(f'{array2[:, 1] = }')
print(f'{array2[:, 2] = }') 
print(line_break)
print()

print(f' column slicing with step:')
print(f'{array2[:, ::2] = }')


# column slicing in 2D array
print(line_break)

t_array: np.ndarray = np.array([ [10,   20,  30, 40],
                                 [50,   60,  70, 80],
                                 [90,  100, 110, 120],
                                 [130, 140, 150, 160]])

print(f'{t_array = }')
print("Column slicing with step in 2D array:")
print(f'{t_array[:, ::2] = }')      # every second column
print(f'{t_array[::2, :] = }')      # every second row
print(f'{t_array[1::2, 1::2] = }')  # every second row and column starting from index 1

print(line_break)
print()
# reverse slicing
print("Reverse slicing:")
print(f'{t_array[::-1, ::-1] = }')  # reverse all rows and columns
print(f'{t_array[::-1, :] = }')      # reverse all rows
print(f'{t_array[:, ::-1] = }')      # reverse all columns


scores = np.array([85, 90, 78, 100, 64, 91] )
print(line_break)
print("Original scores array:")
print(f'{scores = }')       
print(f'Highest score: {np.max(scores)}')
print(f'Lowest score: {np.min(scores)}')
print(f'Average score: {np.mean(scores)}')
print(f'Standard deviation: {np.std(scores)}')

#Comparison operators

print(line_break)
print("Comparison operators on numpy arrays:")
print(f'{scores = }')
print(f'Scores greater than 80: {scores > 80}')
print(f'Scores equal to 100: {scores == 100}')
print(f'Scores less than 70: {scores < 70}')
print(f'Scores not equal to 90: {scores != 90}')
print(line_break)

results = scores >= 90
print("Scores greater than or equal to 90:")
print(f'{results = }')

# astype() method returns a new array with the same data but with the specified data type

binary_results = results.astype(int)   
print("Converted boolean results to integers:")
print(f'{binary_results = }')

print("Original scores array:")
print(f'{scores = }')  
scores[scores < 70] = 0
print("Scores after setting scores less than 70 to 0:")
print(f'{scores = }')

print(line_break)


# Broadcasting allows NumPy to perform operations on arrays with different shapes by virtually expanding the smaller array to match the shape of the larger one without actually copying data.

# The dimensions have the same size 
# or 
# one of them is 1

# Example of broadcasting
print("Broadcasting example:")
array_a = np.array([[1, 2, 3],
                    [4, 5, 6]])
array_b = np.array([[10],
                    [20]])
result = array_a + array_b

print(f'Array A:\n{array_a}')
print(f'{array_a.shape = }')
print(f'Array B:\n{array_b}')
print(f'{array_b.shape = }')
print(f'Result:\n{result}')
print(f'{result.shape = }')
print()
print(line_break)

# broadcasting  3 x 2  and 2 x 3  => 2 x 2 example
array_c = np.array([[1, 2],
                    [3, 4],
                    [5, 6]])
array_d = np.array([[10, 20, 30],
                    [40, 50, 60]])
result2 = array_c + array_d.T  # Transpose array_d to make shapes compatible
print()
print(f'Array C:\n{array_c}')
print(f'{array_c.shape = }')
print()
print(f'Array D (transposed):\n{array_d.T}')
print(f'{array_d.T.shape = }')  
print(f'Result 2:\n{result2}')
print(f'{result2.shape = }')
print()
print(line_break)

# Broadcasting with different shapes example
array_e = np.array([[1, 2, 3],
                    [4, 5, 6]])
array_f = np.array([[10],
                    [20]])
result3 = array_e + array_f

print(f'Array E:\n{array_e}')
print(f'{array_e.shape = }')
print(f'Array F:\n{array_f}')
print(f'{array_f.shape = }')
print(f'Result 3:\n{result3}')
print(f'{result3.shape = }')
print()


#Broadcasting 1 X 10 array with 10 X 1 array
array_g = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
array_h = np.array([[10],   
                    [20],
                    [30],
                    [40],
                    [50],
                    [60],
                    [70],
                    [80],
                    [90],
                    [100]])
result4 = array_g + array_h
print()
print(f'Array G:\n{array_g}')
print(f'{array_g.shape = }')
print(f'Array H:\n{array_h}')
print(f'{array_h.shape = }')
print(f'Result 4:\n{result4}')
print(f'{result4.shape = }')
print()
print(line_break)  

#Broadcasting 1 X 10 array   multiply 10 X 1 array range(1, 11)
array_i = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
array_j = np.array([[1],
                    [2],
                    [3],
                    [4],
                    [5],
                    [6],
                    [7],
                    [8],
                    [9],
                    [10]])
result5 = array_i * array_j
print()
print(f'Array I:\n{array_i}')
print(f'{array_i.shape = }')
print(f'Array J:\n{array_j}')
print(f'{array_j.shape = }')
print(f'Result 5:\n{result5}')
print(f'{result5.shape = }')
print()
print(line_break)



# numpy matrix multiplication using matmul() 3 x 2  and 2 x 3  => 3 x 3 example
array_k = np.array([[1, 2],
                    [3, 4],
                    [5, 6]])    
array_l = np.array([[10, 20, 30],
                    [40, 50, 60]])  
result6 = np.matmul(array_k, array_l)

print(f'Array K:\n{array_k}')
print(f'{array_k.shape = }')
print(f'Array L:\n{array_l}')
print(f'{array_l.shape = }')
print(f'Result 6:\n{result6}')
print(f'{result6.shape = }')
print()
print(line_break)




# numpy aggregate  
# Aggregate functions = summarize data and typically
#  return a single value


print("Numpy aggregate functions:")
data = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])
print()        
print(f'{data = }')
print(f'Sum of all elements: {np.sum(data)}')
print(f'Sum of each column (axis=0): {np.sum(data, axis=0)}')
print(f'Sum of each row (axis=1): {np.sum(data, axis=1)}')

print(f'Mean of all elements: {np.mean(data)}')
print(f'Minimum element: {np.min(data)}')
print(f'Minimum position (np.argmin(data)): {np.argmin(data)}') 
print(f'Maximum element: {np.max(data)}')
print(f'Maximum position (np.argmax(data)): {np.argmax(data)}') 
print(f'Standard deviation: {np.std(data)}')
print(f'Variance: {np.var(data)}')
print()
print(line_break)


# NumPY Filtering
print("NumPy Filtering example:")
data2 = np.array([[10, 15, 20, 25, 30, 100, 40],
                    [45, 14, 37, 60, 65, 17, 75],
                    [80, 85, 18, 95, 35, 105, 110]])
print()
print(f'{data2 = }')
print()
teens = data2[data2 < 18]
print("Filtered elements less than 18:")
print(f'{teens = }')
print()
adults = data2[(data2 >= 18) & (data2 < 65)]
print("Filtered elements between 18 and 64:")
print(f'{adults = }')
seniors = data2[data2 >= 65]
print()
print("Filtered elements 65 and older:")
print(f'{seniors = }')
print()
print(line_break)

# NumPy filtering odd using data2   
print()
print("NumPy Filtering odd numbers example:")
odds = data2[data2 % 2 == 1]
print(f'{odds = }')         
print("End of numpyEx.py")

# NumPy filtering even using data2 
print()
print("NumPy Filtering even numbers example:")
evens = data2[data2 % 2 == 0]
print(f'{evens = }')

# NumPy filtering  where values are less than 18 and replace with Zero
print()
print(f'{data2 = }')
print()
print()
print("NumPy Filtering and replacing values less than 18 with Zero:")
modified_data = np.where(data2 >= 18, data2, 0)
print(f'{modified_data = }')    
print()
print(line_break)


print("End of numpyEx.py")


# End of numpyEx.py
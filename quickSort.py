def lomuto_partition(arr, low, high):
    pivot = arr[high]  # Pivot is the last element
    i = low - 1        # i starts before the low index

    for j in range(low, high):
        if arr[j] < pivot:       # Strictly less than pivot
            i += 1               # Move i forward only if condition is met
            arr[i], arr[j] = arr[j], arr[i]  # Swap arr[i] and arr[j]
            print(f'Swapped {arr[i]} and {arr[j]}: {arr}')  # Debug statement
    # Place pivot in its correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1  # Return pivot index


def quicksort(arr, low, high):
    if low < high:
        pi = lomuto_partition(arr, low, high)
        quicksort(arr, low, pi - 1)   # Left side
        quicksort(arr, pi + 1, high)  # Right side


# Example
line_break: str = '-' * 40
print(line_break)
arr = [7, 2, 4, 9, 3, 1, 8, 6, 5]
print(arr)
print(line_break)
quicksort(arr, 0, len(arr) - 1)
print(arr)
print(line_break)

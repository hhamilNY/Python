def merge_sort(arr):
    # Base case: arrays with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr

    # Find the midpoint to split the array
    mid = len(arr) // 2

    # Recursively split and sort the left half
    left_half = merge_sort(arr[:mid])
    print(f' {left_half =}  {mid =}')
    # Recursively split and sort the right half
    right_half = merge_sort(arr[mid:])
    print(f' {right_half =}  {mid =}')
    # Merge the sorted halves and return
    return merge(left_half, right_half)

def merge(left, right):
    sorted_array = []
    i = j = 0

    # Compare elements from left and right arrays one by one
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_array.append(left[i])
            i += 1
        else:
            sorted_array.append(right[j])
            j += 1

    # Append any remaining elements from left or right
    sorted_array.extend(left[i:])
    sorted_array.extend(right[j:])
    return sorted_array



# Example
line_break: str = '-' * 40
print(line_break)
arr = [7, 2, 4, 9, 3, 1, 8, 6, 5]
print(arr)
print(line_break)
arr = merge_sort(arr)
print(arr)
print(line_break)
"""
Sample code snippets for testing the Time Complexity Estimator
"""

# Sample 1: Binary Search - O(log n)
BINARY_SEARCH = """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
"""

# Sample 2: Bubble Sort - O(n²)
BUBBLE_SORT = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
"""

# Sample 3: Factorial (Recursive) - O(n) time, O(n) space
FACTORIAL_RECURSIVE = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""

# Sample 4: Fibonacci (Naive) - O(2^n)
FIBONACCI_NAIVE = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
"""

# Sample 5: Linear Search - O(n)
LINEAR_SEARCH = """
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
"""

# Sample 6: Merge Sort - O(n log n)
MERGE_SORT = """
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
"""

# Expected outputs for testing
EXPECTED_OUTPUTS = {
    'binary_search': {
        'time_complexity': 'O(log n)',
        'space_complexity': 'O(1)',
        'analysis_keywords': ['logarithmic', 'divide', 'conquer', 'search space']
    },
    'bubble_sort': {
        'time_complexity': 'O(n²)',
        'space_complexity': 'O(1)',
        'analysis_keywords': ['quadratic', 'nested loops', 'comparisons']
    },
    'factorial_recursive': {
        'time_complexity': 'O(n)',
        'space_complexity': 'O(n)',
        'analysis_keywords': ['recursive', 'call stack', 'linear']
    },
    'fibonacci_naive': {
        'time_complexity': 'O(2^n)',
        'space_complexity': 'O(n)',
        'analysis_keywords': ['exponential', 'overlapping subproblems', 'recursive']
    },
    'linear_search': {
        'time_complexity': 'O(n)',
        'space_complexity': 'O(1)',
        'analysis_keywords': ['linear', 'sequential', 'worst case']
    },
    'merge_sort': {
        'time_complexity': 'O(n log n)',
        'space_complexity': 'O(n)',
        'analysis_keywords': ['divide and conquer', 'recursive', 'merge']
    }
}

if __name__ == "__main__":
    print("Sample code snippets for Time Complexity Estimator testing:")
    print("\n1. Binary Search:", BINARY_SEARCH)
    print("\n2. Bubble Sort:", BUBBLE_SORT)
    print("\n3. Factorial (Recursive):", FACTORIAL_RECURSIVE)
    print("\n4. Fibonacci (Naive):", FIBONACCI_NAIVE)
    print("\n5. Linear Search:", LINEAR_SEARCH)
    print("\n6. Merge Sort:", MERGE_SORT)
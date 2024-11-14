# O(log n) Логарифмическая сложность алгоритма
# arr отсортирован
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
print(binary_search(arr, 70))  # выведет 6
print(binary_search(arr, 25))  # выведет -1

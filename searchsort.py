def binary_search(value, data):
    return _binary_search(value, data, 0, len(data))

def _binary_search(value, data, start, end):
    if start < end:
        mid = (start + end) // 2
        if data[mid] == value:
            return mid
        elif data[mid] > value:
            return _binary_search(value, data, start, mid)
        else:
            return _binary_search(value, data, mid + 1, end)


def bubble_sort(data):
    """sort the data in place. Return the number of comparisons"""
    is_sorted = False
    comparisons = 0
    sorted_region = 0
    while not is_sorted:
        is_sorted = True
        sorted_region += 1
        for i in range(len(data) - sorted_region):
            comparisons += 1
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                is_sorted = False
    return comparisons


def shuttle_sort(data):
    """sort the data in place. Return the number of comparisons
    This differs from the bubble sort in that the 'bubbling happens
    in both directions."""
    is_sorted = False
    comparisons = 0
    sorted_region = 0
    while not is_sorted:
        is_sorted = True
        sorted_region += 1
        for i in range(sorted_region-1, len(data) - sorted_region):
            comparisons += 1
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                is_sorted = False
        if is_sorted:
            break
        for i in range(len(data) - sorted_region-1, sorted_region-1, -1):
            comparisons += 1
            if data[i - 1] > data[i]:
                data[i - 1], data[i] = data[i], data[i - 1]
                is_sorted = False
    return comparisons


def quick_sort(data):
    return _quick_sort(data, 0, len(data), comparisons=0)


def _quick_sort(data, start, end, comparisons):
    if start < end:
        p, comparisons = _partition(data, start, end, comparisons)
        comparisons = _quick_sort(data, start, p, comparisons)
        comparisons = _quick_sort(data, p + 1, end, comparisons)
    return comparisons


def _partition(data, start, end, comparisons):
    # choose pivot
    pivot = data[(start + end) // 2]
    i = start - 1
    for j in range(start, end - 1):
        comparisons += 1
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
    data[i + 1], data[end - 1] = data[end - 1], data[i + 1]
    return i + 1, comparisons


def test():
    test_list = [5, 2, 8, 7, 9, 5, 6, 4, 3, 2, 4, 5, 6, 7, 8, 9, 2, 6,
                 5, 6, 7, 8, 9, 7, 5, 5, 6, 5, 4, 3, 2, 3, 7, 5, 6, 5, 1, 9, 7]
    print("bubble", bubble_sort(test_list), test_list)
    test_list = [5, 2, 8, 7, 9, 5, 6, 4, 3, 2, 4, 5, 6, 7, 8, 9, 2, 6,
                 5, 6, 7, 8, 9, 7, 5, 5, 6, 5, 4, 3, 2, 3, 7, 5, 6, 5, 1, 9, 7]
    print("shuttle", shuttle_sort(test_list), test_list)
    test_list = [5, 2, 8, 7, 9, 5, 6, 4, 3, 2, 4, 5, 6, 7, 8, 9, 2, 6,
                 5, 6, 7, 8, 9, 7, 5, 5, 6, 5, 4, 3, 2, 3, 7, 5, 6, 5, 1, 9, 7]
    print("quick", quick_sort(test_list), test_list)

    search_list = [2, 4, 5, 7, 9, 11, 15, 19, 23]
    print("find 7", binary_search(7, search_list))
    print("don't find 16", binary_search(16, search_list))
test()

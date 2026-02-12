"""Custom sorting and searching algorithms + benchmarks."""

from __future__ import annotations

import timeit
from collections.abc import Callable
from typing import Any


def merge_sort(data: list[Any], key: Callable = lambda x: x) -> list[Any]:
    """Sort using merge sort (O(n log n) time, O(n) space)."""
    if len(data) <= 1:
        return list(data)
    mid = len(data) // 2
    left = merge_sort(data[:mid], key=key)
    right = merge_sort(data[mid:], key=key)
    return _merge(left, right, key=key)


def _merge(left: list[Any], right: list[Any], key: Callable) -> list[Any]:
    result: list[Any] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def insertion_sort(data: list[Any], key: Callable = lambda x: x) -> list[Any]:
    """Insertion sort (O(n^2) avg/worst, O(n) best if already sorted)."""
    arr = list(data)
    for i in range(1, len(arr)):
        current = arr[i]
        current_key = key(current)
        j = i - 1
        while j >= 0 and key(arr[j]) > current_key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr


def binary_search(sorted_data: list[Any], target: Any, key: Callable = lambda x: x) -> int | None:
    """Binary search on sorted_data (O(log n)). Returns index or None."""
    low, high = 0, len(sorted_data) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = key(sorted_data[mid])
        if mid_val == target:
            return mid
        if mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return None


def linear_search(data: list[Any], target: Any, key: Callable = lambda x: x) -> int | None:
    """Linear scan (O(n)). Returns index or None."""
    for i, item in enumerate(data):
        if key(item) == target:
            return i
    return None


def benchmark_sort(data: list[Any], key: Callable = lambda x: x, repeats: int = 5) -> dict[str, float]:
    """Compare merge_sort and insertion_sort vs built-in sorted()."""
    t_merge = timeit.timeit(lambda: merge_sort(data, key=key), number=repeats)
    t_insert = timeit.timeit(lambda: insertion_sort(data, key=key), number=repeats)
    t_builtin = timeit.timeit(lambda: sorted(data, key=key), number=repeats)
    return {
        "merge_sort_ms": round(t_merge / repeats * 1000, 3),
        "insertion_sort_ms": round(t_insert / repeats * 1000, 3),
        "builtin_sorted_ms": round(t_builtin / repeats * 1000, 3),
    }


def benchmark_search(data: list[Any], target: Any, key: Callable = lambda x: x, repeats: int = 5) -> dict[str, float]:
    """Compare binary_search vs linear_search vs `target in ...` (using keys).

    Assumes *data* is already sorted by *key* for binary_search.
    """
    t_bin = timeit.timeit(lambda: binary_search(data, target, key=key), number=repeats)
    t_lin = timeit.timeit(lambda: linear_search(data, target, key=key), number=repeats)
    t_in = timeit.timeit(lambda: any(key(x) == target for x in data), number=repeats)
    return {
        "binary_search_ms": round(t_bin / repeats * 1000, 3),
        "linear_search_ms": round(t_lin / repeats * 1000, 3),
        "builtin_any_ms": round(t_in / repeats * 1000, 3),
    }

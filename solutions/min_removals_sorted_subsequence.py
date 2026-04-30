import bisect

def find_rightmost_insert_position(tails, target):
    """Return the rightmost insertion position for target in a sorted list.

    For LNDS, equal characters should be placed to the right of existing equal values,
    which corresponds to the behavior of bisect_right.
    """
    left = 0
    right = len(tails)

    while left < right:
        mid = (left + right) // 2
        if tails[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return left


def min_removals_sorted_subsequence(s):
    """Return the minimum number of removals so the remaining characters form a non-decreasing subsequence.

    This is equivalent to computing the length of the longest non-decreasing subsequence (LNDS)
    and returning `len(s) - LNDS_length`.

    We use a patience-sorting style tails array and binary search.
    For LNDS, we must insert equal characters to the rightmost possible pile, which is handled by
    `bisect_right` instead of `bisect_left`.
    """

    # tails[i] is the smallest ending character of any non-decreasing subsequence of length i+1.
    tails = []

    for ch in s:
        # Find the insertion point to extend or replace an existing subsequence.
        # Custom binary search gives the same behavior as bisect_right.
        # pos = bisect.bisect_right(tails, ch)
        pos = find_rightmost_insert_position(tails, ch)

        if pos == len(tails):
            tails.append(ch)
        else:
            tails[pos] = ch

    return len(s) - len(tails)




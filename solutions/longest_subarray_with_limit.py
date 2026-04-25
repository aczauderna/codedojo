from collections import deque


def longest_subarray_with_limit(nums, limit):

#     I need the lenght of longest contigous subarray where
#     max(subarray) - min(subarray) <= limit

#    I'll have window [l,r]. I will expand r anytime max - min > limit, and shrink the left until it's valid again
#    To do this I'll have monotonic queues to track min and max

    max_dq = deque() # stores values in decreasing order - front is current max
    min_dq = deque() # stores values in increasing order - front is current min

    left = 0
    best = 0

    for right, num in enumerate(nums):

        # update max_dq
        while max_dq and max_dq[-1] < num:
            max_dq.pop()
        max_dq.append(num)

        # update min_dq
        while min_dq and min_dq[-1] > num:
            min_dq.pop()
        min_dq.append(num)

        # shrink from left while window is invalid
        while max_dq[0] - min_dq[0] > limit:

            if nums[left] == max_dq[0]:
                max_dq.popleft()
            if nums[left] == min_dq[0]:
                min_dq.popleft()

            left += 1

        # finally update best window
        best = max(best, right-left + 1)

    return best


# NOTES
# A monotonic queue is just a deque that keeps its elements in sorted order, but only internally — not representing the whole array, only the current window
# The deques do not store the entire window.
# They store only the elements that might become the max or min as the window slides.

# Example:
# Window: [2, 4, 7]
# max_dq (decreasing): [7]
# min_dq (increasing): [2]
# Even though the window has 3 elements, each deque has only 1.
# Why?
# Because:
# For max: once 7 enters, 4 and 2 can never be the max again → discard them.
# For min: once 2 enters, 4 and 7 can never be the min → discard them.

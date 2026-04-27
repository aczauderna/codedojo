def longest_subarray_with_k_distinct(nums, k):
    
    left = 0
    answer = 0
    current_window_count = {}

    for right, num in enumerate(nums):

        current_window_count[num] = current_window_count.get(num, 0) + 1

        # shrink if needed
        while len(current_window_count.keys()) > k:
            left_val = nums[left]
            current_window_count[left_val] -= 1
            if current_window_count[left_val] == 0:
                del current_window_count[left_val]
            left += 1

        answer = max(answer, right - left + 1)

    return answer
        



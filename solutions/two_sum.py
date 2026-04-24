
def two_sum(nums, target):
    """
    Find two numbers in the list that add up to the target value.

    Args:
        nums: List of integers
        target: Target sum value

    Returns:
        List of two indices [i, j] where nums[i] + nums[j] == target
    """
    # Create a hashmap to store value -> index
    num_map = {}

    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i

    # Should not reach here according to problem constraints
    return []

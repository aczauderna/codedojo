

def sum_of_unique_elements(nums):

    count = {}

    for num in nums:
        count[num] = count.get(num, 0) + 1
    
    unique_nums = [n for n, c in count.items() if c == 1]

    return sum(unique_nums)
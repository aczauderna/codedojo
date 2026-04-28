from collections import deque

def first_non_repeating_stream_char(stream):
    
    freq = {}
    queue = deque()
    result = []

    for i, ch in enumerate(stream):

        freq[ch] = freq.get(ch, 0) + 1

        if freq[ch] == 1:
            # this is first time we see this character, append it
            queue.append(ch)
            
        # remove all characters from the front that are no longer unique
        while queue and freq[queue[0]] > 1:
            queue.popleft()

        if queue:
            result.append(queue[0]) 
        else:
            result.append("#") 


    return "".join(result)
def count_vowels(s):
    
    vowels = set("aeiouAEIOU")
    count = 0
    
    for char in s:
        if char in vowels:
            count += 1
            
    return count
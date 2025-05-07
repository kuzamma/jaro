def jaro_similarity(s1, s2):
    """
    Calculate the Jaro similarity between two strings.
    
    Args:
        s1, s2 (str): Strings to compare
        
    Returns:
        float: Jaro similarity between s1 and s2 (0.0 to 1.0)
    """
    # If the strings are equal
    if s1 == s2:
        return 1.0
    
    len1 = len(s1)
    len2 = len(s2)
    
    # Maximum distance for matching characters
    max_dist = max(len1, len2) // 2 - 1
    
    # Initialize matching counts
    matches = 0
    s1_matches = [False] * len1
    s2_matches = [False] * len2
    
    # Find matching characters
    for i in range(len1):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len2)
        for j in range(start, end):
            if not s2_matches[j] and s1[i] == s2[j]:
                s1_matches[i] = True
                s2_matches[j] = True
                matches += 1
                break
    
    # If no matches found
    if matches == 0:
        return 0.0
    
    # Count transpositions
    k = 0
    transpositions = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    
    transpositions = transpositions // 2
    
    # Calculate Jaro similarity
    sim = (matches / len1 + matches / len2 + (matches - transpositions) / matches) / 3.0
    return sim
def adjust_difficulty(current_difficulty: str, is_correct: bool) -> str:
    """
    Adjusts student difficulty based on correctness of the answer.
    """
    levels = ["easy", "medium", "hard"]
    
    # Normalize input
    current_difficulty = current_difficulty.lower()
    if current_difficulty not in levels:
        current_difficulty = "easy"
        
    current_index = levels.index(current_difficulty)
    
    if is_correct:
        # Increase difficulty (up to hard)
        new_index = min(len(levels) - 1, current_index + 1)
    else:
        # Decrease difficulty (down to easy)
        new_index = max(0, current_index - 1)
        
    return levels[new_index]

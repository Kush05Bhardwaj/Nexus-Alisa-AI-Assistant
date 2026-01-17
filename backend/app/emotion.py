def extract_emotion(text: str):
    """
    Extract emotion tag from LLM response.
    Backend guard: If LLM forgets the emotion tag, add neutral as fallback.
    This ensures overlay and voice systems never break due to missing emotion.
    """
    # List of valid emotions
    valid_emotions = ["teasing", "calm", "serious", "happy", "sad", "neutral"]
    
    # Case 1: Proper format with tag
    if text.startswith("<emotion="):
        tag = text.split(">")[0]
        emotion = tag.replace("<emotion=", "")
        clean_text = text.split(">", 1)[1].strip()
        return emotion, clean_text
    
    # Case 2: LLM put emotion word at start without tag (fallback)
    for emotion in valid_emotions:
        if text.lower().startswith(emotion + " "):
            clean_text = text[len(emotion):].strip()
            return emotion, clean_text
        # Also check with newline
        if text.lower().startswith(emotion + "\n"):
            clean_text = text[len(emotion):].strip()
            return emotion, clean_text
    
    # Case 3: No emotion detected, add neutral
    return "neutral", text.strip()

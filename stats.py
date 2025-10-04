def get_num_words(text):
    """Return the number of words in text.

    Splits on any whitespace by default.
    """
    if text is None:
        return 0
    return len(text.split())

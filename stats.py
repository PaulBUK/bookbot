def get_num_words(text):
    """Return the number of words in text.

    Splits on any whitespace by default.
    """
    if text is None:
        return 0
    return len(text.split())


def char_frequencies(text):
    """Return a dict mapping each lowercase character to its frequency in text.

    Counts everything (letters, digits, punctuation, whitespace). Characters
    are converted to lowercase to avoid duplicates for different cases.
    """
    if text is None:
        return {}
    freqs = {}
    for ch in text.lower():
        freqs[ch] = freqs.get(ch, 0) + 1
    return freqs


def sort_char_counts(char_dict):
    """Convert a char->count dict into a list of {'char': c, 'num': n}

    Only alphabetical characters (char.isalpha() == True) are included.
    The returned list is sorted in-place from greatest to least by 'num'.
    """
    items = []
    for ch, cnt in char_dict.items():
        if ch.isalpha():
            items.append({"char": ch, "num": cnt})

    def get_num(d):
        return d["num"]

    items.sort(key=get_num, reverse=True)
    return items

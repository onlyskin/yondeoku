def _get_lemmas_above_threshold(lemmas, threshold):
    occurrences = _build_occurrences_dict(lemmas)
    above_threshold = [o for o in occurrences.keys() if occurrences[o] >= threshold]
    return set(above_threshold)

def _build_occurrences_dict(strings):
    occurrences = {}
    for string in strings:
        if string in occurrences.keys():
            occurrences[string] = occurrences[string] + 1
        else:
            occurrences[string] = 1
    return occurrences


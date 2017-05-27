def _filter_lemmas_by_new(lemmas, exclude_set):
    return [l for l in lemmas if l not in exclude_set]

def _enumerate_unread_sections(gBlock):
    output = []
    for i, s in enumerate(gBlock.sections):
        if not s.read:
            output.append((i, s))
    return output

def _get_next_n_words_and_section_indices(gBlock, exclude_set, n):
    indices = []
    new_lemmas = []
    unread_sections = _enumerate_unread_sections(gBlock)

    while len(indices) <= n and unread_sections:
        index, section = unread_sections.pop(0)
        next_lemmas = section.lemmas
        next_new_lemmas = _filter_lemmas_by_new(next_lemmas, exclude_set)
        if len(new_lemmas) == 0 or len(new_lemmas) + len(next_new_lemmas) <= n:
            indices.append(index)
            new_lemmas.extend(next_new_lemmas)
        else:
            break

    return {'indices': indices,
            'lemmas': new_lemmas}


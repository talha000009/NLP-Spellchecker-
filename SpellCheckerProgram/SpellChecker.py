import string


class SpellChecker:
    def __init__(self, corpus, levenshtein):
        self.corpus = corpus
        self.levenshtein = levenshtein
        self.vocabulary = corpus.vocabulary  # unique words
        self.words_count = corpus.words_count
        total_words = float(sum(self.words_count.values()))
        self.word_probabilities = {word: self.words_count[word] / total_words for word in self.vocabulary}

    def _level_one_edits(self, word):
        """returns all possible spelling error within one edit distance"""
        letters = string.ascii_lowercase
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [l + r[1:] for l, r in splits if r]
        swaps = [l + r[1] + r[0] + r[2:] for l, r in splits if len(r) > 1]
        replaces = [l + c + r[1:] for l, r in splits if r for c in letters]
        inserts = [l + c + r for l, r in splits for c in letters]

        return set(deletes + replaces + inserts + swaps)

    def _level_two_edits(self, word):
        """return all possible spelling error within two edit distance"""
        return set(edit2 for edit1 in self._level_one_edits(word) for edit2 in self._level_one_edits(edit1))

    def _check_error(self, word):
        """check if all possible spelling errors are within two edit distance then
        return to a suggested list of words sorted by probability of occurrence from the corpus"""
        candidates = self._level_one_edits(word) or self._level_two_edits(word) or [word]
        valid_candidates = [w for w in candidates if w in self.vocabulary]

        return sorted([(c, self.word_probabilities[c]) for c in valid_candidates], key=lambda tup: tup[1], reverse=True)

    def get_candidates(self, source):
        """return to suggested list of candidates sorted by Levenshtein minimum edit distance"""
        candidate_words = []
        candidates = self._check_error(source)
        for candidate, probability in candidates:
            med = self.levenshtein.minimum_edit_distance(source, candidate)
            candidate_words.append(('non_word_error', source, candidate, probability, med))

        # print(candidate_words)
        return sorted(candidate_words, key=lambda x: x[4])

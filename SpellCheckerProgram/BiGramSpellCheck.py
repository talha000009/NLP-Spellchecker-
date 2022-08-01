class BiGramSpellCheck:
    def __init__(self, levenshtein, corpus):
        self.corpus = corpus
        self.levenshtein = levenshtein

    def create_unigram(self):
        """return unique words from corpus"""
        return self.corpus.vocabulary

    def create_bigram(self, text_data):
        """returns to
        1. bigram models: which is pairs of words in a list;
        2. unigram_count: count the occurrence of words as unigram
        3. bigram_count: count the occurrence of words as bigram """
        bigrams = []
        unigram_count = {}
        bigram_count = {}

        for i in range(len(text_data) - 1):
            # count uniqram words
            if text_data[i] in unigram_count:
                unigram_count[text_data[i]] += 1
            else:
                unigram_count[text_data[i]] = 1

            # create and count bigrams
            if i < len(text_data) - 1:
                temp = (text_data[i], text_data[i+1])
                bigrams.append(temp)
                if temp in bigram_count:
                    bigram_count[temp] += 1
                else:
                    bigram_count[temp] = 1

        return bigrams, unigram_count, bigram_count

    def bigram_probability_calculation(self, model, unigram_count, bigram_count):
        """return to bigram probabilities
        eg: ('greater', 'antiquity'): 0.03225806451612903,
        ('antiquity', 'than'): 1.0,
        ('any', 'human'): 0.007692307692307693,
        ('human', 'remains'): 0.05555555555555555,
        ('remains', 'now'): 0.012345679012345678,
        """
        bigram_probabilities = {}
        for bigram in model:
            bigram_probabilities[bigram] = bigram_count.get(bigram) / unigram_count.get(bigram[0])
        return bigram_probabilities

    def word_bigram_probability_calculation(self, word, model, unigram_count, bigram_count):
        """return to bigram probabilities of specified word
        eg: {'this': 0.00909090909090909}
        {'is': 0.002074688796680498}
        {'earthquake': 0.16666666666666666}
        """
        bigram_probabilities = {}
        for bigram in model:

            bigram_probabilities[word] = bigram_count.get(bigram) / unigram_count.get(word)
        return bigram_probabilities

    def check_word_error(self, probabilities, data, checking_word):
        """return to suggested list of candidate words sorted by bigram probability"""
        candidate_words = []
        for i in range(len(data)):
            first_word, last_word = data[i - 1], data[i]
            if (first_word, last_word) not in probabilities and last_word == checking_word:
                # print("first word: ", first_word)
                # print("last word: ", last_word)
                for probable in probabilities:
                    if probable[0] == first_word:  # last_word == checking_word
                        probability = probabilities[probable]
                        # print("Probable: ", probable)
                        # print("probability", probability)
                        if probability > 0:
                            med = self.levenshtein.minimum_edit_distance(checking_word, probable[1])
                            candidate_words.append(('real_word_error', last_word, probable[1], probability, med))

        # print(candidate_words)
        return sorted(candidate_words, key=lambda x: x[3], reverse=True)

# model, unigram_count, bigram_count = bigram_model.create_bigram(corpus.get_file_data())
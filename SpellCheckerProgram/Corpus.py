# Import the libraries we need
import re
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

from collections import Counter


class Corpus:
    def __init__(self, corpus_file):
        bad_chars = [
            '-', '*', '+', '/', '?', '\\', '#', '$', '@', '%', '^', '&', '(', ')', '_', '=', '~', '|', '"', ':', ';',
            '[', ']', '{', '}', '.', ''
        ]
        self.words = []
        with open(corpus_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = ''.join((filter(lambda i: i not in bad_chars, line)))  # remove symbols and punctuations
                self.words += re.findall(r'[^0-9\s]\w+', line.lower())  # convert all words to lowercase
        # self.lemmatizer = WordNetLemmatizer()
        # self.stemmer = PorterStemmer()

        pre_processed_words = []
        for i in self.words:
            # stemmed_word = self.stemmer.stem(i)
            # lemmated_word = self.lemmatizer.lemmatize(i)
            # pre_processed_words.append(stemmed_word)
            # pre_processed_words.append(lemmated_word)
            pre_processed_words.append(i)

        self.sentences = nltk.sent_tokenize(open(corpus_file).read())
        self.vocabulary = set(pre_processed_words)
        self.words_count = Counter(self.words)
        self.total_words = float(sum(self.words_count.values()))

    # def stem_word(self, word):
    #     return self.stemmer.stem(word)
    #
    # def lem_word(self, word):
    #     return self.lemmatizer.lemmatize(word)

    def get_dictionary(self):
        """returns unique words from the corpus"""
        return self.vocabulary

    def get_file_data(self):
        """returns to a list of words found in corpus without symbols"""
        return self.words

    def get_word_count(self):
        """return a collection of counter of each words"""
        return self.words_count


corpus = Corpus("./corpus.txt")
# print("Corpus: ", corpus)
# print("Tokenized Sentence: ", corpus.sentences[0:2])
print(corpus.total_words)
uni = Counter(corpus.vocabulary)
print(float(sum(uni.values())))


import Corpus as c
import BiGramSpellCheck as b
import Levenshtein as l
import SpellChecker as sp
import App as ui


def main():
    corpus = c.Corpus("./corpus.txt")
    levenshtein = l.Levenshtein(1, 1, 2)  # Edit distance values can be changed
    non_word_error_checker = sp.SpellChecker(corpus, levenshtein)
    bigram_model = b.BiGramSpellCheck(levenshtein, corpus)
    ui.App(corpus, non_word_error_checker, bigram_model).mainloop()


if __name__ == '__main__':
    main()

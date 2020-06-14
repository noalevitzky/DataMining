import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import collections
import numpy as np
from scipy import special
import matplotlib.pyplot as plt
import math
from stop_words import get_stop_words

# nltk.download()

FILE_PATH = 'C:/Users/Noa/Desktop/huji/second year/dataMining/ex3/theWoderfulWizardOfOz.txt'
porter = PorterStemmer()


def stem_sentence(t):
    stem_sentence = []
    for word in t:
        stem_sentence.append(porter.stem(word))
    return stem_sentence


def get_ordered_freq(t):
    frequency = {}

    for word in t:
        count = frequency.get(word, 0)
        frequency[word] = count + 1

    ordered = {k: v for k, v in reversed(sorted(
        frequency.items(), key=lambda item: item[1]))}

    return ordered


def print_freq(f, section):
    print("**** ", section, " ****\nmost common tokens:\n", f,
          "\nnum of tokens: ", str(len(f.keys())),"\n")


if __name__ == "__main__":
    with open(FILE_PATH, 'r') as file:

        """ B - tokenize"""
        tokens = nltk.word_tokenize(file.read())
        ordered_freq = get_ordered_freq(tokens)
        print_freq(ordered_freq, 'B')

        """ plot B """
        values = list(ordered_freq.values())
        log_val = [math.log10(val) for val in values]
        key = [i for i in range(len(values))]

        # plot occurrences
        # s = np.array(log_val)
        #
        # # Calculate zipf and plot the data
        # a = 2.  # distribution parameter
        # count, bins, ignored = plt.hist(s, 50, normed=True)
        # x = np.arange(1., 50.)
        # y = x ** (-a) / special.zetac(a)
        # plt.plot(x, y / max(y), linewidth=2, color='r')
        # plt.show()
        #

        # lists = ordered_freq.items()  # sorted by key, return a list of tuples
        #
        # x, y = zip(*lists)  # unpack a list of pairs into two tuples
        # # x = [math.log10(i) for i in x]
        # y = [math.log10(i) for i in y]

        # plt.plot(x, y)
        # plt.show()

        """ C - remove stopwords"""
        tokens_no_sw = \
            [w for w in tokens if w not in get_stop_words('english')]
        ordered_freq_no_sw = get_ordered_freq(tokens_no_sw)
        print_freq(ordered_freq_no_sw, 'C')

        """ D - stem """
        tokens_no_sw_stemmed = stem_sentence(tokens_no_sw)
        ordered_freq_no_sw_stemmed = get_ordered_freq(tokens_no_sw_stemmed)
        print_freq(ordered_freq_no_sw_stemmed, 'D')

import pandas
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from stop_words import get_stop_words
from nltk.tokenize import PunktSentenceTokenizer
import re

# General
plt.style.use('fivethirtyeight')
FILE_PATH = 'C:/Users/Noa/Desktop/huji/second year/dataMining/ex3/theWoderfulWizardOfOz.txt'
NOUNS_PATH = 'C:/Users/Noa/Desktop/huji/second year/dataMining/ex3/nouns.txt'
porter = PorterStemmer()
STOP_SIGNS = [',', '.', "'", '"', '`', ';', "''", '""', "``", ']', '[', '(',
              ')', ':', "?", "!"]

with open(FILE_PATH, 'r') as file:
    tokens = nltk.word_tokenize(file.read())


# Helper Functions
def stem_sentence(t):
    stem_sentence = []
    for word in t:
        stem_sentence.append(porter.stem(word))
    return stem_sentence


def get_ordered_freq(t):
    frequency = {}
    for word in t:
        if word in STOP_SIGNS:
            continue

        count = frequency.get(word, 0)
        frequency[word] = count + 1

    ordered = {k: v for k, v in reversed(sorted(
        frequency.items(), key=lambda item: item[1]))}

    return ordered


def select_x_highest(d, num):
    i = 0
    highest_dict = {}

    for k, v in d.items():
        if i < num:
            highest_dict[k] = v
            i += 1
        else:
            return highest_dict


def print_freq(f, num, section):
    print("**** ", section, " ****\ntop 20 tokens:\n", f,
          "\nnum of tokens: ", num, "\n")


# For POS tagging
def process_content(tokenized_text, chunk):
    processed = []
    try:
        for i in tokenized_text:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            chunkParser = nltk.RegexpParser(chunk)
            chunked = chunkParser.parse(tagged)
            for subtree in chunked.subtrees(
                    filter=lambda t: t.label() == 'Chunk'):
                processed.append(subtree)
    except Exception as e:
        print(str(e))
    finally:
        return processed


def extract_phrases(nltk_chunked_txt):
    phrases = []
    for row in nltk_chunked_txt:
        row_lst = row.leaves()
        word_lst = []
        for word, t in row_lst:
            word_lst.append(word)
        phrases.append(" ".join(word_lst))
    return phrases

def extract_words(nltk_chunked_txt):
    phrases = []
    for row in nltk_chunked_txt:
        row_lst = row.leaves()
        for word, t in row_lst:
            phrases.append(word)
    return phrases

def parseSection(f_dict, section, title):
    freq_y = np.array(list(f_dict.values()))
    rank_x = np.arange(1, len(f_dict) + 1)
    fig, axes = plt.subplots()
    axes.loglog(rank_x, freq_y, marker=".", linestyle='None')

    plt.title(title)
    plt.ylabel('Word Frequency (log)')
    plt.xlabel('Rank (log)')
    # plt.show()
    res = select_x_highest(f_dict, 20)
    print_freq(res, len(f_dict), section)


if __name__ == "__main__":
    with open(FILE_PATH, 'r') as file:
        """ B - tokenize"""
        ordered_freq = get_ordered_freq(tokens)
        parseSection(ordered_freq, 'B',
                     'Frequency of Words In The Wizard of Oz')

        """ C - remove stopwords"""
        tokens_no_sw = \
            [w for w in tokens if w not in get_stop_words('english')]
        ordered_freq_no_sw = get_ordered_freq(tokens_no_sw)
        parseSection(ordered_freq_no_sw, 'C',
                     'Frequency of Words In The Wizard of Oz '
                     '(Without Stopwords)')

        """ D - stem """
        tokens_no_sw_stemmed = stem_sentence(tokens_no_sw)
        ordered_freq_no_sw_stemmed = get_ordered_freq(tokens_no_sw_stemmed)
        parseSection(ordered_freq_no_sw_stemmed, 'D',
                     'Frequency of Words In The Wizard of Oz '
                     '(w/ Stemming & w/o stopwords)')

        """ E - POS """
        custom_sent_tokenizer = PunktSentenceTokenizer("GWBush.txt")
        # JJ|JJR|JJS (one or more), and NN|NNS|NNP|NNPS (one or more)
        chunkPattern = r"""Chunk: {<JJ.?>+<NN.?.?>+} """

        with open(FILE_PATH, 'r') as file:
            tokenized = custom_sent_tokenizer.tokenize(file.read())

        processed = process_content(tokenized, chunkPattern)
        phrases = extract_phrases(processed)
        phrases_freq = get_ordered_freq(phrases)

        parseSection(phrases_freq, 'E',
                     'Frequency of Phrases In The Wizard of Oz (Adj+Noun)')

        """ F - example of a mistake in POS """
        # todo

        """ G - Tag cloud """
        chunkPattern = r"""Chunk: {(<NN.>)} """
        processed = process_content(tokenized, chunkPattern)
        phrases = extract_words(processed)
        phrases_freq = get_ordered_freq(phrases)
        print("**** G ****\nnouns by freq:\n", phrases_freq, '\nnum of nouns: '
              + str(len(phrases_freq)) + '\n') 
        
        with open(NOUNS_PATH, 'w') as f:
            f.write(" ".join(phrases))

        """ H - re for two consecutive repeated words """
        reg = re.compile(r'\b(\w+)[\'\<\>\|\.\?\-\"\,\:\;\[\]\(\)\{\}\\\!\~'
                         r'\@\#\%\^\&\*\s]+\1\b')
        repeated = []
        with open(FILE_PATH, 'r') as file:
            for line in file:
                if reg.search(line):
                    repeated.append(line.rstrip().lstrip())

        print("**** H ****\nrepeated tokens (total " + str(len(repeated)) + "):")
        for i, line in enumerate(repeated):
            print(str(i+1) + ':', line)



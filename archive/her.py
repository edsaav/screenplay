import re
from collections import Counter
from matplotlib import pyplot as plt

word_list = []

with open('her.txt', 'r') as f:
    for line in f:
        word_list.extend(line.strip().split(' '))

def clean_word(word):
    word = re.sub('[.,!?:;\-()]','',word)
    return word.lower()

stop_words = ['a','the', 'an', 'is', 'if', 'are', 'were', 'there', 'then', 'am',
    'where', 'and', 'at', 'in', 'he', 'she', 'me', 'of', 'as', 'they', 'her', 'on',
    'to', 'his', 'with', 'be', 'on', 'to', 'you', 'do', 'your', 'you\'re', 'your',
    'yours', 'what', 'was', 'this', 'that', 'that\'s', 'my', 'we', 'so', 'pg',
    'has', 'have', 'had', 'i', 'i\'m', 'i\'ve', 'i\'d', 'i\'ll', 'it', 'it\'s',
    'continued', 'int', 'cont\'d', 'for', 'about', 'them', 'from', 'through']

clean_list = [clean_word(x) for x in word_list if len(x) > 1 and clean_word(x) not in stop_words ]

clean_list.sort()

def remove_singles(wc):
    singles = []
    for i in wc:
        if wc[i] == 1:
            singles.append(str(i))
    for s in singles:
        del wc[s]
    return wc

words_count = remove_singles(Counter(clean_list))

words = [w for w in words_count]
counts = [words_count[w] for w in words_count]

plt.bar(words, counts)
plt.ylabel('# of Occurances')
plt.title('Word Counts in "Her"(2013)')

plt.show()

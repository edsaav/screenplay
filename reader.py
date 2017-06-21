import os
import film
from nltk.tokenize import word_tokenize

def script_files():
    directory = os.path.dirname(os.path.realpath(__file__))
    sf = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            sf.append(filename)
    return sf

for s in script_files():
    f = film.Film(s)
    print s + ': ' + str(f.word_count_dialogue()) + ' words of dialogue.'
    print s + ': ' + str(f.number_of_lines()) + ' lines of dialogue.'
    print s + ': ' + str(f.words_per_line()) + ' average words per line.'
    print s + ': ' + str(f.number_of_scenes()) + ' total scenes.'

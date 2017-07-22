import os
import film
from nltk.tokenize import word_tokenize

SCRIPTS_FOLDER = 'scripts'

def script_files():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), SCRIPTS_FOLDER)
    sf = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            sf.append(os.path.join(SCRIPTS_FOLDER, filename))
    return sf

for s in script_files():
    try:
        f = film.Film(s)
        print f.stats()
    except IndexError:
        print 'Bad script error: ' + s

# for s in script_files():
#     print s

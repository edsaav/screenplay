import os
import film
from nltk.tokenize import word_tokenize
import csv

SCRIPTS_FOLDER = 'scripts'

def script_files():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), SCRIPTS_FOLDER)
    sf = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            sf.append(os.path.join(SCRIPTS_FOLDER, filename))
    return sf

# for s in script_files():
#     try:
#         f = film.Film(s)
#         print f.stats()
#     except IndexError:
#         print 'Bad script error: ' + s

with open('script_data.csv','w') as datafile:
    fieldnames = ['Title', 'Dialogue Ratio', 'Parenthetical Ratio', 'Words per Line', 'Dialogue Sentiment', 'Number of Scenes']
    writer = csv.DictWriter(datafile, fieldnames=fieldnames)
    tracker = 0
    failures = 0
    print 'Starting processing...'

    writer.writeheader()
    for s in script_files():
        try:
            f = film.Film(s)
            writer.writerow(f.stats())
            tracker += 1
        except:
            'Failed to write ' + s
            failures += 1
        print str(tracker) + ' successes and ' + str(failures) + ' failures...'
    print 'Processing complete!'

# for s in script_files():
#     print s

# screenplay.py

import re
from collections import Counter
from matplotlib import pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def list_characters(doc):
    character_list = []
    symbols = re.compile('[:\-(.!]|FADE') # regex to capture all caps lines that are not character names
    for line in doc:
        content = line.strip()
        if content.isupper() and not symbols.search(content):
            character_list.append(content)
    return character_list

def set_characters(doc):
    character_list = list_characters(doc)
    return set(character_list)

def character_appearances(doc, recurring = False):
    """Return as a dictionary every speaking character along with their Number
    of lines. Optionally exclude characters with only a single line.
    """
    character_list = list_characters(doc)
    appearances = Counter(character_list)
    singles = []
    if recurring == True:
        for c in appearances:
            if appearances[c] == 1:
                singles.append(str(c))
        for s in singles:
            del appearances[s]
        return appearances
    return appearances

def character_chart(doc):
    ca = character_appearances(doc, True)
    characters = [c for c in ca]
    appearances = [ca[c] for c in ca]
    x = [x for x, _ in enumerate(characters)]
    plt.bar(x,appearances)
    plt.ylabel('Number of Lines')
    plt.title('Characters by Number of Lines')
    plt.xticks([i for i, _ in enumerate(characters)], characters)
    plt.show()

def extract_content(doc):
    """Return as a string all dialogue and descriptive text, as is.
    """
    content = ''
    ignore = re.compile('[:\-(]|FADE|pg\.')
    for line in doc:
        if not ignore.search(line) and not line.isupper():
            content += line
    return content

def content_words(doc, remove_stopwords = False):
    """Return as a list all dialogue and descriptive text broken down into
    lowercase word tokens, excluding punctuation. Optionally ignore stopwords.
    """
    punctuation = ['.', ',', '!', '?', ':', ';', '...']
    suffix = ['\'s', '\'ve', '\'m', 'n\'t', '\'ll', '\'re']
    stopwords_list = set(stopwords.words('english'))
    exclude = punctuation + suffix
    if remove_stopwords == True:
        exclude.extend(stopwords_list)
    tokens = word_tokenize(extract_content(doc))
    words = [t.lower() for t in tokens]
    stripped_words = [w for w in words if w not in exclude]
    return stripped_words

def word_histogram(doc):
    words_counts = Counter(content_words(doc))
    words = [w for w in words_counts]
    counts = [words_counts[w] for w in words_counts]
    x = [x for x, _ in enumerate(words)]
    plt.bar(x, counts)
    plt.xticks([i for i, _ in enumerate(words)], words)
    plt.show()

def top_n_interesting_words(doc, n):
    return Counter(content_words(doc, True)).most_common(n)

def is_transition(line):
    regex = re.compile('FADE|MONTAGE|CONTINUED|INTERCUT|CUT TO')
    if line.isupper() and regex.search(line):
        return True
    return False

def is_slugline(line):
    regex = re.compile('INT\.|EXT\.')
    if line.isupper() and regex.search(line):
        return True
    return False

def is_character(line):
    regex = re.compile('^\s+[A-Z]')
    if is_slugline(line) or is_transition(line):
        return False
    elif regex.search(line) and line.isupper():
        return True
    else:
        return False

def is_parenthetical(line):
    regex = re.compile('^\s+\(|^\s[a-z\ ]+\)')
    if regex.search(line) and line.islower():
        return True
    return False

def is_page(line):
    regex = re.compile('pg\.|^\s{20,200}[1-9]')
    # regex = re.compile('^\s+[1-9]')
    if regex.search(line):
        return True
    return False

def is_dialogue(line):
    regex = re.compile('^\s{3,99}[A-Za-z][\sa-z\']')
    if regex.search(line):
        return True
    return False

def is_action(line):
    regex = re.compile('^\s{0,3}[A-Za-z][\sa-z]')
    page_regex = re.compile('pg\.')
    if not is_parenthetical(line):
        if regex.search(line) and not page_regex.search(line):
            return True
    return False

def is_blank(line):
    if not line.strip():
        return True
    return False

# def line_type(line):
#     parenthetical = re.compile('  \(|\)')
#     symbols = re.compile('[:\-.!]|FADE|MONTAGE|MORE')
#     page = re.compile('pg\.')
#     dialogue = re.compile('   [A-Z]|   [a-z]')
#     if line.strip().isupper():
#         if symbols.search(line):
#             return 'slug'
#         else:
#             return 'character'
#     elif not line.strip():
#         return 'blank'
#     elif parenthetical.search(line):
#         return 'parenthetical'
#     elif page.search(line):
#         return 'page'
#     elif dialogue.search(line) and not parenthetical.search(line):
#         return 'dialogue'
#     else:
#         return 'action'

def normalize_character(line):
    line_words = line.strip().split(' ')
    if '(CONT\'D)' in line_words:
        del line_words[line_words.index('(CONT\'D)')]
    char = ''
    for i in [w for w in line_words if len(w) > 1]:
        char += i + ' '
    return char.strip()

def next_dialogue_line(doc, block = ''):
    l = next(doc)
    if is_blank(l):
        print block.strip()
    else:
        if is_parenthetical(l) or is_page(l):
            l = next(doc)
        if is_dialogue(l):
            block += l.strip() + ' '
        next_dialogue_line(doc, block)

def get_lines(doc, character):
    for line in doc:
        if is_character(line) and normalize_character(line) == character.upper():
            next_dialogue_line(doc)


# def extract_lines(doc):
#     for line in doc:
#         if is_action(line):
#             print line

# 'action' is catching quoted and numerical text
# consider composing a Script class that opens a file upon instantiation







###### Test code below ######
with open('her.txt', 'r') as f:
    get_lines(f, 'theodore')

from __future__ import division
import re
from nltk.tokenize import word_tokenize
from copy import copy
from textblob import TextBlob


class Film(object):

    def __init__(self, text_file):
        self.f = []
        self.count = { 'lines':0, 'parentheticals':0, 'scenes':0 }
        self.characters = []
        with open(text_file, 'r') as doc:
            for line in doc:
                self.f.append(line)
        for line in self.f:
            if self.__is_character(line):
                self.count['lines'] += 1
                character = self.__normalize_character(line)
                if not character in self.characters and not character.split(' ')[0] in self.characters:
                    self.characters.append(character)
            elif self.__is_parenthetical(line):
                self.count['parentheticals'] += 1
            elif self.__is_slugline(line):
                self.count['scenes'] += 1
        self.title = self.characters[0]
        self.characters = self.characters[1:]

    def stats(self):
        return {
            'Title' : self.title,
            'Dialogue Ratio' : self.dialogue_ratio(),
            'Parenthetical Ratio' : self.parenthetical_ratio(),
            'Words per Line' : self.words_per_line(),
            'Dialogue Sentiment' : self.dialogue_sentiment(),
            'Number of Scenes' : self.number_of_scenes()
        }

    def word_count_dialogue(self):
        return len(self.__dialogue())

    def word_count_full_text(self):
        return len(self.__full_text())

    def dialogue_ratio(self):
        t = self.word_count_full_text()
        d = self.word_count_dialogue()
        return d/t

    def parenthetical_ratio(self):
        return self.count['parentheticals']/self.count['lines']

    def number_of_lines(self):
        n = 0
        for line in self.f:
            if self.__is_character(line):
                n += 1
        return n

    def words_per_line(self):
        return self.word_count_dialogue()/self.number_of_lines()

    def number_of_scenes(self):
        n = 0
        for line in self.f:
            if self.__is_slugline(line):
                n += 1
        return n

    def number_of_parentheticals(self):
        n = 0
        for line in self.f:
            if self.__is_parenthetical(line):
                n += 1
        return n

    def dialogue_sentiment(self):
        d = ''
        for l in self.__dialogue():
            d += l
            d += ' '
        blob = TextBlob(d)
        return blob.sentiment.polarity

    def categorize(self):
        for l in self.f:
            print self.__type(l) + l

    def __type(self, line):
        if self.__is_dialogue(line):
            return 'Dialogue:     |'
        elif self.__is_character(line):
            return 'Character:    |'
        elif self.__is_slugline(line):
            return 'Slugline:     |'
        elif self.__is_transition(line):
            return 'Transition:   |'
        elif self.__is_parenthetical(line):
            return 'Parenthetical:|'
        elif self.__is_page(line):
            return 'Page:         |'
        elif self.__is_blank(line):
            return 'Blank:        |'
        elif self.__is_action(line):
            return 'Action:       |'
        else:
            return 'Unknown:      |'


    def __is_dialogue(self, line):
        regex = re.compile('^\s{8,25}[A-Za-z\-][\sa-z\'\-][\sA-Za-z\.]')
        shouting = re.compile('[A-Z]\!|HHHH')
        if regex.search(line) or shouting.search(line):
            return True
        return False

    def __is_page(self, line):
        regex = re.compile('pg\.|^\s{20,200}[1-9]')
        if regex.search(line):
            return True
        return False

    def __is_blank(self, line):
        if not line.strip():
            return True
        return False

    def __is_action(self, line):
        regex = re.compile('^\s{0,7}[A-Za-z][\sa-z\'][\sa-z\']|^\s{0,7}\.{3}[A-Za-z][\sa-z\'][\sa-z\']')
        page_regex = re.compile('pg\.')
        if not self.__is_parenthetical(line):
            if regex.search(line) and not page_regex.search(line):
                return True
        return False

    def __is_character(self, line):
        regex = re.compile('^\s{10,100}[A-Z]')
        if self.__is_slugline(line) or self.__is_transition(line) or self.__is_dialogue(line):
            return False
        elif regex.search(line) and line.isupper():
            return True
        else:
            return False

    def __is_transition(self, line):
        regex = re.compile('FADE|MONTAGE|CONTINUED|INTERCUT| CUT |CARRYING US TO|BLACK:|[A-Z]+\.{3}|SUPERIMPOSE|CONTINUOUS|TITLE|SHOTS|BACK TO:|MOMENTS LATER')
        if line.isupper() and regex.search(line):
            return True
        return False

    def __is_slugline(self, line):
        regex = re.compile('INT\.|EXT\.')
        if line.isupper() and regex.search(line):
            return True
        return False

    def __clean_tokens(self, line):
        punctuation = ['.', ',', '!', '?', ':', ';', '...', '-', '--']
        suffix = ['\'s', '\'ve', '\'m', 'n\'t', '\'ll', '\'re']
        exclude = punctuation + suffix
        l = copy(line)
        words = [w.lower() for w in word_tokenize(l)]
        cleaned_words = [w for w in words if w not in exclude]
        return cleaned_words

    def __dialogue(self):
        d = []
        for line in self.f:
            if self.__is_dialogue(line):
                d.extend(self.__clean_tokens(line))
        return d

    def __is_parenthetical(self, line):
        regex = re.compile('^\s+\(|^\s[a-z\ ]+\)')
        if regex.search(line) and line.islower():
            return True
        return False

    def __full_text(self):
        text = []
        for line in self.f:
            text.extend(self.__clean_tokens(line))
        return text

    def __normalize_character(self, line):
        line_words = line.strip().split(' ')
        notes = ['(CONT\'D)', '(O.S.)', '(V.O.)']
        for n in notes:
            if n in line_words:
                del line_words[line_words.index(n)]
        char = ''
        for i in [w for w in line_words if len(w) > 1]:
            char += i + ' '
        return char.strip()

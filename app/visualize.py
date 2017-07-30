import matplotlib.pyplot as plt
import csv

class Visualize(object):

    def __init__(self):
        self.dialogue_ratio = []
        self.parenthetical_ratio = []
        self.words_per_line = []
        self.dialogue_sentiment = []
        self.number_of_scenes = []
        self.results = []

        with open('full_data_set.csv','rb') as f:
            reader = csv.reader(f)
            for r in reader:
                try:
                    self.dialogue_ratio.append(float(r[1]))
                    self.parenthetical_ratio.append(float(r[2]))
                    self.words_per_line.append(float(r[3]))
                    self.dialogue_sentiment.append(float(r[4]))
                    self.number_of_scenes.append(float(r[5]))
                    self.results.append(float(r[8]))
                except:
                    print 'Skipping header line...'

    def view(self,field):
        plt.plot(field,self.results,'bo')
        plt.show()

    def view_all(self):
        data = [self.dialogue_ratio, self.parenthetical_ratio, self.words_per_line, self.dialogue_sentiment, self.number_of_scenes]
        for d in data:
            self.view(d)

v = Visualize()
v.view_all()

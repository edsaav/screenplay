import matplotlib.pyplot as plt
import csv

class Visualize(object):

    def __init__(self):
        # self.dialogue_ratio = []
        # self.parenthetical_ratio = []
        # self.words_per_line = []
        # self.dialogue_sentiment = []
        # self.number_of_scenes = []
        # self.results = []
        self.data = {
            'Dialogue Ratio':[],
            'Parenthetical Ratio':[],
            'Words per Line':[],
            'Dialogue Sentiment':[],
            'Number of Scenes':[],
            'Results':[]
        }

        with open('full_data_set.csv','rb') as f:
            reader = csv.reader(f)
            for r in reader:
                try:
                    self.data['Dialogue Ratio'].append(float(r[1]))
                    self.data['Parenthetical Ratio'].append(float(r[2]))
                    self.data['Words per Line'].append(float(r[3]))
                    self.data['Dialogue Sentiment'].append(float(r[4]))
                    self.data['Number of Scenes'].append(float(r[5]))
                    self.data['Results'].append(float(r[8]))
                except:
                    print 'Skipping header line...'

    def view(self,field):
        plt.plot(self.data[field],self.data['Results'],'bo')
        plt.xlabel(field)
        plt.ylabel('Domestic Gross Revenue')
        plt.show()

    def view_all(self):
        for d in self.data:
            if d != 'Results':
                self.view(d)

v = Visualize()
v.view_all()

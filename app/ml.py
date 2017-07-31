import numpy as np
import tensorflow as tf
import csv
import time

class Learner(object):

    def __init__(self):
        self.data = {
            'Dialogue Ratio':[],
            'Parenthetical Ratio':[],
            'Words per Line':[],
            'Dialogue Sentiment':[],
            'Number of Scenes':[],
            'Results':[],
            'Results Category':[]
        }
        self.__read('full_data_set.csv')

    def linear_classify(self,column):
        features = [tf.contrib.layers.real_valued_column('x', dimension=1)]
        estimator = tf.contrib.learn.LinearClassifier(feature_columns=features)

        x_train = np.array(self.data[column][:300])
        y_train = np.array(self.data['Results Category'][:300])
        x_eval = np.array(self.data[column][301:])
        y_eval = np.array(self.data['Results Category'][301:])
        input_fn = tf.contrib.learn.io.numpy_input_fn({"x":x_train}, y_train,
                                                      batch_size=300,
                                                      num_epochs=1000)
        eval_input_fn = tf.contrib.learn.io.numpy_input_fn(
            {"x":x_eval}, y_eval, batch_size=121, num_epochs=1000)

        estimator.fit(input_fn=input_fn, steps=1000)

        accuracy_score = estimator.evaluate(input_fn=input_fn, steps=1)['accuracy']

        self.__log(column,accuracy_score,'linear_classify')

        print "Accuracy Score: %r"% accuracy_score

    def dnn_classify(self,column):
        features = [tf.contrib.layers.real_valued_column('x', dimension=1)]
        estimator = tf.contrib.learn.DNNClassifier(feature_columns=features, hidden_units=[10,20,10],n_classes=2,model_dir='/tmp/iris_model')

        x_train = np.array(self.data[column][:300])
        y_train = np.array(self.data['Results Category'][:300])
        x_eval = np.array(self.data[column][301:])
        y_eval = np.array(self.data['Results Category'][301:])
        input_fn = tf.contrib.learn.io.numpy_input_fn({"x":x_train}, y_train,
                                                      batch_size=300,
                                                      num_epochs=1000)
        eval_input_fn = tf.contrib.learn.io.numpy_input_fn(
            {"x":x_eval}, y_eval, batch_size=121, num_epochs=1000)

        estimator.fit(input_fn=input_fn, steps=1000)

        accuracy_score = estimator.evaluate(input_fn=input_fn, steps=1)['accuracy']

        self.__log(column,accuracy_score,'dnn_classify')

        print "Accuracy Score: %r"% accuracy_score

    def __read(self,source):
        with open(source,'rb') as f:
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
            for r in self.data['Results']:
                if (r) >= np.mean(self.data['Results']):
                    self.data['Results Category'].append(1)
                else:
                    self.data['Results Category'].append(0)

    def __log(self,column,accuracy,function):
        with open('log.txt','a+') as f:
            f.write(str(time.time()) + ' : ' + column + ' : ' + str(accuracy) + ' : ' + function + "\n")

l = Learner()
l.dnn_classify('Dialogue Ratio')

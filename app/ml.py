import numpy as np
import tensorflow as tf
import csv

data = []
results = []

with open('full_data_set.csv','rb') as f:
    reader = csv.reader(f)
    for r in reader:
        try:
            data_points = [float(r[1]),float(r[2]),float(r[3]),float(r[4]),float(r[5])]
            data.append(data_points)
            if float(r[8]) >= 5000000:
                results.append(0)
            else:
                results.append(1)
        except:
            print 'Header line'

features = [tf.contrib.layers.real_valued_column('x', dimension=2)]
estimator = tf.contrib.learn.LinearClassifier(feature_columns=features)

x_train = np.array(data[:300])
y_train = np.array(results[:300])
x_eval = np.array(data[301:])
y_eval = np.array(results[301:])
input_fn = tf.contrib.learn.io.numpy_input_fn({"x":x_train}, y_train,
                                              batch_size=300,
                                              num_epochs=1000)
eval_input_fn = tf.contrib.learn.io.numpy_input_fn(
    {"x":x_eval}, y_eval, batch_size=121, num_epochs=1000)

estimator.fit(input_fn=input_fn, steps=1000)

accuracy_score = estimator.evaluate(input_fn=input_fn, steps=1)['accuracy']

print "Accuracy Score: %r"% accuracy_score

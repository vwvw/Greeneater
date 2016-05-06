import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing as pre
from sklearn import svm

def find_closest(A, target):
    #A must be sorted
    idx = A.searchsorted(target)
    idx = np.clip(idx, 1, len(A)-1)
    left = A[idx-1]
    right = A[idx]
    idx -= target - left < right - target
    return idx[0]

DELTA = 300


FMT = '%Y-%m-%d %H:%M:%S';
dateparse = lambda x: pd.datetime.strptime(x, FMT)

my_data = pd.read_csv('temperatures_formatted.csv', delimiter=';', parse_dates=['dateAndTime'], date_parser=dateparse)

begin_training = pd.datetime.strptime('2016-03-11 00:00:00',FMT)
end_training = pd.datetime.strptime('2016-03-20 00:00:00',FMT)
begin_test = pd.datetime.strptime('2016-03-29 00:00:00',FMT)
end_test = pd.datetime.strptime('2016-04-10 00:00:00',FMT)



dt = my_data['dateAndTime']
index_b_training = find_closest(dt,begin_training)
index_e_training = find_closest(dt, end_training)
index_b_test = find_closest(dt,begin_test)
index_e_test = find_closest(dt, end_test)

plt.style.use('ggplot')
plt.figure()
my_data.ix[1:len(my_data),1:5].plot()
plt.draw()
plt.show(block=False)

print index_e_training - index_b_training

room_training = my_data.ix[index_b_training:index_e_training-DELTA,3].reset_index(drop=True)
appartment_training = my_data.ix[index_b_training:index_e_training-DELTA,1].reset_index(drop=True)
outside_training = my_data.ix[index_b_training:index_e_training,2].reset_index(drop=True)
state_training = my_data.ix[index_b_training:index_e_training,4].reset_index(drop=True)
state_integral = state_training.rolling(window=DELTA,center=False).sum().ix[DELTA:].reset_index(drop=True).divide(DELTA)
room_predicted = room_training.copy(deep=True)
for num in range(1,3):


	print room_predicted
	print outside_training

	appart_diff = appartment_training.subtract(room_predicted).reset_index(drop=True)

	outside_integral = outside_training.subtract(room_predicted).rolling(window=DELTA,center=False).sum().ix[DELTA:].reset_index(drop=True).divide(DELTA)

	X_train = pd.concat([appart_diff, outside_integral, room_training, state_integral], axis=1)

	print X_train
	scaler = pre.StandardScaler().fit(X_train)
	X_train_scaled = scaler.transform(X_train)

	room_real_training = my_data.ix[index_b_training+DELTA:index_e_training,3].reset_index(drop=True)
	print "begin training"
	SVR_model = svm.SVR(kernel='rbf',C=100,gamma=.001).fit(X_train_scaled,room_real_training)
	print "end training"
	room_predicted = pd.Series(data=SVR_model.predict(X_train_scaled))

#
# Testing 
#


appartment_test = my_data.ix[index_b_test:index_e_test-DELTA,1].reset_index(drop=True)
outside_test = my_data.ix[index_b_test:index_e_test,2].reset_index(drop=True)
room_test = my_data.ix[index_b_test:index_e_test-DELTA,3].reset_index(drop=True)
state_test = my_data.ix[index_b_test:index_e_test,4].reset_index(drop=True)


appart_diff_test = appartment_test.subtract(room_test).reset_index(drop=True)
state_integral_test = state_test.rolling(window=DELTA,center=False).sum().ix[DELTA:].reset_index(drop=True).divide(DELTA)
outside_integral_test = outside_test.rolling(window=DELTA,center=False).sum().ix[DELTA:].reset_index(drop=True).divide(DELTA)

X_test = pd.concat([appart_diff_test, outside_integral_test, room_test, state_integral_test], axis=1)
print X_test
X_test_scaled = scaler.transform(X_test)

room_real_test = my_data.ix[index_b_test+DELTA:index_e_test,3].reset_index(drop=True)
predict_y_array = SVR_model.predict(X_test_scaled)

room_real_test_array = np.array(room_real_test, dtype=pd.Series)

diff = np.subtract(room_real_test_array,predict_y_array)

print "-----\n"
print np.mean(np.absolute(diff))
print "-----"
hist, bins = np.histogram(diff, bins=11)
width = 0.7 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.figure()
plt.bar(center, hist, align='center', width=width)

print "end of the programm"
plt.style.use('ggplot')
plt.figure()

plt.plot(predict_y_array,label='predicted')
plt.plot(room_real_test_array, label='real')
lgd = plt.legend()
plt.draw()
plt.show()

SVR_model.score(X_test_scaled,room_real_test)



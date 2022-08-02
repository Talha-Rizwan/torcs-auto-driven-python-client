import sys
import argparse
import socket
import driver
from turtle import down, forward, rt, up
import csv
import driver
import carState
import pandas as pd
import os.path

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

from imblearn.over_sampling import SMOTE
from random import randint
#################################################

# Function importing Dataset
class buildtree:
  def importdata(self):
    balance_data = pd.read_csv('data.csv')
    balance_data=balance_data.drop(labels='Opponents',axis=1)
    balance_data=balance_data.drop(labels='Track',axis=1)
    balance_data=balance_data.drop(labels='CurLapTime',axis=1)
    balance_data=balance_data.drop(labels='Damage',axis=1)
    balance_data=balance_data.drop(labels='DistanceFromStart',axis=1)
    balance_data=balance_data.drop(labels='DistanceRaced',axis=1)
    balance_data=balance_data.drop(labels='Fuel',axis=1)
    balance_data=balance_data.drop(labels='Rpm',axis=1)
    balance_data=balance_data.drop(labels='SpeedX',axis=1)
    balance_data=balance_data.drop(labels='SpeedY',axis=1)
    balance_data=balance_data.drop(labels='SpeedZ',axis=1)
    balance_data=balance_data.drop(labels='Brake',axis=1)
    balance_data=balance_data.drop(labels='Gear',axis=1)
    balance_data=balance_data.drop(labels='Clutch',axis=1)
    balance_data=balance_data.drop(labels='Focus',axis=1)
    balance_data=balance_data.drop(labels='Meta',axis=1)
    
    balance_data.info()
    # print ("Dataset of unbalanced data: \n ",balance_data.head())
    return balance_data

  def balance(self,df):
    # print("the balance data arrow keys are : ")
    # print(df['ArrowKey'].value_counts())
    seed = 100
    k = 1
    X = df.loc[:, df.columns != 'ArrowKey']
    y = df['ArrowKey'].copy()
    # print(y)
    # print("the value of X is : ")
    # print(X)
    sm = SMOTE(sampling_strategy='auto', k_neighbors=k, random_state=seed)
    X_res, y_res = sm.fit_resample(X, y)
    df = pd.concat([ pd.DataFrame(y_res),pd.DataFrame(X_res)], axis=1)
    df.columns = ['ArrowKey','Angle','TrackPos','Acceleration','Steer' ]
    # print("balanced dataframe is :", df['ArrowKey'].value_counts()) 
    # print("displaying the head of dataset:")
    # df.head() 
    return df

  # # Function to split the dataset
  def splitdataset(self,balance_data):
  # Separating the target variable
    X = balance_data.values[:, 1:5]
    Y = balance_data.values[:, 0]

    # Splitting the dataset into train and test
    X_train, X_test, y_train, y_test = train_test_split( 
    X, Y, test_size = 0.3)

    # print(X_train)
    return X, Y, X_train, X_test, y_train, y_test

  def train_using_gini(self,X_train, X_test, y_train):
    # Creating the classifier object
    clf_gini = DecisionTreeClassifier(criterion = "gini")

    # Performing training
    clf_gini.fit(X_train, y_train)
    return clf_gini

  # Function to perform training with entropy.
  def tarin_using_entropy(self,X_train, X_test, y_train):

    # Decision tree with entropy
    clf_entropy = DecisionTreeClassifier(
            criterion = "entropy", random_state = 100,
            max_depth = 3, min_samples_leaf = 5)

    # Performing training
    clf_entropy.fit(X_train, y_train)
    return clf_entropy

  # Function to make predictions
  def prediction(self,X_test, clf_object):
    
      # Predicton on test with giniIndex
      y_pred = clf_object.predict(X_test)
      print("Predicted values:")
      print(y_pred)
      return y_pred
        
  # Function to calculate accuracy
  def cal_accuracy(self,y_test, y_pred):
        
      print("Confusion Matrix: ",
          confusion_matrix(y_test, y_pred))
        
      print ("Accuracy : ",
      accuracy_score(y_test,y_pred)*100)
        
      print("Report : ",
      classification_report(y_test, y_pred))


#################################################
def check_header(filename):
    if os.path.isfile(filename):
        return True
    else:
        return False


if __name__ == '__main__':
    pass

# Configure the argument parser
parser = argparse.ArgumentParser(description = 'Python client to connect to the TORCS SCRC server.')

parser.add_argument('--host', action='store', dest='host_ip', default='localhost',
                    help='Host IP address (default: localhost)')
parser.add_argument('--port', action='store', type=int, dest='host_port', default=3001,
                    help='Host port number (default: 3001)')
parser.add_argument('--id', action='store', dest='id', default='SCR',
                    help='Bot ID (default: SCR)')
parser.add_argument('--maxEpisodes', action='store', dest='max_episodes', type=int, default=1,
                    help='Maximum number of learning episodes (default: 1)')
parser.add_argument('--maxSteps', action='store', dest='max_steps', type=int, default=0,
                    help='Maximum number of steps (default: 0)')
parser.add_argument('--track', action='store', dest='track', default=None,
                    help='Name of the track')
parser.add_argument('--stage', action='store', dest='stage', type=int, default=3,
                    help='Stage (0 - Warm-Up, 1 - Qualifying, 2 - Race, 3 - Unknown)')

arguments = parser.parse_args()

# Print summary
print('Connecting to server host ip:', arguments.host_ip, '@ port:', arguments.host_port)
print('Bot ID:', arguments.id)
print('Maximum episodes:', arguments.max_episodes)
print('Maximum steps:', arguments.max_steps)
print('Track:', arguments.track)
print('Stage:', arguments.stage)
print('*********************************************')

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as msg:
    print('Could not make a socket.')
    sys.exit(-1)

# one second timeout
sock.settimeout(1.0)

shutdownClient = False
curEpisode = 0
list1=[]
list2=[]
header=['ArrowKey','Angle','CurLapTime','Damage','DistanceFromStart','DistanceRaced','Fuel','Opponents','Rpm','SpeedX','SpeedY','SpeedZ','Track','TrackPos','Acceleration','Brake','Gear','Steer','Clutch','Focus','Meta']
verbose = False
key="None"
d = driver.Driver(arguments.stage)



tree=buildtree()
data = tree.importdata()
data=tree.balance(data)
X, Y, X_train, X_test, y_train, y_test = tree.splitdataset(data)
clf_gini = tree.train_using_gini(X_train, X_test, y_train)


while not shutdownClient:
    while True:
        print('Sending id to server: ', arguments.id)
        buf = arguments.id + d.init()
        print('Sending init string to server:', buf)
        try:
            sock.sendto(buf.encode(), (arguments.host_ip, arguments.host_port))
        except socket.error as msg:
            print("Failed to send data...Exiting...")
            sys.exit(-1)
            
        try:
            buf, addr = sock.recvfrom(1000)
            print('Received data from server:', buf.decode())
            if buf.decode().find("***identified***") >= 0:
                break
        except socket.error as msg:
            print("didn't get response from server...")


    currentStep = 0
    
    while True:
        # wait for an answer from server
        buf = None
        try:
            buf, addr = sock.recvfrom(1000)
        except socket.error as msg:
            print("didn't get response from server...")
        
        if verbose:
            print('Received: ', buf)
        
        if buf != None and buf.decode().find('***shutdown***') >= 0:
            d.onShutDown()
            shutdownClient = True
            print('Client Shutdown')
            break
        
        if buf != None and buf.decode().find('***restart***') >= 0:
            d.onRestart()
            print('Client Restart')
            break
        currentStep += 1
        if currentStep != arguments.max_steps:
            if buf != None:
                buf = d.drive(buf.decode())
                # print(buf)
                # if d.upwards == 1:
                #    key="Up"
                # elif d.downwards == 1:
                #     key="Down"
                # elif d.right == 1:
                #     key="Right"
                # elif d.left == 1:
                #     key="Left"
                # list1.append(key) 
                list1.append(d.state.angle)
                # list1.append(d.state.curLapTime)
                # list1.append(d.state.damage)
                # list1.append(d.state.distFromStart)
                # list1.append(d.state.distRaced)
                # list1.append(d.state.fuel)
                # list1.append(d.state.opponents)
                # list1.append(d.state.rpm)
                # list1.append(d.state.speedX)
                # list1.append(d.state.speedY)
                # list1.append(d.state.speedZ)
                # list1.append(d.state.track)
                list1.append(d.state.trackPos)
                list1.append(d.control.accel)
                # list1.append(d.control.brake)
                # list1.append(d.control.gear)
                list1.append(d.control.steer)
                # list1.append(d.control.clutch)
                # list1.append(d.control.focus)
                # list1.append(d.control.meta)
                list2.append(list1)
                yp=np.array(list1)
                # print("the yp is : ",yp)
                # print(type(yp))

                two_dim_arr = yp.reshape(1, 4)
                # print(two_dim_arr)
                # print(type(two_dim_arr))

                y1=tree.prediction(two_dim_arr,clf_gini)
                # print("the y1 is : ",y1)
                d.next_stage = y1[0]#randint(1, 4)
                list1=[]
        else:
            buf = '(meta 1)'
        
        if verbose:
            print('Sending: ', buf)
        
        if buf != None:
            try:
                sock.sendto(buf.encode(), (arguments.host_ip, arguments.host_port))
            except socket.error as msg:
                print("Failed to send data...Exiting...")
                sys.exit(-1)
        # with open('lap9.csv', 'w', encoding='UTF8', newline='') as f:
        #     writer = csv.writer(f)
        #     # writer.writerow(header)
        #     writer.writerows(list2)
            
        # f.close()

    if curEpisode == arguments.max_episodes:
        shutdownClient = True
    curEpisode += 1

        

sock.close()

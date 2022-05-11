from sklearn import model_selection 

from sklearn.linear_model import LogisticRegression 

import xgboost 

from sklearn import preprocessing 

import pickle 

from sklearn.metrics import plot_confusion_matrix, accuracy_score 

import pandas as pd  

 
 

def turn_orgs_to_bots(df):   

  df[df['labels'] == 2] = 0   

  return df 

   

def logisticRegression(): 

 

master_df = pd.read_csv("train_test_data.csv") 

 

df = turn_orgs_to_bots(master_df) 

# features  

x1 = bots_humans.drop(['labels', 'id'], axis=1).values 

 
 

# labels 

y1 = bots_humans['labels'].values 

X_train, X_test, Y_train, Y_test = model_selection.train_test_split(x1, y1, test_size=0.30, random_state=100) 

 
 

X_train_scaled = preprocessing.scale(X_train) 

X_test_scaled = preprocessing.scale(X_test) 

model = LogisticRegression() 

model.fit(X_train_scaled, Y_train) 

result = model.score(X_test_scaled, Y_test) 

print("Accuracy: %.2f%%" % (result * 100.0)) 

 
 

logisticRegression() 

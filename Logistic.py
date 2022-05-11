from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import xgboost
from sklearn import preprocessing
import pickle
from sklearn.metrics import plot_confusion_matrix, accuracy_score
import pandas as pd 
import scipy 
from scipy import stats 
import numpy as np
import matplotlib.pyplot as plt

def turn_orgs_to_bots(df):  
  df[df['label'] == 2] = 0  
  return df
  
def logisticRegression():
	
	master_df = pd.read_csv(r'C:InsertFileLocation.csv')
	
	#df = turn_orgs_to_bots(master_df)
	# features 
	x1 = master_df.drop(['label'], axis=1).values

	# labels
	y1 = master_df['label'].values
	X_train, X_test, Y_train, Y_test = model_selection.train_test_split(x1, y1, test_size=0.30, random_state=100)

	X_train_scaled = preprocessing.scale(X_train)
	X_test_scaled = preprocessing.scale(X_test)
	model = LogisticRegression()
	model.fit(X_train_scaled, Y_train)
	result = model.score(X_test_scaled, Y_test)
	return result
    #print("Accuracy: %.2f%%" % (result * 100.0))
 


def remove_outliers(std_dev):  
  mdf = pd.read_csv(r'C:InsertFileLocation.csv')  
  mdf = turn_orgs_to_bots(mdf)
  columns = ["astroturf", "fake follower", "financial", "other", "overall", "self-declared", "spammer", "label"]  
  mdf= mdf[columns]
  
    # separate them by category  
  human_df = mdf[mdf["label"] == 1]  
  non_human_df = mdf[mdf["label"] == 0]  
  columns = ["astroturf", "fake follower", "financial", "other", "overall", "self-declared", "spammer"]
    # filter out the outliers  
 # CAP,astroturf,fake_follower,financial,other,overall,self-declared  
  #columns = ["astroturf", "fake follower", "financial", "other", "overall", "self-declared", "spammer"]  
  #for humans in columns : ["astroturf", "fake follower", "financial", "other", "overall", "self-declared"]  
  #columns_list = ["astroturf", "overall", "spammer",]
  human_df = human_df[np.abs(stats.zscore(human_df[columns]) < std_dev).all(axis=1)]  
  
    # for non_humans  
  non_human_df = non_human_df[np.abs(stats.zscore(non_human_df[columns]) < std_dev).all(axis=1)]  
  
    #print(human_df.describe())  
  #print(non_human_df.describe())  
  
    # combine both of the dataframe and export  
  master = pd.concat([human_df, non_human_df])  
  
    #print(master.describe())  
  master.to_csv(r'C:InsertFileLocation.csv', index=False)

std_dev = 2.8
std_dev_list = []
results_list = []
while std_dev >= 0:
    std_dev_list.append(std_dev)
    remove_outliers(std_dev)
    result = logisticRegression()
    result *= 100
    results_list.append(float("{:.2f}".format(result)))
    std_dev -= 0.1

plt.plot(std_dev_list, results_list)
plt.xlabel('standard deviation')
plt.ylabel('accurary %')
plt.show()

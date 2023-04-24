# -*- coding: utf-8 -*-
"""RaviTask2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UIeG6bRWZCQ4n5SW-yPvkagjwEmK-Jw9
"""

# Commented out IPython magic to ensure Python compatibility.
from io import IncrementalNewlineDecoder
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
# %matplotlib inline 
import seaborn as sns
import sklearn 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier,RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import RandomizedSearchCV
import imblearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

"""# New Section"""

dataset= pd.read_csv('/content/flightdata.csv')
dataset.head()

dataset.info()

dataset = dataset.drop('Unnamed: 25', axis=1)
dataset.isnull().sum()

dataset = dataset[{"FL_NUM","MONTH","DAY_OF_MONTH","DAY_OF_WEEK","ORIGIN","DEST","CRS_ARR_TIME","DEP_DEL15","ARR_DEL15"}]
dataset.isnull().sum()

dataset[dataset.isnull().any(axis=1)].head(10)

dataset['DEP_DEL15'].mode()

dataset = dataset.fillna({'ARR_DEL15': 1})
dataset = dataset.fillna({'DEP_DEL15': 0})
dataset.iloc[177:185]

import math

for index, row in dataset.iterrows():
    dataset.loc[index,'CRS_ARR_TIME']=math.floor(row['CRS_ARR_TIME']/100)
dataset.head()

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
dataset['DEST']=le.fit_transform(dataset['DEST'])
dataset['ORIGIN']=le.fit_transform(dataset['ORIGIN'])
dataset.head(5)

dataset['ORIGIN'].unique()

dataset = pd.get_dummies(dataset, columns=['ORIGIN', 'DEST'])
dataset.head()

x = dataset.iloc[:, 0:8].values
y = dataset.iloc[:, 8:9].values
x

from sklearn.preprocessing import OneHotEncoder
oh = OneHotEncoder()
z=oh.fit_transform(x[:,4:5]).toarray()
t=oh.fit_transform(x[:,5:6]).toarray()
z

t

x=np.delete(x,[4,5],axis=1)
x

"""# New Section"""

dataset.describe()

sns.distplot(dataset.MONTH)

sns.scatterplot (x='ARR_DELAY',y='ARR_DEL15',data=dataset)

sns.catplot(x="ARR_DEL15",y="ARR_DELAY",kind='bar',data=dataset)

sns.heatmap(dataset.corr())

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split (x,y,test_size=0.2,random_state=0)

x_test.shape

x_train.shape

y_test.shape

y_train.shape

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

"""# New Section"""

from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(random_state=0)
classifier.fit(x_train,y_train)

decisiontree = classifier.predict(x_test)

decisiontree

from sklearn.metrics import accuracy_score
desacc = accuracy_score(y_test,decisiontree)

from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=10,criterion='entropy')

rfc.fit(x_train,y_train)

y_predict = rfc.predict(x_test)

import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

classification=Sequential()
classification.add(Dense(30,activation='relu'))
classification.add(Dense(128,activation='relu'))
classification.add(Dense(64,activation='relu'))
classification.add(Dense(32,activation='relu'))
classification.add(Dense(1,activation='sigmoid'))

classification.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

classification.fit(x_train,y_train,batch_size=4,validation_split=0.2,epochs=100)

y_pred=classifier.predict ([[129,99,1,0,0,1,0,1]])
print(y_pred)
(y_pred)

y_predict = rfc.predict ([[129,99,1,0,0,1]])
print(y_pred)
(y_pred)

classification.save ('flihgt.h5')

y_pred = classification.predict(x_test)

y_pred

y_pred = (y_pred > 0.5)
y_pred

def predict_exit(sample_value):
  sample_value = np.array(sample_value)
  sample_value = sample_value.reshape(1,-1)
  sample_value = sc.transform(sample_value)
  return classifier.predict(sample_value)

test=classification.predict([[1,1,121.000000,36.0,0,0]])
if test==1:
  print('Prediction: Chance of delay')
else:
  print('prediction: No chance of delay.')

from sklearn import model_selection
from sklearn.neural_network import MLPClassifier

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import KFold, cross_validate
from sklearn.metrics import classification_report

dfs = []
models = [
    ('RF', RandomForestClassifier()),
    ('DecisionTree', DecisionTreeClassifier()),
    ('ANN', MLPClassifier())
]
results = []
names = []
scoring = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted', 'roc_auc']
target_names = ['no delay', 'delay']
for name, model in models:
    kfold = KFold(n_splits=5, shuffle=True, random_state=90210)
    cv_results = cross_validate(model, x_train, y_train, cv=kfold, scoring=scoring)
    clf = model.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    print(name)
    print(classification_report(y_test, y_pred, target_names=target_names))
    results.append(cv_results)
    names.append(name)
    this_df = pd.DataFrame(cv_results)
    this_df['model'] = name
    dfs.append(this_df)
final = pd.concat(dfs, ignore_index=True)

y_predict_train = model.predict(x_train)
train_accuracy = accuracy_score(y_train, y_predict_train)
print('Training accuracy:', train_accuracy)
y_predict_test = model.predict(x_test)
test_accuracy = accuracy_score(y_test, y_predict_test)
print('Testing accuracy:', test_accuracy)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_predict)
cm

from sklearn.metrics import accuracy_score
desacc = accuracy_score(y_test,decisiontree)

desacc

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,decisiontree)

cm

from sklearn.metrics import accuracy_score,classification_report
y_pred = model.predict(x_test)
score = accuracy_score(y_test, y_pred)
print('The accuracy for ANN model is: {}%'.format(score*100))

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_pred)
cm

parameters = {
               'n_estimators': [1,20,30,55,68,74,90,120,115],
                'criterion':['gini','entropy'],
                'max_features':["auto","sprt","log2"],
        'max_depth':[2,5,8,10],'verbose':[1,2,3,4,6,8,9,10]
}

RCV = RandomizedSearchCV(estimator=rfc,param_distributions=parameters,cv=10,n_iter=4)

RCV.fit(x_train,y_train)

model = RandomForestClassifier(verbose=10, n_estimators=120,max_features='log2',max_depth=10,criterion='entropy')
RCV.fit(x_train,y_train)

y_predict_rf = RCV.predict(x_test)

RFC=accuracy_score(y_test,y_predict_rf)
RFC

import pickle
pickle.dump(RCV,open('flight.pkl','wb'))
# -*- coding: utf-8 -*-
"""Health Mental Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CzFfuiH4YXcceqJekQR7huc0WCuGZ2kM
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)

from google.colab import files
uploaded = files.upload()

df = pd.read_csv('survey.csv')
df.head(7)

df.info()

df.isnull().sum()

df['state'].value_counts(ascending=False)[:1]

df['work_interfere'].value_counts(ascending=False)[:1]

df['self_employed'].value_counts()[:1]

df['state'].fillna('CA', inplace=True)
df['work_interfere'].fillna('Sometimes', inplace=True)
df['self_employed'].fillna('No', inplace=True)

df.isnull().sum()

df.drop(['comments'], axis=1, inplace=True)

df.head(7)

for col in df.iloc[:,2:].columns:
  print(col)
  print(df[col].value_counts())
  print('*'*120)

df['Gender'] = df['Gender'].replace('male', 'Male')
df['Gender'] = df['Gender'].replace('man', 'Male')
df['Gender'] = df['Gender'].replace('Man', 'Male')
df['Gender'] = df['Gender'].replace('m', 'Male')
df['Gender'] = df['Gender'].replace('M', 'Male')
df['Gender'] = df['Gender'].replace('female', 'Female')
df['Gender'] = df['Gender'].replace('Woman', 'Female')
df['Gender'] = df['Gender'].replace('woman', 'Female')
df['Gender'] = df['Gender'].replace('f', 'Female')
df['Gender'] = df['Gender'].replace('F', 'Female')

def gender_check(gender):
  if  gender == 'Female' or gender == 'Male':
    return gender
  else:
    return 'Other'

df['Gender'] = df['Gender'].apply(gender_check)

df['Gender'].value_counts()

sns.countplot(df['Gender'], palette='Set2')

plt.show()

df['no_employees'].value_counts()

df['no_employees'] = df['no_employees'].map({'1-5':1, '6-25':2, '26-100':3, '100-500':4, '500-1000':5, 'More than 1000':6})

df['no_employees'].value_counts()

sns.countplot(df, y='no_employees', palette='Set2')

plt.show()

df.drop(['Timestamp'], axis=1, inplace=True)

cat_cols = df.select_dtypes(include='object').columns
cat_cols

dummy_var = pd.get_dummies(df[cat_cols],dtype=int,drop_first=True)
dummy_var.head(7)

sns.heatmap(dummy_var.corr(), annot=True)

X = dummy_var.drop(['treatment_Yes'], axis=1)
y= dummy_var['treatment_Yes']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

def models(X_train, y_train):
  from sklearn.linear_model import LogisticRegression
  log = LogisticRegression(random_state=0)
  log.fit(X_train, y_train)

  from sklearn.neighbors import KNeighborsClassifier
  knn = KNeighborsClassifier()
  knn.fit(X_train, y_train)

  from sklearn.svm import SVC
  svc = SVC(kernel='linear', random_state=0)
  svc.fit(X_train, y_train)

  from sklearn.naive_bayes import GaussianNB
  gauss = GaussianNB()
  gauss.fit(X_train, y_train)

  print('Logistic Regression Training Accuracy:', log.score(X_train, y_train))
  print('K Nearest Neighbor Training Accuracy:', knn.score(X_train, y_train))
  print('Support Vector Machine (Linear Classifier) Training Accuracy:', svc.score(X_train, y_train))
  print('Naive Bayes Training Accuracy:', gauss.score(X_train, y_train))

  return log, knn, svc, gauss

models = models(X_train, y_train)

from sklearn.metrics import confusion_matrix
for i in range(len(models)):
  cm = confusion_matrix(y_test, models[i].predict(X_test))
  TP = cm[0][0]
  TN = cm[1][1]
  FN = cm[1][0]
  FP = cm[0][1]
  print(f'{models[i]}')
  print('Testing Accuracy is', (TP + TN) / (TP + TN + FN + FP))
  print()

from sklearn.model_selection import cross_val_score

cv_score = []
for i in range(len(models)):
    cvs = cross_val_score(models[i], X, y, cv=5)
    cv_score.append(cvs.mean())
    print(f'{models[i]}')
    print(cvs)
    print(cvs.mean())
    print()

models = pd.DataFrame(cv_score, index=models, columns=['Cross Validation Scores']).sort_values(by='Cross Validation Scores', ascending=False)
models
















# -*- coding: utf-8 -*-
"""Mohsin_Modeling_Sentiment (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Bsi9D1iP3VJDaLJGtLHEtigQYFJtvDLY
"""

from google.colab import drive
drive.mount('/content/drive')

pip install nltk

import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

nltk.download('vader_lexicon')

df1 = pd.read_csv('./drive/MyDrive/Russia-Ukraine War Tweets/Piyush/0313_2022_clean.csv', encoding='utf-8', error_bad_lines=False, nrows=10000)
df2 = pd.read_csv('./drive/MyDrive/Russia-Ukraine War Tweets/Piyush/0314_2022_clean.csv', error_bad_lines=False)
df3 = pd.read_csv('./drive/MyDrive/Russia-Ukraine War Tweets/Piyush/0315_2022_clean.csv', error_bad_lines=False)
df4 = pd.read_csv('./drive/MyDrive/Russia-Ukraine War Tweets/Piyush/0316_2022_clean.csv', error_bad_lines=False)
df5 = pd.read_csv('./drive/MyDrive/Russia-Ukraine War Tweets/Piyush/0317_2022_clean.csv', error_bad_lines=False)
df6 = pd.read_csv('./drive/MyDrive/Russia-Ukraine War Tweets/Piyush/0318_2022_clean.csv', error_bad_lines=False)

import csv

file_path = './drive/MyDrive/Russia-Ukraine War Tweets/Piyush/0313_2022_clean.csv'
df1 = pd.DataFrame()
date = []
text = []
with open(file_path, 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    try:
      for row in csv_reader:
        date.append(row[1])
        text.append(row[2])
    except:
      pass
df1['Date'] = date
df1['text'] = text

file_path = './drive/MyDrive/Russia-Ukraine War Tweets/Piyush/0314_2022_clean.csv'
df2 = pd.DataFrame()
date = []
text = []
with open(file_path, 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    try:
      for row in csv_reader:
        date.append(row[1])
        text.append(row[2])
    except:
      pass
df2['Date'] = date
df2['text'] = text

file_path = './drive/MyDrive/Russia-Ukraine War Tweets/Piyush/0315_2022_clean.csv'
df3 = pd.DataFrame()
date = []
text = []
with open(file_path, 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    try:
      for row in csv_reader:
        date.append(row[1])
        text.append(row[2])
    except:
      pass
df3['Date'] = date
df3['text'] = text

file_path = './drive/MyDrive/Russia-Ukraine War Tweets/Piyush/0316_2022_clean.csv'
df4 = pd.DataFrame()
date = []
text = []
with open(file_path, 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    try:
      for row in csv_reader:
        date.append(row[1])
        text.append(row[2])
    except:
      pass
df4['Date'] = date
df4['text'] = text

file_path = './drive/MyDrive/Russia-Ukraine War Tweets/Piyush/0317_2022_clean.csv'
df5 = pd.DataFrame()
date = []
text = []
with open(file_path, 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    try:
      for row in csv_reader:
        date.append(row[1])
        text.append(row[2])
    except:
      pass
df5['Date'] = date
df5['text'] = text

file_path = './drive/MyDrive/Russia-Ukraine War Tweets/Piyush/0318_2022_clean.csv'
df6 = pd.DataFrame()
date = []
text = []
with open(file_path, 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    try:
      for row in csv_reader:
        date.append(row[1])
        text.append(row[2])
    except:
      pass
df6['Date'] = date
df6['text'] = text

f_data = pd.concat([df1,df2,df3,df4,df5,df6])

sa = SentimentIntensityAnalyzer()

def get_sentiment_scores(text):
    sentiment = sa.polarity_scores(text)
    return sentiment['compound']

f_data['text'] = f_data['text'].fillna('')
f_data['sentiment'] = f_data['text'].apply(get_sentiment_scores)

f_data.head()

def categorize_sentiment(score):
    if score >= 0.05:
        return 1
    else:
        return 0

f_data['sentiment_category'] = f_data['sentiment'].apply(categorize_sentiment)

f_data.head()

from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


X_train, X_val, y_train, y_val = train_test_split(f_data['text'], f_data['sentiment_category'], test_size=0.2, random_state=42)


tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_val_tfidf = tfidf_vectorizer.transform(X_val)

# Define the parameter distributions
param_dist = {'C': uniform(0.001, 1000)}

logreg = LogisticRegression()

# Use RandomizedSearchCV
random_search = RandomizedSearchCV(logreg, param_distributions=param_dist, n_iter=10, cv=5, n_jobs=-1, scoring='accuracy')
random_search.fit(X_train_tfidf, y_train)

# Get best hyperparameters and best model
best_params_random = random_search.best_params_
print(f"Best Hyperparameters: {best_params_random}")

best_model_random = random_search.best_estimator_
y_val_pred_random = best_model_random.predict(X_val_tfidf)
accuracy_random = accuracy_score(y_val, y_val_pred_random)
print(f'Accuracy on validation set (Random Search): {accuracy_random:.2f}')

# Plotting results
param_values_random = random_search.cv_results_['params']
accuracy_values_random = random_search.cv_results_['mean_test_score']

fig, ax = plt.subplots()
for i, param_value in enumerate(param_values_random):
    ax.scatter(i, accuracy_values_random[i], label=str(param_value))

ax.set_xticks(range(len(param_values_random)))
ax.set_xticklabels([str(param_value) for param_value in param_values_random], rotation=45, ha='right')
ax.set_xlabel('Hyperparameters')
ax.set_ylabel('Mean Accuracy')
ax.set_title('Hyperparameter Tuning Results (Random Search)')
ax.legend()
plt.show()

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score

# Assuming 'f_data' is your dataset
subset_data = f_data.sample(n=1000, random_state=42)  # Creating a subset of 1000 samples

X_train, X_val, y_train, y_val = train_test_split(subset_data['text'], subset_data['sentiment_category'], test_size=0.2, random_state=42)

tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_val_tfidf = tfidf_vectorizer.transform(X_val)

# Tuning SVM
svm = SVC()
param_grid_svm = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 200, 500, 1000], 'kernel': ['linear', 'rbf']}
grid_search_svm = GridSearchCV(svm, param_grid_svm, cv=5, scoring='accuracy', n_jobs=-1)
grid_search_svm.fit(X_train_tfidf, y_train)
best_params_svm = grid_search_svm.best_params_
print(f"Best SVM Hyperparameters: {best_params_svm}")

# Tuning KNN
knn = KNeighborsClassifier()
param_grid_knn = {'n_neighbors': [3, 5, 7, 9, 15, 20, 50]}
grid_search_knn = GridSearchCV(knn, param_grid_knn, cv=5, scoring='accuracy', n_jobs=-1)
grid_search_knn.fit(X_train_tfidf, y_train)
best_params_knn = grid_search_knn.best_params_
print(f"Best KNN Hyperparameters: {best_params_knn}")

# Training Perceptron
perceptron = Perceptron()
perceptron.fit(X_train_tfidf, y_train)

# Model Evaluation
svm_y_val_pred = grid_search_svm.best_estimator_.predict(X_val_tfidf)
svm_accuracy = accuracy_score(y_val, svm_y_val_pred)
print(f'SVM Accuracy on validation set: {svm_accuracy:.2f}')

knn_y_val_pred = grid_search_knn.best_estimator_.predict(X_val_tfidf)
knn_accuracy = accuracy_score(y_val, knn_y_val_pred)
print(f'KNN Accuracy on validation set: {knn_accuracy:.2f}')

perceptron_y_val_pred = perceptron.predict(X_val_tfidf)
perceptron_accuracy = accuracy_score(y_val, perceptron_y_val_pred)
print(f'Perceptron Accuracy on validation set: {perceptron_accuracy:.2f}')

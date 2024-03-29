# -*- coding: utf-8 -*-
"""Copy of Copy of Sentiment results.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SeTSV1_qHwD6K8As1Vx8a8PUhkzfzvPo
"""

from google.colab import drive
drive.mount('/content/drive')

pip install statsmodels==v0.12.0

pip install plotly==v4.14.3

"""# General results"""

import pandas as pd
import numpy as np
import re
import nltk
nltk.download('stopwords')

import matplotlib.pyplot as plt
import plotly.express as ex
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
plt.rc('figure',figsize=(17,13))

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from wordcloud import WordCloud,STOPWORDS

from statsmodels.tsa.seasonal import seasonal_decompose

print(pd.__version__)
print(np.__version__)
print(nltk.__version__)
import wordcloud
print(wordcloud.__version__)
import statsmodels
print(statsmodels.__version__)

df1 = pd.read_csv('/content/drive/MyDrive/data/0325_2022_clean.csv')
df2 = pd.read_csv('/content/drive/MyDrive/data/0326_2022_clean.csv')
df3 = pd.read_csv('/content/drive/MyDrive/data/0327_2022_clean.csv')
df4 = pd.read_csv('/content/drive/MyDrive/data/0328_2022_clean.csv')
df5 = pd.read_csv('/content/drive/MyDrive/data/0329_2022_clean.csv')
df6 = pd.read_csv('/content/drive/MyDrive/data/0330_2022_clean.csv')
df7 = pd.read_csv('/content/drive/MyDrive/data/0331_2022_clean.csv')

f_data = pd.concat([df1,df2,df3,df4,df5,df6,df7])

f_data.head()

f_data['date'] = pd.to_datetime(f_data['date'])
f_data = f_data.sort_values(by='date')
f_data = f_data.reset_index().drop(columns=['index'])

f_data.head()

f_data = f_data.reset_index().drop(columns=['index'])
f_data

f_data = f_data.drop_duplicates(subset=['text'])
len(f_data)

df_mean = f_data.groupby(by='date').mean().reset_index()

fig = make_subplots(rows=1, cols=1)

df_mean

fig.add_trace(go.Scatter(x=df_mean['date'],y=df_mean['Positive Sentiment'],name='Positive Sentiment Trend'),
    row=1, col=1)
fig.add_trace(go.Scatter(x=df_mean['date'],y=df_mean['Negative Sentiment'],name='Negative Sentiment Trend'),
    row=1, col=1)

fig.update_layout(height=600, width=1100, title_text="Daily Avearge Trend",xaxis_title="Time",yaxis_title="Sentiment Score",
               legend=dict(yanchor="top",xanchor="right"),font = dict(size = 15))

fig.update_xaxes(ticktext=["2022-03-25","2022-03-25","2022-03-25", "2022-03-25", "2022-03-25", "2022-03-25","2022-03-25"],
                tickvals=["2022-03-25","2022-03-25","2022-03-25", "2022-03-25", "2022-03-25", "2022-03-25","2022-03-25"],
)

fig.show()

polarity = []
for i in range(len(f_data)):
    if f_data['Compound'].iloc[i] > 0.001:
        if f_data['Positive Sentiment'].iloc[i] > 0.5:
            re = 'Highly Positive'
        else:
            re = 'Positive'
    elif f_data['Compound'].iloc[i] < -0.001:
        if f_data['Negative Sentiment'].iloc[i] > 0.5:
            re = 'Highly Negative'
        else:
            re = 'Negative'
    else:
        re = 'Neutral'
    polarity.append(re)

f_data['Polarity'] = polarity

f_data['Polarity'].value_counts()

df_polarity = f_data['Polarity'].value_counts().to_frame()

fig = make_subplots(rows=1, cols=1)

fig.add_trace(go.Bar(y=df_polarity['Polarity'],x=df_polarity.index,name='Positive Sentiment Trend',text = df_polarity['Polarity']),
    row=1, col=1)

fig.update_yaxes(title_text="Tweets Counts")
fig.update_xaxes(title_text="Sentiment Polarity")
#fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_traces(textposition='outside')
fig.update_layout(height=650, width=900, title_text="Distribution of 5 Polarity Categories",font = dict(size = 15))

pos = f_data[f_data['Polarity'] == 'Positive']
hpos = f_data[f_data['Polarity'] == 'Highly Positive']
neu = f_data[f_data['Polarity'] == 'Neutral']
neg = f_data[f_data['Polarity'] == 'Negative']
hneg = f_data[f_data['Polarity'] == 'Highly Negative']

pos_all = pd.concat([pos,hpos]).sort_values(by='date')
neg_all = pd.concat([neg,hneg]).sort_values(by='date')

pos_mean = pos_all.groupby(by='date').mean().reset_index()
neg_mean = neg_all.groupby(by='date').mean().reset_index()

res_pos = seasonal_decompose(df_mean['Positive Sentiment'], period=12, model='additive', extrapolate_trend='freq')
res_neg = seasonal_decompose(df_mean['Negative Sentiment'], period=12, model='additive', extrapolate_trend='freq')

fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Scatter(x=np.arange(0,len(res_pos.trend)), y=res_pos.trend,name='Positive Trend'),
    row=1, col=1)
fig.add_trace(go.Scatter(x=np.arange(0,len(res_neg.trend)), y=res_neg.trend,name='Negative Trend'),
    row=1, col=1)

fig.update_layout(height=450, width=750, title_text="Trend of Positive&Negative",legend=dict(yanchor="top",xanchor="right"),font = dict(size = 15))
fig.update_yaxes(title_text="Daily Average Sentiment Score")
fig.update_xaxes(title_text="Time")

fig.update_xaxes(
    ticktext=["2020-12-14","2021-01-03","2021-01-23","2021-02-12","2021-03-04","2021-03-24","2021-04-14",'2021-04-30'],
    tickvals=["0","20","40","60","80","100","121",'137'])

fig.show()

df_res = pd.DataFrame({'res_pos':res_pos.trend,'res_neg':res_neg.trend})
df_res.to_excel('/content/drive/Shareddrives/Wen_Vaccine_Kaggle/replicate/figure4.xlsx',index=False)

from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['amp','covidvaccine','Äôs','Äôt','shit','fuck','vaccine','covid','covid19','covid19vaccine'])

Positive_text = ' '.join(pos.text)
Negative_text = ' '.join(neg.text)

pwc = WordCloud(stopwords=stop_words,width=600,height=400,collocations = False,random_state=11).generate(Positive_text)
nwc = WordCloud(stopwords=stop_words,width=600,height=400,collocations = False,random_state=11).generate(Negative_text)

plt.subplot(1,2,1)
plt.title('Common Words Among Positive Tweets',fontsize=16,fontweight='bold')
plt.imshow(pwc)
plt.axis('off')
plt.subplot(1,2,2)
plt.title('Common Words Among Negative Tweets',fontsize=16,fontweight='bold')
plt.imshow(nwc)
plt.axis('off')

plt.show()

pos_wordfreq = pwc.words_
neg_wordfreq = nwc.words_

df_pos_wordfreq = pd.DataFrame.from_dict(pos_wordfreq, orient='index')
df_neg_wordfreq = pd.DataFrame.from_dict(neg_wordfreq, orient='index')
df_pos_wordfreq.to_excel('/content/drive/Shareddrives/Wen_Vaccine_Kaggle/replicate/pos_wordfreq.xlsx')
df_neg_wordfreq.to_excel('/content/drive/Shareddrives/Wen_Vaccine_Kaggle/replicate/neg_wordfreq.xlsx')

pos_wordcounts = WordCloud(stopwords=stop_words,width=600,height=400,collocations = False).process_text(Positive_text)
neg_wordcounts = WordCloud(stopwords=stop_words,width=600,height=400,collocations = False).process_text(Negative_text)

df_pos_wordfreq = pd.DataFrame.from_dict(pos_wordcounts, orient='index')
df_neg_wordfreq = pd.DataFrame.from_dict(neg_wordcounts, orient='index')
df_pos_wordfreq.to_csv('/content/drive/Shareddrives/Wen_Vaccine_Kaggle/replicate/pos_wordcounts.csv')
df_neg_wordfreq.to_csv('/content/drive/Shareddrives/Wen_Vaccine_Kaggle/replicate/neg_wordcounts.csv')

h_Positive_text = ' '.join(hpos.text)
h_Negative_text = ' '.join(hneg.text)


h_pwc = WordCloud(stopwords=stop_words,width=600,height=400,collocations = False).generate(h_Positive_text)
h_nwc = WordCloud(stopwords=stop_words,width=600,height=400,collocations = False).generate(h_Negative_text)

plt.subplot(1,2,1)
plt.title('Common Words Among Highly Positive Tweets',fontsize=16,fontweight='bold')
plt.imshow(pwc)
plt.axis('off')
plt.subplot(1,2,2)
plt.title('Common Words Among Highly Negative Tweets',fontsize=16,fontweight='bold')
plt.imshow(nwc)
plt.axis('off')

plt.show()

hpos_wordfreq = h_pwc.words_
hneg_wordfreq = h_nwc.words_

df_hpos_wordfreq = pd.DataFrame.from_dict(hpos_wordfreq, orient='index')
df_hneg_wordfreq = pd.DataFrame.from_dict(hneg_wordfreq, orient='index')
df_hpos_wordfreq.to_excel('/content/drive/Shareddrives/Wen_Vaccine_Kaggle/replicate/hpos_wordfreq2.xlsx')
df_hneg_wordfreq.to_excel('/content/drive/Shareddrives/Wen_Vaccine_Kaggle/replicate/hneg_wordfreq2.xlsx')

hpos_wordcounts = WordCloud(stopwords=stop_words,width=600,height=400,collocations = False).process_text(h_Positive_text)
hneg_wordcounts = WordCloud(stopwords=stop_words,width=600,height=400,collocations = False).process_text(h_Negative_text)

df_hpos_wordcounts = pd.DataFrame.from_dict(hpos_wordcounts, orient='index')
df_hneg_wordcounts = pd.DataFrame.from_dict(hneg_wordcounts, orient='index')
df_hpos_wordcounts.to_csv('/content/drive/Shareddrives/Wen_Vaccine_Kaggle/replicate/hpos_wordcounts2.csv')
df_hneg_wordcounts.to_csv('/content/drive/Shareddrives/Wen_Vaccine_Kaggle/replicate/hneg_wordcounts2.csv')

f_data['month'] = pd.DatetimeIndex(f_data['date']).month
f_12 = f_data[f_data['month'] == 12]
f_1 = f_data[f_data['month'] == 1]
f_2 = f_data[f_data['month'] == 2]
f_3 = f_data[f_data['month'] == 3]
f_4 = f_data[f_data['month'] == 4]

df_month = pd.DataFrame(columns = f_1['Polarity'].value_counts().index.tolist(),
                        data = [f_12['Polarity'].value_counts().values,
                                f_1['Polarity'].value_counts().values,
                                f_2['Polarity'].value_counts().values,
                                f_3['Polarity'].value_counts().values,
                                f_4['Polarity'].value_counts().values],
                       index = ['December','January','February','March','April'])

df_month

neg_dis_byweek_main = pd.read_excel('/content/drive/Shareddrives/Wen_Vaccine_Kaggle/replicate/neg_dis_byweek_1001.xlsx')

#dis = neg_dis_byweek.set_index('Topic')
dis = neg_dis_byweek_main.iloc[:,1:]
import plotly.express as px
fig = px.imshow(dis, y=['NEG_05','NEG_00','NEG_06','NEG_04','NEG_07'],aspect='auto')
fig.update_layout(height=700, width=600,title='Main Negative Topics Evolution by Week')
fig.update_xaxes(tickangle=30)
fig.show()


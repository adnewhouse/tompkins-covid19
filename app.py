import time
from datetime import date
import requests
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set()
sns.palplot('colorblind')


# Update history database
r = requests.get('https://tompkinscountyny.gov/health')
html = r.text
dfs = pd.read_html(html, header=0)
main_data = dfs[1]
hosp_data = dfs[2]
combined = pd.concat([main_data, hosp_data], axis=1)
combined.insert(0, 'Date', [str(date.today())], True)

history = pd.read_csv('history.csv', header=0, index_col=[0])

new_history = pd.concat([history, combined], ignore_index=True)
new_history.drop_duplicates(subset=['Positive Test Results'], keep='last', inplace=True)
new_history.reset_index(drop=True, inplace=True)
new_history.to_csv('history.csv', mode='w', header=True)


# Generate Plots
history = pd.read_csv('history.csv', header=0, index_col=[0])
history.set_index('Date', inplace=True)

fig = plt.figure(dpi=300)
ax = history[['Positive Test Results']].plot.bar(title='Tompkins County Confirmed Covid-19 Cases', rot=45, ax=plt.gca())
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() + (p.get_width() / 2), p.get_height() * 1.005), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
fig.savefig('positive_cases.png', dpi=fig.dpi, bbox_inches='tight')


fig = plt.figure(dpi=300)
history[['Positive Test Results', 'Negative Test Results', 'Total Tested for COVID-19']].plot.line(title='Tompkins County Covid-19 Tests', rot=45, ax=plt.gca())
fig.savefig('tests.png', dpi=fig.dpi, bbox_inches='tight')

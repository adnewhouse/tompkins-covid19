from datetime import date
from datetime import datetime
from pytz import timezone
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os

sns.set()
sns.palplot('colorblind')

now_utc = datetime.now(timezone('UTC'))
now_eastern = now_utc.astimezone(timezone('US/Eastern'))

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
new_history.drop_duplicates(subset=['Date', 'Total Tested for COVID-19'], keep='first', inplace=True)
new_history.reset_index(drop=True, inplace=True)
new_history.to_csv('history.csv', mode='w', header=True)


# Generate Plots
history = pd.read_csv('history.csv', header=0, index_col=[0], parse_dates=['Date'])
history.set_index('Date', inplace=True)

fig, ax = plt.subplots()
ax.plot(history.index, history['Positive Test Results'], 'o-')
ax.set(
        title='Tompkins County Confirmed Covid-19 Cases',
        xlabel='Date',
        ylabel='Cases')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax.tick_params(axis='x', rotation=60)
fig.savefig('positive_cases.png', dpi=300, bbox_inches='tight')


'''
fig = plt.figure(dpi=300)
history[['Positive Test Results', 'Negative Test Results', 'Total Tested for COVID-19']].plot.line(title='Tompkins County Covid-19 Tests', rot=45, ax=plt.gca())
fig.savefig('tests.png', dpi=fig.dpi, bbox_inches='tight')

ax = sns.lineplot(data=history)
fig = ax.get_figure()
fig.savefig("output.png")
'''

# Push updates
os.system('git commit -am \'Update at ' + now_eastern.strftime("%d/%m/%Y %H:%M:%S") + '\'')
os.system('git push')

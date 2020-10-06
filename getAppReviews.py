#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
from tqdm import tqdm

import seaborn as sns
import matplotlib.pyplot as plt

import urllib.request
from bs4 import BeautifulSoup

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from google_play_scraper import Sort, reviews, app


# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format='retina'")

sns.set(style='whitegrid', palette='muted', font_scale=1.2)


# In[3]:


fname = r'C:\Users\srinivasan.p.1\Anaconda3\html\opioid.html'
HtmlFile = open(fname, 'r', encoding='utf-8')
source_code = HtmlFile.read()

soup = BeautifulSoup(source_code, "html.parser")
soup.prettify()


# In[4]:


##get all app div tags
app_divs = []
app_packages = []

divs = soup.find_all('div',{'class':'b8cIId ReQCgd Q9MA7b'})

##Loop through each div to find the app ID
for eachdiv in divs:
    ##Retrieve app ID
    app_ID = eachdiv.find('a').get('href')
    app_packages.append(app_ID.split("/store/apps/details?id=", 1)[-1])


# In[5]:


app_reviews=[]

for ap in tqdm(app_packages):
    rvs, _ = reviews(
        ap,
        sort=Sort.MOST_RELEVANT,
        filter_score_with=5
    )
    for r in rvs:
        r['appId'] = ap
    app_reviews.extend(rvs)


# In[6]:


def print_json(json_object):
    json_str = json.dumps(
        json_object,
        indent=2,
        sort_keys=True,
        default=str
    )
    print (highlight(json_str, JsonLexer(), TerminalFormatter()))


# In[7]:


app_reviews_df = pd.DataFrame(app_reviews)
col_list = ['appId','userName','at','content','score','thumbsUpCount']
app_reviews_df[col_list].to_csv('app_reviews.csv', index=None, header=True)


# In[ ]:





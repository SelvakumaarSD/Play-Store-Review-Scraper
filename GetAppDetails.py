#!/usr/bin/env python
# coding: utf-8

# In[8]:


##import play_scraper
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


# In[9]:


get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format='retina'")

sns.set(style='whitegrid', palette='muted', font_scale=1.2)


# In[13]:


fname = r'C:\Users\srinivasan.p.1\Anaconda3\html\opioid.html'
HtmlFile = open(fname, 'r', encoding='utf-8')
source_code = HtmlFile.read()

soup = BeautifulSoup(source_code, "html.parser")
soup.prettify()


# In[14]:


##get all app div tags
app_divs = []
app_packages = []

divs = soup.find_all('div',{'class':'b8cIId ReQCgd Q9MA7b'})

##Loop through each div to find the app ID
for eachdiv in divs:
    ##Retrieve app ID
    app_ID = eachdiv.find('a').get('href')
    app_packages.append(app_ID.split("/store/apps/details?id=", 1)[-1])

##first 4 apps from the search hit of substance use disorder keyword
##app_packages=[
##    'com.mobileapp.production',
##    'com.recoverypath',
##    'com.getpocketrehab.app',
##    'drug.addiction.therapy'
##]


# In[15]:


app_infos=[]
for ap in tqdm(app_packages):
    info=app(ap, lang='en', country='us')
    del info['comments']
    app_infos.append(info)


# In[16]:


def print_json(json_object):
    json_str = json.dumps(
        json_object,
        indent=2,
        sort_keys=True,
        default=str
    )
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))


# In[17]:


app_infos_df = pd.DataFrame(app_infos)
col_list = ['title','description','installs','ratings','score','reviews','genre','appId','url']
app_infos_df[col_list].to_csv('app_details.csv', index=None, header=True)


# In[ ]:





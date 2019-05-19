#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
import os
import io
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
from collections import OrderedDict
import time


# In[2]:

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


# ### NASA Mars News

# In[3]:
def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)


    # In[4]:


    response = requests.get(url)


    # In[5]:


    soup = bs(response.text, 'html.parser')


    # In[6]:


    print(soup.prettify())


    # In[7]:


    html = browser.html
    soup = bs(html, 'html.parser')

    newsTitle = soup.find('div', class_='content_title').text
    newsP = soup.find('div', class_='article_teaser_body').text

    print(newsTitle)
    print(newsP)


    # ### JPL Mars Space Images - Featured Image

    # In[8]:


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)

    # In[9]:


    response = requests.get(url)


    # In[10]:


    soup = bs(response.text, 'html.parser')


    # In[11]:


    print(soup.prettify())


    # In[12]:


    html = browser.html
    soup = bs(html, 'html.parser')
    imgBase_url = 'https://www.jpl.nasa.gov'

    featuredSrc = soup.find('a', class_='button fancybox')['data-fancybox-href']

    featuredImg = f'{imgBase_url}{featuredSrc}'
    print(featuredImg)


    # ### Mars Weather

    # In[13]:


    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)

    # In[14]:


    response = requests.get(url)


    # In[15]:


    soup = bs(response.text, 'html.parser')


    # In[16]:


    print(soup.prettify())


    # In[17]:


    # <p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">InSight sol 165 (2019-05-15) low -100.3ºC (-148.6ºF) high -18.2ºC (-0.7ºF)
    # winds from the SW at 4.6 m/s (10.4 mph) gusting to 13.7 m/s (30.6 mph)
    # pressure at 7.50 hPa<a href="https://t.co/7NMgdAkFA8" class="twitter-timeline-link u-hidden" data-pre-embedded="true" dir="ltr">pic.twitter.com/7NMgdAkFA8</a></p>


    # In[18]:


    html = browser.html
    soup = bs(html, 'html.parser')

    marsWeather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    # newsTitle = soup.find('div', class_='content_title')
    # newsP = soup.find('div', class_='article_teaser_body')

    print(marsWeather)


    # ### Mars Facts

    # In[19]:


    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(1)

    # In[20]:


    response = requests.get(url)


    # In[21]:


    soup = bs(response.text, 'html.parser')


    # In[22]:


    print(soup.prettify())


    # In[23]:


    html = browser.html
    soup = bs(html, 'html.parser')

    marsTable = soup.find('table')

    print(marsTable)


    # In[24]:


    description = []
    for strong_tag in marsTable.find_all('strong'):
        description.append(strong_tag.text)

    print(description)


    # In[25]:


    value =[]
    for factoid in marsTable.find_all('td', class_='column-2'):
        value.append(factoid.text)
        
    print(value)


    # In[26]:


    marsFacts = pd.DataFrame()
    marsFacts['Description'] = description
    marsFacts['Value'] = value

    marsFacts = marsFacts.set_index('Description')

    marsFacts


    # In[27]:


    str_io = io.StringIO()

    marsFacts.to_html(buf=str_io, classes='table table-striped')

    html_str = str_io.getvalue()

    print(html_str)


    # ### Mars Hemispheres

    # In[28]:


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)

    # In[29]:


    response = requests.get(url)


    # In[30]:


    soup = bs(response.text, 'html.parser')


    # In[31]:


    print(soup.prettify())


    # In[32]:


    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphereNames = []

    for hemispheres in soup.find_all('h3'):
        hemisphereNames.append(hemispheres.text)
        
    print(hemisphereNames)


    # In[33]:


    detailLinks = []

    for link in soup.find_all('a', class_= 'itemLink product-item'):
        detailLinks.append(link['href'])

    detailLinks = list(OrderedDict.fromkeys(detailLinks))

    detailLinks


    # In[34]:


    baseUrl = 'https://astrogeology.usgs.gov'
    builtLinks = []
        
    for link in detailLinks:
        builtLink = f'{baseUrl}{link}'
        builtLinks.append(builtLink)
        
    builtLinks


    # In[35]:


    imgUrls = []

    for link in builtLinks:
        browser.visit(link)
        time.sleep(1)
        response = requests.get(link)
        gazpacho = bs(response.text, 'html.parser')
        sampleLink = gazpacho.find('a', target='_blank')['href']
        imgUrls.append(sampleLink)

    imgUrls


    # In[36]:


    hemisphereImg_urls = []
    keys = ["title", "img_url"]

    zipped_pairs = list(zip(hemisphereNames, imgUrls))

    for pair in zipped_pairs:
        hemisphereImg_urls.append(dict(zip(keys, pair)))
        
    hemisphereImg_urls

    mars_data = {
        "newsTitle": newsTitle,
        "newsP": newsP,
        "featuredImg": featuredImg,
        "marsWeather": marsWeather,
        "html_str": html_str,
        "hemisphereImg_urls": hemisphereImg_urls
    }

     # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

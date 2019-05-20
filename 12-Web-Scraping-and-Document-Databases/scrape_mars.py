#!/usr/bin/env python
# coding: utf-8

# Dependencies
import os
import io
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
from collections import OrderedDict
import time
from selenium import webdriver


# ### NASA Mars News
def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    html = browser.html
    soup = bs(html, 'html.parser')

    newsTitle = soup.find('div', class_='content_title').text
    newsP = soup.find('div', class_='article_teaser_body').text

    # ### JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    html = browser.html
    soup = bs(html, 'html.parser')
    imgBase_url = 'https://www.jpl.nasa.gov'

    featuredSrc = soup.find('a', class_='button fancybox')['data-fancybox-href']

    featuredImg = f'{imgBase_url}{featuredSrc}'

    # ### Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    html = browser.html
    soup = bs(html, 'html.parser')

    marsWeather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    # ### Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    html = browser.html
    soup = bs(html, 'html.parser')

    marsTable = soup.find('table')

    description = []
    for strong_tag in marsTable.find_all('strong'):
        description.append(strong_tag.text)

    value =[]
    for factoid in marsTable.find_all('td', class_='column-2'):
        value.append(factoid.text)
    
    marsFacts = pd.DataFrame()
    marsFacts['Description'] = description
    marsFacts['Value'] = value

    marsFacts = marsFacts.set_index('Description')

    str_io = io.StringIO()

    marsFacts.to_html(buf=str_io, classes='table table-striped')

    html_str = str_io.getvalue()

    # ### Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphereNames = []

    for hemispheres in soup.find_all('h3'):
        hemisphereNames.append(hemispheres.text)
        
    detailLinks = []

    for link in soup.find_all('a', class_= 'itemLink product-item'):
        detailLinks.append(link['href'])

    detailLinks = list(OrderedDict.fromkeys(detailLinks))

    baseUrl = 'https://astrogeology.usgs.gov'
    builtLinks = []
        
    for link in detailLinks:
        builtLink = f'{baseUrl}{link}'
        builtLinks.append(builtLink)
    
    imgUrls = []

    for link in builtLinks:
        browser.visit(link)
        response = requests.get(link)
        gazpacho = bs(response.text, 'html.parser')
        sampleLink = gazpacho.find('a', target='_blank')['href']
        imgUrls.append(sampleLink)

    hemisphereImg_urls = []
    keys = ["title", "img_url"]

    zipped_pairs = list(zip(hemisphereNames, imgUrls))

    for pair in zipped_pairs:
        hemisphereImg_urls.append(dict(zip(keys, pair)))
        
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

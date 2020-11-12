#!/usr/bin/env python
# coding: utf-8

# In[7]:


from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():
    # Set up browser with chromedriver
    
    executable_path = {'executable_path':'C:\webdrivers\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser


# In[8]:


#  Mission to Mars dictionary that can be imported into Mongo
mars_info = {}


# In[9]:



#  MARS NEWS
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

    

        # Visit Nasa url through splinter 
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML with bs
        soup = bs(html, 'html.parser')

        time.sleep(1)
        # Get the latest  news_title and news_p
        try:
            news_title = soup.find('div', class_='content_title').find('a').text
        except:
            news_title=""
        try:   
            news_p = soup.find('div', class_='article_teaser_body').text
        except:
            news_p=""

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()


# In[10]:


# FEATURED IMAGE
def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()

       

        # Visit Mars Space Images through splinter 
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)
        
        
        # HTML Object 
        html_image = browser.html

        # Parse HTML with bs
        soup = bs(html_image, 'html.parser')

        # Retrieve background-image url  
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate  url with scrapped route
        featured_image_url = main_url + featured_image_url

        # Link for featured image
        featured_image_url 

        # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    finally:

        browser.quit()


# In[11]:


# Mars Facts
def scrape_mars_facts():

    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Pandas `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    #  mars facts DF in the list of DF assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Mars']`
    mars_df.columns = ['Description','Mars']

    # Set the index to the `Description` 
    mars_df.set_index('Description', inplace=True)

    # Save html code 
    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = data

    return mars_info


# In[12]:


# MARS HEMISPHERES


def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemi = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for item in items: 
            # Store title
            title = item.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = item.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = bs( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemi.append({"title" : title, "img_url" : img_url})

        mars_info['hemi'] = hemi

        
        

        return mars_info
    finally:

        browser.quit()


# In[ ]:





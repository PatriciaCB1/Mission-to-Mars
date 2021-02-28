#!/usr/bin/env python
# coding: utf-8

# In[146]:


# Import Splinter and BeautifulSoup, Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[147]:


# Path to chromedriver
get_ipython().system('which chromedriver')


# In[148]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[149]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[150]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[151]:


slide_elem.find("div", class_='content_title')


# In[152]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[153]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


#  ### JPL Space Images Featured Image

# In[154]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[155]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[156]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[157]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[158]:


# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts

# In[159]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[160]:


df.to_html()


# ### Mars Weather

# In[161]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[162]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[163]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# ## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[164]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[165]:


# 2. Create a list to hold the images and titles.
hem_url = []

# click on each hemisphere link, navigate to the full-resolution image page, and retrieve the full-resolution image URL string and title for each hemisphere image.

for i in range(len(browser.find_by_tag('h3'))):   
    hem = {}
    browser.find_by_tag('h3')[i].click()
    html = browser.html
    img_soup = soup(html, 'html.parser')
    hem_url_rel = img_soup.find('img', class_='wide-image').get('src')
    hem['img_url'] = f'https://astrogeology.usgs.gov{hem_url_rel}'
    hem['title'] = browser.find_by_css('h2.title').text
    hem_url.append(hem)
    browser.back()
    


# In[166]:


# 4. Print the list that holds the dictionary of each image url and title.
hem_url


# In[167]:


# 5. Quit the browser
browser.quit()


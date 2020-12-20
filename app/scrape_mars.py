from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
import warnings

def scrape_all():
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    news_p = soup.find('div', class_='article_teaser_body').text
    

    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    

    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(featured_image_url)

    html_image = browser.html

    soup = bs(html_image, 'html.parser')

    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    main_url = 'https://www.jpl.nasa.gov'

    featured_image_url = main_url + featured_image_url


    facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)

    mars_df = mars_facts[0]


    mars_df = mars_df.rename(columns={0 : "Attribute", 1 : "Value"}).\
    set_index(["Attribute"])

    mars_df.to_html()

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemispheres_url)
    image_html = browser.html
    soup = bs( image_html, 'html.parser')

    items = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    for item in items: 
    
        title = item.find('h3').text
        
        image_url = item.find('a', class_='itemLink product-item')['href']

        browser.visit(hemispheres_main_url + image_url)

        image_html = browser.html

        soup = bs( image_html, 'html.parser')

        image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']

        hemisphere_image_urls.append({"Title" : title, "Image_URL" : image_url})

        data = {
            "news_title": news_title,
            "news_paragraph": news_p,
            "featured_image_url": image_url,
            "fatcs": mars_df,
            "hemispheres": hemisphere_image_urls
    }

    browser.quit
    return data 
if __name__ == "__main__":
    print('function executed when ran directly')
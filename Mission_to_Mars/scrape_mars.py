# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

def init_browser():
    executable_path = executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict = {}

    # Mars news URL of page to be scraped
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    # Retrieve the latest news title and paragraph
    news_title = news_soup.find_all('div', class_= 'content_title')[0].text
    news_p = news_soup.find_all('div', class_= 'article_teaser_body')[0].text

    # Mars image to be scraped
    mars_image_url = 'https://spaceimages-mars.com/'
    browser.visit(mars_image_url)
    image_html = browser.html
    images_soup = BeautifulSoup(image_html, 'html.parser')
    # Retrieve featured image link
    relative_image_path = images_soup.find_all('img')[1]['src']
    featured_image_url = mars_image_url + relative_image_path

    # Mars facts to be scraped, converted to html table
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    mars_facts_df = tables[1]
    mars_facts_df.columns = ["Description", 'Value']
    mars_html_table = mars_facts_df.to_html()
    mars_html_table.replace('\n', '')

    # Mars hemispheres name and image to be scraped
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')
    # Mars hemisphere data
    all_mars_hemis = hemi_soup.find('div', class_='collapsible results')
    mars_hemis = all_mars_hemis.find_all('div', class_='item')
    hemi_image_urls = []
    # Iterate through each hemisphere
    for i in mars_hemis:
        # Collect Title
        hemisphere = i.find('div', class_='description')
        title = hemisphere.h3.text
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]
        browser.visit(hemi_url + hemisphere_link)
        image_html2 = browser.html
        image_soup = BeautifulSoup(image_html2, 'html.parser')
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        # Create Dictionary to store Title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = hemi_url + image_url 
        hemi_image_urls.append(image_dict)

    # Mars
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemi_image_urls
    }

    return mars_dict
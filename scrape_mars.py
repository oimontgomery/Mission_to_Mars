from splinter import Browser
from bs4 import BeautifulSoup as bs
import time 
import requests
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():

    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('div', class_="slide")
    news_title = results.find('div', class_="content_title").text
    news_p = results.find('div', class_="rollover_description_inner").text
    

    url_1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars/'
    browser.visit(url_1)
    html = browser.html
    soup_1 = bs(html, 'html.parser')
    space_results = soup_1.find('li', class_="slide").find('a', class_="fancybox")['data-fancybox-href']
    featured_image_url = ['https://www.jpl.nasa.gov/' + space_results]
    

    url_2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_2)
    html = browser.html
    soup_2 = bs(html, 'html.parser')
    mars_weather = soup_2.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    

    url_3 = 'http://space-facts.com/mars/'
    tables = pd.read_html(url_3)
    mars_facts = tables[0]
    mars_facts = mars_facts.rename(columns={0: ' ', 1: 'Value'})
    mars_facts.set_index(' ', inplace=True)
    html_table = mars_facts.to_html()
    
    

    url_4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_4)
    html = browser.html
    soup_4 = bs(html, 'html.parser')
    #Look through the text to find the four intial links
    url_text = soup_4.find_all('div', class_= 'item')
    url_list = []

    for url in url_text:
        image_url = url.find('a', class_= 'itemLink product-item')['href']
        url_list.append(image_url)

    complete_urls = ['https://astrogeology.usgs.gov' + url for url in url_list]
    full_links_list = []
    url_titles = []

    for complete_url in complete_urls:
        browser.visit(complete_url)
        html_x = browser.html
        soup_x = bs(html_x, 'html.parser')
        url_title = soup_x.find('h2', class_='title').text
        url_titles.append(url_title)
        full_link = soup_x.find('img', class_= "wide-image")['src']
        full_links_list.append(full_link)

    complete_fill_links = ['https://astrogeology.usgs.gov' + complete_url for complete_url in full_links_list]


    complete_data = {
        "news_title": news_title,
        "news_description": news_p,
        "latest_image": featured_image_url,
        "latest_tweet": mars_weather,
        "html_table": html_table,
        "complete_links": complete_fill_links
    }
    # Close the browser after scraping
    browser.quit()

    # Return results
    return complete_data
from bs4 import BeautifulSoup as bs
import time
import requests
import pymongo
from splinter import Browser
import pandas as pd
import os


all_mars_info={}

def init_browser(): 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_news():

    browser=init_browser()
    news_url='https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(1)
    html=browser.html
    soup=bs(html, 'html.parser')
    paragraphs=soup.find('li', class_='slide')
    news_title=paragraphs.find('div', class_='content_title').text
    news_p=paragraphs.find('div', class_='article_teaser_body').text
    
    all_mars_info['news_title']=news_title
    all_mars_info['news_paragraph']=news_p

    browser.quit()

    return all_mars_info

def scrape_image():

    browser=init_browser()
    image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(1)
    html=browser.html
    soup=bs(html, 'html.parser')
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    new_page=browser.html
    feature_src=bs(new_page, 'html.parser')
    img_src=feature_src.find('img', class_='main_image')
    resource_name=img_src['src']
    base_url='https://jpl.nasa.gov'
    featured_image_url=base_url+resource_name

    all_mars_info['featured_image_url']=featured_image_url

    browser.quit()

    return all_mars_info

def scrape_weather():

    browser=init_browser()
    weather_url='https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(1)
    twitter=browser.html
    twitter_page=bs(twitter, 'html.parser')
    tweet=twitter_page.find('article')
    time.sleep(10)
    mars_weather=tweet.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    mars_weather=mars_weather[4].text

    all_mars_info['mars_weather']=mars_weather

    browser.quit()

    return all_mars_info

def scrape_facts():

    facts_url='https://space-facts.com/mars/'
    tables=pd.read_html(facts_url)
    df=tables[0]
    df.columns=['Fact','Value']
    df.set_index('Fact', inplace=True)
    html_table=df.to_html()
    html_table=html_table.replace('\n', '')
    
    all_mars_info['mars_facts']=html_table

    return all_mars_info

def scrape_hemispheres():

    browser=init_browser()
    hemisphere_image_urls=[]
    hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(1)
    hem=browser.html
    hems=bs(hem, 'html.parser')
    hem_dict={}
    hem_list=['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']

    for hemisphere in hem_list:
        browser.click_link_by_partial_text(f'{hemisphere} Hemisphere Enhanced')
        time.sleep(1)
        image_page=browser.html
        data=bs(image_page, 'html.parser')
        title=data.find('h2', class_='title').text
        hem_dict["title"]=title
        base_url='https://astrogeology.usgs.gov'
        add_url=data.find('img', class_='wide-image')
        add_url=add_url['src']
        full_url=base_url + add_url
        hem_dict["img_url"]=full_url
        hemisphere_image_urls.append(hem_dict)
        browser.visit(hemisphere_url)
        time.sleep(1)
        hem=browser.html
        hems=bs(hem, 'html.parser')
        hem_dict={}

    all_mars_info['hemisphere_url']=hemisphere_image_urls

    browser.quit()

    return all_mars_info


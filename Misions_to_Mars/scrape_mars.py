  
# Dependencies
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)



def scrape_info():
    browser = init_browser()

    ###  Nasa Mars news

    # Visit nasa news
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    
    # Retrieve page with the requests module
    response = requests.get(nasa_url)

    # Scrape page into Soup
    soup = bs(response.text, 'html.parser')    

    # Get the title name and the paragraphs 
    results = soup.find_all('div', class_='grid_layout')[1]
    tit = results.find("div", class_="content_title")
    news_title = tit.find('a').text

    des = results.find("div", class_="rollover_description_inner")
    news_p = des.text



    ### JPL Mars Space Images


    # JPL Nasa URL
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html,'html.parser')

    result = soup.find_all('div', class_='carousel_container')[0]
    
    # Click on Full Image button to get the featured image
    browser.find_by_id('full_image').click()

    # Get the image url
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    answer = soup.find('img', class_='fancybox-image')
    a = answer['src']
    featured_image_url = (f'https://www.jpl.nasa.gov/{a}')



    ### Mars Facts


    # Get the URL
    fact_url = 'https://space-facts.com/mars/'
    table = pd.read_html(fact_url)
    t = table[0]

    # Organize the data an form a DataFrame
    tables = pd.DataFrame(t)

    # Rename the columns and set the index
    tables.rename(columns={0:'Parameters', 1:'Values'}, inplace=True)
    tables.set_index('Parameters', inplace=True)
    mars_facts = tables.to_html()

    ### Mars Hemispheres

    # URL
    pic_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(pic_url)

    # Using splinter browser
    pic_html = browser.html 

    # BS
    soup = bs(pic_html, "html.parser")
    picture = soup.find('div', class_='collapsible results')  
    item = picture.find_all('div', class_='item')

    # Get the title and the images urls
    hemisphere_image_urls = []

    # Loop through item to get the correct URL
    for items in item:
        title = items.find('h3').text
        title = title.replace(' Enhanced','')
        im_url = items.find('a')['href']
        image_url = (f"https://astrogeology.usgs.gov{im_url}")
        browser.visit(image_url)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        pic_link = downloads.find('a')['href']
        hemisphere_image_urls.append({"title": title, "img_url": pic_link})

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

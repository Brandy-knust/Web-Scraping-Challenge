from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_info():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # NASA Mars News Site and collect the latest News Title and Paragraph Text
    url="https://mars.nasa.gov/news/"
    news_title=[]
    news_p=[]
    
    driver.get(url)
    time.sleep(3)
    html=driver.page_source
    soup = bs(html)
    item_list=soup.find(class_="item_list")
    results=item_list.find_all(class_="content_title")
    news_title=results[0].text
    news_p=soup.find(class_="article_teaser_body").text

    #Visit the url for JPL Featured Space Image
    mars_image_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"   
    driver.get(mars_image_url)
    time.sleep(3)
    html=driver.page_source
    soup=bs(html)
    img=soup.find(class_="showimg")
    for link in soup("a", "showimg", href=True):
        img_href=(link['href'])
    featured_image_url=(f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_href}')
    
    #Mars Facts webpage table
    mars_url="https://space-facts.com/mars/"
    mars_df=pd.read_html(mars_url)[0]
    mars_df.columns=["Description", "Mars"]
    mars_df.set_index("Description", inplace=True)
    html_string=mars_df.to_html()

    #Obtain high resolution images for each of Mar's hemispheres
    hemi_url=[]
    hemisphere_image_urls=[]
    hemisphere_titles=[]

    hemispheres_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    driver.get(hemispheres_url)
    time.sleep(3)
    html=driver.page_source
    soup = bs(html)
    hem_res=soup.find_all(class_="itemLink")
    soup.find_all('a', 'itemLink', href=True)
    for link in soup.find_all('a', 'itemLink', href=True):
        if link.h3: 
            hemi_url.append(link['href'])
    
    for hemi in hemi_url:
        driver.get(f"https://astrogeology.usgs.gov{hemi}")
        time.sleep(3)
        html=driver.page_source
        soup=bs(html)
        himg=soup.find(class_="downloads")
        sample_pictures=himg.find("a", text="Sample").get('href')
        sample_title=soup.find("h2", class_="title").get_text()
        hemisphere_image_urls.append(sample_pictures)
        hemisphere_titles.append(sample_title)
    hemisphere_dict = dict(zip(hemisphere_titles, hemisphere_image_urls))    

    return_data = {"LatestMarsNews":news_title, "News":news_p, "FeaturedMarsImage":featured_image_url, "MarsFacts":html_string, "MarsHemispheres": hemisphere_dict}
    driver.close()
    return return_data
    

if __name__ == "__main__":
    print(scrape_info() )
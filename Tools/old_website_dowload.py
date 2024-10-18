'''THe websites are all invalid. This module can be used as a code reference to scrape manges that images are stored as chapters.'''
import time 
import requests
import os
import pandas as pd 

from selenium.webdriver.common.by import By 
from pathvalidate import sanitize_filename
from Modules.chrome_driver_setup import setup_webdriver

def getTitlesByWebsite(website, driver):
    if website == 'Toptoonmh.com':
        page_title = driver.find_element(By.XPATH,"//header//div[contains(@class, 'ptm-pull-left')]").text
        clean_title = sanitize_filename(page_title)
    elif website == '7mj.net':
        page_title = driver.find_element(By.XPATH,"//meta[@name='title']").get_attribute("content")
        clean_title = sanitize_filename(page_title[5:])
    return clean_title
def getImgUrlByWebsite(website, driver):
    img_urls = []
    if website == '7mj.net':
        breads = driver.find_elements(By.TAG_NAME, "img")  
    elif website == 'Toptoonmh.com':    
        breads = driver.find_elements(By.XPATH, "//div[contains(@class, 'center padding5')]//img[contains(@class, 'lazyimg')]")
        
    for bread in breads:
            if website == '7mj.net':
                url = bread.get_attribute('data-src')
            elif website == 'Toptoonmh.com':   
                url = bread.get_attribute('src')
                
            if url and url[:4] == "http":
                img_urls.append(url)      
    return img_urls
    

    
def extract_images(image_urls_list:list, file_path, failed_urls):
    # Changing directory into a specific folder:
    #os.chdir(directory_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # Downloading all of the images
    for img in image_urls_list:
        file_name = file_path+img.split('/')[-1]
        
        if os.path.isfile(file_name):
            print(f"***Abort cause {img} exists")
            continue
        print(f"Downloading {img}")
        try:
            r = requests.get(img, stream=True,headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                with open(file_name, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
        except Exception as e:
            failed_urls.append([img,e])


def fetchImgUrlInChapters(file, manga_path, website, isUpdate):
    driver = setup_webdriver()
    failed_urls = []
    with open(file) as f:
        chapters = f.readlines()
    for chapter in chapters: 
        if chapter and chapter[:4] == "http":
  
            driver.get(chapter) 
            time.sleep(7)
            
            clean_title = getTitlesByWebsite(website, driver)
            chapter_path = manga_path+clean_title+"/" 
            
            # if just for updating new chapters, ignore downloaded old chapters
            if isUpdate and os.path.exists(chapter_path):
                print(f"Chapter {clean_title} has been downloaded, proceed to the next chapter")
                continue
                
            img_urls = getImgUrlByWebsite(website, driver)
                    
            # download images
            chapter_path = manga_path+clean_title+"/"            
            extract_images(img_urls, chapter_path, failed_urls)
            
    if failed_urls: 
        df = pd.DataFrame(failed_urls) 
        df.to_csv(f"failed_downloads_{website}_urls.csv", index=False)
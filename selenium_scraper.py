import time 
 
import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
from pathvalidate import sanitize_filename

import requests
import os
# start by defining the options 
options = webdriver.ChromeOptions() 
#options.headless = True # it's more scalable to work in headless mode 
# normally, selenium waits for all resources to download 
# we don't need it as the page also populated with the running javascript code. 
options.page_load_strategy = 'none' 
# this returns the path web driver downloaded 
chrome_path = ChromeDriverManager().install() 
chrome_service = Service(chrome_path) 
# pass the defined options and service objects to initialize the web driver 
driver = Chrome(options=options, service=chrome_service) 
driver.implicitly_wait(5)

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
        df.to_csv(f"failed_downloads_{title}_urls.csv", index=False)
        
def main():
    title = '万能履历表' #秘密教学
    website = 'Toptoonmh.com'  # '7mj.net' 'akuma.moe
    isUpdate = False # is it first time download or just update
    isTest = False

    resource_url_file = f'Reference/{title}_urls_test.txt' if isTest else f'Reference/{title}_urls.txt'
    directory_path = '.\Downloads\\'
    manga_path = f'{directory_path}{title}\\'
    print(f"""
    ************************************************************************    
        Start scratching {title} 
            Testing = {isTest} 
            Update = {isUpdate}
    ************************************************************************
    """)

    fetchImgUrlInChapters(resource_url_file, manga_path, website, isUpdate)

    print(f"""
    ************************************************************************   
        End scratching {title} 
            Testing = {isTest} 
            Update = {isUpdate}
    ************************************************************************
    """)
    
if __name__ == "__main__":
    main()
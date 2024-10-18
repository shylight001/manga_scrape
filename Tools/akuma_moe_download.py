import os
import datetime
import time
import requests
from selenium.webdriver.common.by import By 
from constant import FAILED_IMG_URLS_FILE_PATH,FAILED_PAGE_URLS_FILE_PATH, RESOURCE_URL_FILE_PATH, MANGA_DOWNLOAD_PATH, COOKIES, HEADERS, TITLE

from Tools.chrome_driver_setup import setup_webdriver

'''
Download function for Akuma website
'''
def fetchImageURLsInAkumaCollection():
    # Akuma usually comes with collection, such as chapter 1-60, and stores one image in each page. Therefore get all page urls first. 
    # The page urls are in order so I just generated them by text editor and Excel, and store them in Reference/{title_name}_akuma_urls_test.txt
    driver = setup_webdriver()
    with open(RESOURCE_URL_FILE_PATH) as f:
        page_urls = f.readlines()
        print(f"Starting to fetch these urls: \n{page_urls}")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")
    print(f"\n-----Timestamp: {timestamp}\n")
    FAILED_PAGE_URLS_FILE_PATH_WITH_TIME = FAILED_PAGE_URLS_FILE_PATH.format(TITLE=TITLE, TIMESTAMP=timestamp)
    FAILED_IMG_URLS_FILE_PATH_WITH_TIME = FAILED_IMG_URLS_FILE_PATH.format(TITLE=TITLE, TIMESTAMP=timestamp)

    print(f"-----Created {FAILED_PAGE_URLS_FILE_PATH_WITH_TIME}")
    print(f"-----Created {FAILED_IMG_URLS_FILE_PATH_WITH_TIME}")
    failed_page_urls_file = open(FAILED_PAGE_URLS_FILE_PATH_WITH_TIME, "a")
    failed_img_urls_file = open(FAILED_IMG_URLS_FILE_PATH_WITH_TIME, "a")

    is_first_time = True
    for page_url in page_urls: 
        if page_url and page_url[:4] != "http": #verify if the page_url is valid
            print(f"Not a valid page_url, continue onto the next url")
            continue
        try:
            driver.get(page_url) 
            if is_first_time: # first time robot check takes longer to open the webpage
                time.sleep(10)
                is_first_time = False
            else:
                time.sleep(4)
            # fetch img src attribute by xpath 
            img_url = driver.find_element(By.XPATH, "//div[@id='image-container']//img").get_attribute("src") 

            if img_url and img_url[:4] == "http":
                print(f"-----HEY WORKING ON URL:{img_url}\n")   
                # Download the image to local
                extract_images_akuma(img_url, MANGA_DOWNLOAD_PATH, failed_img_urls_file)

        except Exception as e:
            print(f"\n!!!!!FAILED ON URL:{page_url}\n")   
            failed_page_urls_file.write(f"{page_url}")  

    failed_page_urls_file.close()
    failed_img_urls_file.close()
    # if failed file is empty, remove them 
    if os.path.getsize(FAILED_PAGE_URLS_FILE_PATH_WITH_TIME) == 0:
        os.remove(FAILED_PAGE_URLS_FILE_PATH_WITH_TIME)
        print(f"-----Removed {FAILED_PAGE_URLS_FILE_PATH_WITH_TIME}")
    if os.path.getsize(FAILED_IMG_URLS_FILE_PATH_WITH_TIME) == 0:
        os.remove(FAILED_IMG_URLS_FILE_PATH_WITH_TIME)
        print(f"-----Removed {FAILED_IMG_URLS_FILE_PATH_WITH_TIME}")

def extract_images_akuma(img_url, file_path, failed_file):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_name = file_path+img_url.split('/')[-1]
    
    if os.path.isfile(file_name):
        print(f"***Abort {file_name} already exists")
        return
    try:
        print(f"Try Downloading {img_url}")
        r = requests.get(img_url, cookies=COOKIES,headers=HEADERS)
        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            print(f"~YAY~ Finished downloading:{img_url}\n")   
        else:
            raise Exception(r.status_code)
    except Exception as e:
        failed_file.write(img_url)
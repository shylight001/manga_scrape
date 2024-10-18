WEBSITE = 'Manga website'  
TITLE = 'Manga title' #秘密教学
IS_UPDATE = False # is it first time download or just update
IS_TEST = True # if it is test, run {title}_urls_test.txt, otherwise run {title}_urls.txt


RESOURCE_URL_FILE_PATH = f'Resources/{TITLE}_urls_test.txt' if IS_TEST else f'Resources/{TITLE}_urls.txt'
DOWNLOAD_DIRECTORY = '.\Downloads\\'
MANGA_DOWNLOAD_PATH = f'{DOWNLOAD_DIRECTORY}{TITLE}\\'

FAILED_IMG_URLS_FILE_PATH = "Logs/failed_downloads_{TITLE}_image_urls_{TIMESTAMP}.txt"
FAILED_PAGE_URLS_FILE_PATH = "Logs/failed_{TITLE}_page_urls_{TIMESTAMP}.txt"

# How to fake cookies and headers:
# 1. use Dev tool to copy worked request as cURL(bash),
# 2. then use https://curlconverter.com/ to convert the request to python code, to get the cookies and headers.
COOKIES = {
}

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}
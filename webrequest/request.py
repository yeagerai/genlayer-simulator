import re
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


def get_webdriver() -> object:
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_text(driver:webdriver, url:str):
    driver.get(url)
    webpage_text = driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(webpage_text, 'html.parser')
    # Remove all tags and return only the text
    text_with_no_tags = soup.get_text()
    text_with_no_new_lines = text_with_no_tags.replace('\n', '')
    text_with_no_multi_spaces = re.sub(' +', ' ', text_with_no_new_lines)
    driver.close()
    return text_with_no_multi_spaces
import re
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def get_webdriver() -> object:
    return webdriver.Chrome(options=options)


def remove_unwanted_characters(text: str):
    unwanted_characters = ["\n", "\r", "\t", "\0", "\b", "\f", "\v", "¶"]
    clean_text = text
    for character in unwanted_characters:
        clean_text = clean_text.replace(character, "")
    return clean_text


def get_html(driver: webdriver, url: str):
    driver.get(url)
    webpage_text = driver.execute_script("return document.body.innerHTML;")
    text_with_no_bad_characters = remove_unwanted_characters(webpage_text)
    text_with_no_multi_spaces = re.sub(" +", " ", text_with_no_bad_characters)
    driver.close()
    return text_with_no_multi_spaces


def get_text(driver: webdriver, url: str):
    driver.get(url)
    webpage_text = driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(webpage_text, "html.parser")
    # Remove all tags and return only the text
    text_with_no_tags = soup.get_text()
    text_with_no_new_lines = text_with_no_tags.replace("\n", "")
    text_with_no_multi_spaces = re.sub(" +", " ", text_with_no_new_lines)
    driver.close()
    return text_with_no_multi_spaces

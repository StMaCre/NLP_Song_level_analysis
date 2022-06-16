from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(
    r"C:\Users\steph\Desktop\chromedriver.exe", options=options)
driver.implicitly_wait(8)
wait = WebDriverWait(driver, 10)


def get_info(i):
    word_list = []
    level_list = []
    words = driver.find_elements(
        By.XPATH, "/html/body/div[2]/div[3]/div/div/div[2]/div/div[3]/div")
    for word in words:
        word_list.append(word.text)
        level_list.append(i)
    df = pd.DataFrame(list(zip(level_list, word_list)),
                      columns=['level', 'word'])
    return df


df = pd.DataFrame()

i = 1
while i in range(51):
    website = "https://app.memrise.com/course/131111/5000-most-common-french-words/" + \
        str(i)
    driver.get(website)
    df = pd.concat([df, get_info(i)], ignore_index=True)
    i += 1
    df.to_csv('words.csv', encoding='utf-8', sep=",")

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


def get_info():
    dico = {"artist": None, "title": None, "album": None, "text": None}
    try:
        artist = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/ul/li[1]/a")
        dico["artist"] = [artist.text]
    except:
        pass
    try:
        title = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/h1")
        dico["title"] = [title.text]
    except:
        pass
    try:
        album = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/ul/li[2]")
        dico["album"] = [album.text]
    except:
        pass
    try:
        text = driver.find_elements(
            By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div[3]/div/div/div/div[3]/div[1]/div[4]/div/div/div')
        full_text = []
        for line in text:
            full_text.append(line.get_attribute('innerHTML'))
        full_text = " ".join(full_text)
        dico["text"] = full_text
    except:
        pass
    df = pd.DataFrame(dico)
    return df


df = pd.DataFrame()

# Get the first page and while there are still pages click on new page
i = 41
while i in range(50):
    website = "https://lyricstranslate.com/en/songs/22/none/none/0?page=" + \
        str(i)
    driver.get(website)
    y = 1
    # Get the lyrics page
    while y in range(101):
        page = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div[3]/form/div/div[2]/table[2]/tbody/tr[" + str(y) + "]/td[2]/a")
        driver.get(page.get_attribute("href"))
        get_info()
        y += 1
        df = pd.concat([df, get_info()], ignore_index=True)
        driver.get(website)
    i += 1
    df.to_csv('file4.csv', encoding='utf-8', sep="/")

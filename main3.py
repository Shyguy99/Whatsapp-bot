from selenium import webdriver
import os
from openwa import WhatsAPIDriver

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

li=[]
li.append("user-data-dir="+os.environ.get("USER_DATA"))
dr = WhatsAPIDriver(client='chrome', chrome_options=li,executable_path=os.environ.get("CHROMEDRIVER_PATH"))
driver.get("https://www.google.com")
print(driver.page_source)
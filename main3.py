import time

from selenium import webdriver
import os
from openwa import WhatsAPIDriver

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)


li=[("user-data-dir="+os.environ.get("USER_DATA")),"--headless","--disable-dev-shm-usage","--no-sandbox"]
dr = WhatsAPIDriver(client='chrome', chrome_options=li,executable_path=os.environ.get("CHROMEDRIVER_PATH"))
driver.get("https://www.google.com")

print("Waiting for QR")

while not dr.wait_for_login():
    time.sleep(5)
print("Bot started")
while True:
    for contact in dr.get_unread(include_me=True):
        for i in contact.messages:
            if i.type=='chat':
                if i.content=="#qq":
                    dr.reply_message(i.chat_id,i.id,"Chal gyaaaaa")


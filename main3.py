import os, sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

print("Environment", os.environ)
try:
    os.environ["CHROMEDRIVER_PATH"]
except KeyError:
    print("Please set the environment variable SELENIUM to Selenium URL")
    sys.exit(1)
options=
driver = webdriver.Remote(
    command_executor=os.environ["CHROMEDRIVER_PATH"],
    desired_capabilities=DesiredCapabilities.CHROME
)

print("Driver initialized")
print("Getting https://web.whatsapp.com")
driver.get("https://web.whatsapp.com")
driver.save_screenshot('shot.png')
print("Screenshot saved")
driver.close()
print("Driver closed")
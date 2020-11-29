
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup


from openwa import WhatsAPIDriver

driver = WhatsAPIDriver(client='Chrome')
driver.wait_for_login()

wd = webdriver.Chrome()
wd.get("https://www.google.com/")
win1=wd.window_handles[0]
wd.execute_script("window.open('');")
win2 = wd.window_handles[1]

while True:
    for contact in driver.get_unread(include_me=True, include_notifications=True):
        for message in contact.messages:

            ch=0
            if message.type == 'chat' and "#gfg" in message.content:
               try:
                print("New message '{}' received from number {}".format(message.content, message.sender.id))
                srh=message.content
                srh=list(srh.split("#"))
                if len(srh)==4:
                    srh_title=srh[2]
                    srh_lang=srh[3]
                    srh_lang=srh_lang.capitalize()
                elif len(srh)==3:
                    srh_title=srh[2]
                    srh_lang=""
                else:
                    driver.reply_message(message.chat_id,message.id,"Wrong syntax")
                    ch=1
                if ch==0:
                    wd.switch_to_window(win1)
                    a = wd.find_element_by_name('q')
                    a.clear()
                    a.send_keys(str(srh_title)+" gfg")
                    a.send_keys(Keys.ENTER)
                    b = wd.find_elements_by_css_selector(".g a")
                    got_it = False
                    for i in range(50):
                        link = b[i].get_attribute('href')
                        print(str(link))
                        if "www.geeksforgeeks.org" in str(link):
                            got_it = True
                            break
                    if got_it == True:
                        wd.switch_to_window(win2)
                        page = wd.get(str(link))

                        soup = BeautifulSoup(wd.page_source, 'html.parser')
                        to_lang = soup.findAll("li", {"class": "responsive-tabs__list__item"})
                        if len(to_lang) == 0:
                            to_lang = soup.findAll("h2", {"class": "tabtitle"})
                        k = soup.findAll("td", {"class": "code"})

                        get_code = False
                        p = "Sry"
                        if len(to_lang)==0 and len(k)!=0:
                            p=k[0].text
                            get_code=True
                            driver.reply_message(message.chat_id,message.id,p)



                        for i in range(len(to_lang)):
                            p=k[0].text
                            if str(to_lang[i].text) == "":
                                driver.reply_message(message.chat_id, message.id, k[i].text)
                                get_code = True
                                break
                            if str(srh_lang) in  str(to_lang[i].text):
                                 print(to_lang[i].text)
                                 print(k[i].text)
                                 driver.reply_message(message.chat_id,message.id,k[i].text)
                                 get_code=True
                                 break
                        if get_code==False:
                             driver.reply_message(message.chat_id,message.id,"Code not in {} language.".format(srh_lang))
                             driver.reply_message(message.chat_id,message.id,p)
                    else:
                        driver.reply_message(message.chat_id,message.id,"No data in GFG")
               except Exception as ex:
                   print(ex)


            elif message.type=='image':
                if hasattr(message, 'caption') and message.caption=='#sticker':
                    msg_caption = message.caption
                    print('caption', message.caption)

                    a=(driver.download_media(message,True))

                    #t=b64encode(a.getvalue())
                    driver.send_image_as_sticker(a,message.chat_id)

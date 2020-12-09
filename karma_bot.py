import json
import random

from bs4 import BeautifulSoup
from gtts import gTTS
from selenium.webdriver.common.keys import Keys

#class for sticker maker
class karma_sticker:
      #function for creating sticker from image
      def k_send_sticker(self,driver,message):
            if message.type == 'video' and hasattr(message, 'caption') and message.caption == '#sticker':  #video and gif can't converted
               driver.reply_message(message.chat_id, message.id, "Sry can't make sticker")
            elif hasattr(message, 'caption') and message.caption == '#sticker':
               print('caption', message.caption, message.chat_id)
               a = (driver.download_media(message, True))
               print(str(a))
               try:
                  if message.chat_id == '919675642959-1606755119@g.us' or message.chat_id == '919557666582-1580308963@g.us':  #custom setting you can ignore it 
                      driver.driver.switch_to_window(driver.driver.window_handles[0])
                      driver.send_image_as_sticker(a, '919675642959-1606756367@g.us')
                  else:
                     driver.driver.switch_to_window(driver.driver.window_handles[0])
                     driver.send_image_as_sticker(a, message.chat_id)  #sending converted sticker
               except Exception as ex:
                  print(ex)
                  driver.reply_message(message.chat_id, message.id, "Sry can't make sticker")


#class for word game
class karma_word_game:
      #initilizing some helping variables
      def __init__(self):
         self.wstarted = 'no'             #check whether game started or not
         self.c=0   #check whether 3 peoples voted or not for skiping a word
         self.score_board=[]
         with open('words.json', 'r+') as f:
            self.li = json.load(f)        #json file containing all words
      
      #function to start the game
      def wgame_start(self,driver,message):
         print(message.sender.id)
         if self.wstarted == 'no':
            self.__init__()               #reinitilizing the helping variables before starting the game
            self.score = {}
            self.score_board = {}         #dictionary containg scorers and there score
            driver.reply_message(message.chat_id, message.id, "Word Guessing game started!!")
            w = random.choice(self.li['data'])
            self.res = w[:]
            l_word = len(w)
            gap = int(3.7 / 10 * l_word)  #finding how many letters will be hidden in the word
            gap_list = random.sample(range(0, l_word - 1), gap)  #finding which positions of the letters will be hidden in the word
            w = list(w)
            for i in gap_list:
               w[i] = '_ '
            temp_w = ""
            self.w = temp_w.join(w)    #getting the final word to display
            driver.reply_message(message.chat_id, message.id,
                                 "Guess the word:\n" + self.w + "\nEnter #ans#your answer here to answer ")
            self.already_solve = 0   #variable to check whether current word is solved or not
            self.wstarted = 'yes'
            self.skip_list = []
            print(self.res)
         else:
            driver.reply_message(message.chat_id, message.id, "Game Already started!")


      #function to check answer given by user is right or not 
      def ans(self,driver,message):
         if self.wstarted == 'yes':
            if message.sender.id in self.score:    #checking whether user has entered in game or not
               anss = message.content
               anss = list(anss.split("#"))
               if len(anss) == 3:
                  ans = anss[2]
                  if ans.lower() == self.res:      #checking whether answer  given is right or not
                     if self.already_solve == 0:
                        driver.reply_message(message.chat_id, message.id,
                                             "Right Answer!You got a point\n\nType #nex_word for next word\n\nType #score to check the scores ")
                        self.already_solve = 1
                        self.score_board[self.score[message.sender.id]] += 1  #updating user score if he/she is right
                     else:
                        driver.reply_message(message.chat_id, message.id,
                                             "Already Answered!\n\nNo point will be given\n\nType #score to check the scores \nType #nex_word for next word")
                  else:
                     driver.reply_message(message.chat_id, message.id,
                                          "Wrong Answer! Think more\n\nType #currword to see current guessing word.")
               else:
                  driver.reply_message(message.chat_id, message.id,
                                       "Wrong format of answering\n\nType #ans#your answer here")
            else:
               driver.reply_message(message.chat_id, message.id,
                                    "First register by entering your name\n\nSend #enter#your name here")
         else:
            driver.reply_message(message.chat_id, message.id, "No Game running at present!\n Type #wordgame to start")

      #function to enter in the game
      def enter_game(self,driver,message):
            if self.wstarted == 'yes':
               if message.sender.id in self.score:
                  driver.reply_message(message.chat_id, message.id,
                                       "You are already in game!\n\nJust answer by typing #ans#your answer here")
               else:
                  nam = list(message.content.split("#"))
                  if len(nam) == 3:
                     name = nam[2]
                     self.score[message.sender.id] = name   #new player added 
                     self.score_board[name] = 0             #initilizing new player score to 0
                     driver.reply_message(message.chat_id, message.id,
                                          "You have entered the game..\n\nAnswer by typing #ans#your answer here")
            else:
               driver.reply_message(message.chat_id, message.id, "No Game running at present!\n Type #wordgame to start")
      
      #function to skip or go to next word 
      def next_word_or_skip(self,driver,message):
            if self.wstarted == 'yes':
               if self.already_solve == 0 and self.c < 3:      #checking if word is not guessed then 3 people vote is required to change
                  if message.sender.id in self.skip_list:      #checking whether the player is already voted or not
                     driver.reply_message(message.chat_id, message.id, "You already voted to skip\n" + str(
                        3 - self.c) + " votes needed now to skip this word")     
                  else:
                     self.c += 1
                     driver.reply_message(message.chat_id, message.id, str(3 - self.c) + " vote needed now")
                     self.skip_list.append(message.sender.id)
                     if self.c==3:
                           driver.reply_message(message.chat_id,message.id,"The right Answer is:\n "+self.res)
               if self.already_solve == 1 or (self.already_solve == 0 and self.c >= 3):  #if 3 persons condition fulfill word will change 
                  w = random.choice(self.li['data'])
                  self.res = w[:]
                  l_word = len(w)
                  gap = int(3.7 / 10 * l_word)                 #same process for choosing new word and preprocessing it
                  gap_list = random.sample(range(0, l_word - 1), gap)
                  w = list(w)
                  for i in gap_list:
                     w[i] = '_ '
                  temp_w = ""
                  self.w = temp_w.join(w)
                  driver.reply_message(message.chat_id, message.id, "Guess the word:\n" + self.w)
                  self.already_solve = 0
                  self.c = 0
                  self.skip_list = []
                  print(self.res)
            else:
               driver.reply_message(message.chat_id, message.id,
                                    "No Game running at present!\n Type #wordgame to start")
      
      #function to show current word 
      def current_word(self,driver,message):
            if self.wstarted == 'yes':
               driver.reply_message(message.chat_id, message.id, "Current word:\nGuess the word:\n" + self.w)
            else:
               driver.reply_message(message.chat_id, message.id,"No Game running at present!\n Type #wordgame to start")

      #function to show the scoreboard
      def show_score(self,driver,message):
         if len(self.score_board) != 0:
            s = ""
            score_boards = dict(sorted(self.score_board.items(), key=lambda x: x[1],reverse=True))    #sorting the players on basis of high scores
            for key, value in score_boards.items():
               s += str(key) + ": " + str(value) + "\n"
            driver.reply_message(message.chat_id, message.id, s)
         else:
            driver.reply_message(message.chat_id, message.id, "Empty Score Board")


      #function for ending the game(bot owner can do this only,according the conditions for this function)
      def end_wgame(self,driver,message):
            self.wstarted = 'no'
            driver.reply_message(message.chat_id, message.id, "Game Ended!You can restart it by typing #wordgame")

#class for tic tac toe game
class tic_tac_game:

        #initizing helpinf variables
        def __init__(self):
            self.ga = "no"  #to check whether the game is started
            self.pler = []  #to store current two players ids

        #funcion to start the game
        def tic_game_start(self,driver,message):
            if self.ga == "no":
                self.__init__()                 #reinitilizing the helping variables before starting the game
                self.c = 0
                srh = message.content
                srh = list(srh.split("#"))
                if len(srh) == 3 and '@' in srh[2]:       #checking for valid syntax 
                    if '@c.us' in srh[2]:                 #if id in form of 913287327383@c.us
                        pler2 = srh[2]
                        self.pler = [[message.chat_id, message.sender.id, message.sender.id],
                                [message.chat_id, srh[2], srh[2]]]
                    else:                                 #if id is in form of @916276327676
                        srh[2] = srh[2][1:] + '@c.us'
                        pler2 = srh[2]
                        self.pler = [[message.chat_id, message.sender.id, message.sender.id],    
                                [message.chat_id, srh[2], srh[2]]]                 #adding players id in list
                else:
                    driver.reply_message(message.chat_id, message.id, "Wrong syntax")
                    self.c = 1
                if self.c == 0 and self.ga == "no":
                    self.a = random.randint(0, 1)
                    self.sym = {self.pler[self.a][2]: "X", self.pler[abs(self.a - 1)][2]: "O"}     #symbols to marked in game you can change them 
                    self.key_list = list(self.sym.keys())
                    self.val_list = list(self.sym.values())
                    self.ini = {1: "   ", 2: "   ", 3: "   ", 4: "   ", 5: "   ", 6: "   ", 7: "   ", 8: "   ", 9: "   "}
                    #initilizing initial board
                    driver.reply_message(message.chat_id, message.id,                              
                                         self.ini[1] + "|" + self.ini[2] + "|" + self.ini[3] + "\n" + self.ini[
                                             4] + "|" + self.ini[5] + "|" + self.ini[6] + "\n" + self.ini[
                                             7] + "|" + self.ini[8] + "|" + self.ini[9] + "\n")
                    driver.reply_message(message.chat_id, message.id, "Game Starts\n" + self.pler[self.a][2] + " Your turn!")

                    self.ga = "yes"
            else:
                driver.reply_message(message.chat_id, message.id, "Game Already Started!")

        #function to placing the symbol on board
        def turn(self,driver,message):
            if len(self.pler) != 0 and (message.sender.id == self.pler[0][2] or message.sender.id == self.pler[1][2]):
                op = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
                if str(message.content[1]) in op:                #checking for valid syntax 
                    if self.pler[self.a][2] == message.sender.id:
                        print(message.sender.id)
                        co = int(str(message.content[1]))
                        if self.ini[co] == "   ":                #checking for valid move
                            self.ini[co] = self.sym[self.pler[self.a][2]]
                            self.a = abs(self.a - 1)
                            q = 0
                            driver.reply_message(message.chat_id, message.id,
                                                 self.ini[1] + "|" + self.ini[2] + "|" + self.ini[3] + "\n" +
                                                 self.ini[
                                                     4] + "|" + self.ini[5] + "|" + self.ini[6] + "\n" +
                                                 self.ini[
                                                     7] + "|" + self.ini[8] + "|" + self.ini[9] + "\n" + str(
                                                     self.pler[self.a][2]) + " Your turn!")

                            #checking whether anybody won till now or not
                            if self.ini[1] == self.ini[2] == self.ini[3] and self.ini[1] != "   ":
                                a = self.key_list[self.val_list.index(self.ini[1])]
                                q = 1
                            elif self.ini[4] == self.ini[5] == self.ini[6] and self.ini[4] != "   ":
                                a = self.key_list[self.val_list.index(self.ini[4])]
                                q = 1
                            elif self.ini[7] == self.ini[8] == self.ini[9] and self.ini[7] != "   ":
                                a = self.key_list[self.val_list.index(self.ini[7])]
                                q = 1
                            elif self.ini[1] == self.ini[4] == self.ini[7] and self.ini[1] != "   ":
                                a = self.key_list[self.val_list.index(self.ini[1])]
                                q = 1
                            elif self.ini[2] == self.ini[5] == self.ini[8] and self.ini[2] != "   ":
                                a = self.key_list[self.val_list.index(self.ini[2])]
                                q = 1
                            elif self.ini[3] == self.ini[6] == self.ini[9] and self.ini[3] != "   ":
                                a = self.key_list[self.val_list.index(self.ini[3])]
                                q = 1
                            elif self.ini[1] == self.ini[5] == self.ini[9] and self.ini[1] != "   ":
                                a = self.key_list[self.val_list.index(self.ini[1])]
                                q = 1
                            elif self.ini[3] == self.ini[5] == self.ini[7] and self.ini[3] != "   ":
                                a = self.key_list[self.val_list.index(self.ini[3])]
                                q = 1
                            if q == 1:
                                driver.reply_message(message.chat_id, message.id,
                                                     "Match Ended!!\n" + self.a + " Wins the Game")
                                ga = "no"
                                pler = []
                            else:
                                #checkin whether match is draw or not
                                for v in self.ini.values():
                                    r = 1
                                    if v == "   ":
                                        r = 0
                                        break
                                if r == 1:
                                    driver.reply_message(message.chat_id, message.id,
                                                         "Match Ended!!\nMatch Draw! No one won")
                                    self.ga = "no"
                                    self.pler = []
                        else:
                            driver.reply_message(message.chat_id, message.id, "Position already filled")
                    else:
                        driver.reply_message(message.chat_id, message.id, "Not your turn!")
                else:
                    driver.reply_message(message.chat_id, message.id, "Wrong input or Not Your Turn ")
        
        #function for ending game in middle
        def end_tic_game(self,driver,message):
            driver.reply_message(message.chat_id, message.id, "Game Ended in middle")
            self.ga = "no"
            self.pler = []

#class for converting text to speech
class voice_converse:

        count=0         #variable to keep track of number of voice record
        
        #initilizing helping variables
        def __init__(self):
            with open(r'All_voice\counter.txt','r+') as self.c_file:  #taking the last voice record number to start numbering from there only 
                p =self.c_file.read()  
            self.counter=int(p)                             #getting the number from where to start numbering again see below code to get it clear

        #function to convert text to speech
        def text_to_speech(self,driver,message):
            ch = 0
            print(message.content)
            srh = message.content
            srh = list(srh.split("#"))                      #separating tag,text and language from message
            if len(srh) == 4:
                srh_text = srh[2]
                la = srh[3]
            elif len(srh) == 3:
                la = "en"
                srh_text = srh[2]
            elif len(srh) == 2:
                driver.reply_message(message.chat_id, message.id, "Empty text")
                ch = 1
            else:
                driver.reply_message(message.chat_id, message.id, "Wrong syntax")
                ch = 1
            if ch == 0:
                all_la = ['en', 'ja', 'hi', 'fr', 'bn', 'de', 'ur', 'gu', 'zh-CN']
                if str(la) in all_la:
                    language = la
                else:
                    language = 'en'
                myobj = gTTS(text=srh_text, lang=language, slow=False)

                myobj.save("All_voice\{}.mp3".format(self.counter))                          #saving voice in the folder #Note you have to create folder first
                print("Saved")
                try:
                    driver.driver.switch_to_window(driver.driver.window_handles[0])          #switching to the current web whatsapp tab for sending voice
                    driver.send_media(r'D:\Giga\python file\bot\wp bot\All_voice\{}.mp3'.format(self.counter), message.chat_id, "Your text to speech ouput")
                except Exception as ex:
                    print(ex)
                    print("Not sent")
                print("Voice sent")
                self.counter +=1
                voice_converse.count=self.counter
                print(self.counter)

#class for getting code from gfg
class GFG:
        #function for getting the code
        def gfg(self,driver,message,wd,win1,win2):
            ch=0
            try:
                
                srh = message.content
                srh = list(srh.split("#"))              #splitting the message in tag,question,and language
                if len(srh) == 4:
                    srh_title = srh[2]
                    srh_lang = srh[3]
                    srh_lang = srh_lang.capitalize()
                elif len(srh) == 3:
                    srh_title = srh[2]
                    srh_lang = ""
                else:
                    driver.reply_message(message.chat_id, message.id, "Wrong syntax")
                    ch = 1
                if ch == 0:
                    wd.switch_to_window(win1)
                    a = wd.find_element_by_name('q')                #finding the google search box
                    a.clear()
                    a.send_keys(str(srh_title) + " gfg "+srh_lang)            #entering the question text
                    a.send_keys(Keys.ENTER)                         #pressing enter key to search
                    b = wd.find_elements_by_css_selector(".g a")    #selecting all the links shown in google result
                    got_it = False
                    for i in range(len(b)):
                        link = b[i].get_attribute('href')
                        print(str(link))
                        if "www.geeksforgeeks.org" in str(link):    #selecting the first link that is from gfg
                            got_it = True
                            break
                    if got_it == True:
                        wd.switch_to_window(win2)
                        page = wd.get(str(link))                    #opening the link in second tab if we got it

                        soup = BeautifulSoup(wd.page_source, 'html.parser')

                        #get the all the code on the page with there language label by using ids of html 
                        to_lang = soup.findAll("li", {"class": "responsive-tabs__list__item"})
                        if len(to_lang) == 0:
                            to_lang = soup.findAll("h2", {"class": "tabtitle"})
                        k = soup.findAll("td", {"class": "code"})

                        get_code = False
                        p = ""
                        if len(to_lang) == 0 and len(k) != 0:      #if code is there but without language label
                            p = k[0].text
                            get_code = True
                            driver.reply_message(message.chat_id, message.id, p)

                        for i in range(len(to_lang)):              #getting the required code in given language if it is there on the page
                            p = k[0].text
                            if str(to_lang[i].text) == "":
                                driver.reply_message(message.chat_id, message.id, k[i].text)
                                get_code = True
                                break
                            if str(srh_lang) in str(to_lang[i].text):
                                print(to_lang[i].text)
                                print(k[i].text)
                                driver.reply_message(message.chat_id, message.id, k[i].text)
                                get_code = True
                                break
                        if get_code == False:
                            driver.reply_message(message.chat_id, message.id,
                                                 "Code not in {} language or code not found".format(srh_lang)+"\n"+p)
                    else:
                        driver.reply_message(message.chat_id, message.id, "No data in GFG")
            except Exception as ex:
                print(ex)

#class for quiting the program (admin only according to calling if condition)
class quit_bot:
    def quit(self, driver, wd):
        with open('All_voice\counter.txt', 'r+') as c_fil:       #replacing the counter value in the txt file with the new number
            c_fil.seek(0)
            c_fil.truncate()
            c_fil.write(str(voice_converse.count))
        wd.quit()                                                #quiting chrome driver
        driver.quit()                                            #quiting WhatsappApi driver


#Code written by Kailash Sharma 

 



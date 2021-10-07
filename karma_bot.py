import json
import random

import time

import pydoodle
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

# list of emojis for the fig game
emojis = ["🍓", "🥭", "🥥", "🍎", "🍇", "🫐", "🍒", "🌶️", "🥒", "🍅", "🥦", "🍞", "🥯", "🍕", "🍔", "🍫", "🍿", "🍩",
          "🥤", "🥜", "🍼", "🍨", "🍬", "🍭"]

# list of emojis number for minesweeper
emoj = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]


# class for sticker maker
class karma_sticker:
    # function for creating sticker from image
    def k_send_sticker(self, driver, message):

        if message.type == 'video' and hasattr(message,
                                               'caption') and message.caption == '#sticker':  # video and gif can't converted
            driver.reply_message(message.chat_id, message.id, "Sry can't make sticker")
        elif hasattr(message, 'caption') and message.caption == '#sticker':
            print('caption', message.caption, message.chat_id)
            a = (driver.download_media(message, True))
            print(str(a))
            try:
                if message.chat_id == '919675642959-1606755119@g.us' or message.chat_id == '919557666582-1580308963@g.us':  # custom setting you can ignore it
                    driver.driver.switch_to_window(driver.driver.window_handles[0])
                    driver.send_image_as_sticker(a, '919675642959-1606756367@g.us')
                else:
                    print("Sending sticker")
                    driver.driver.switch_to_window(driver.driver.window_handles[0])
                    driver.send_image_as_sticker(a, message.chat_id)  # sending converted sticker
                    print("Sticker sent")
            except Exception as ex:
                print(ex)
                driver.reply_message(message.chat_id, message.id, "Sry can't make sticker")


# class for word game
class karma_word_game:
    # initilizing some helping variables
    def __init__(self):
        self.wstarted = 'no'  # check whether game started or not
        self.c = 0  # check whether 3 peoples voted or not for skiping a word
        self.score_board = []
        with open('words.json', 'r+') as f:
            self.li = json.load(f)  # json file containing all words

    # function to start the game
    def wgame_start(self, driver, message):
        print(message.sender.id)
        if self.wstarted == 'no':
            self.__init__()  # reinitilizing the helping variables before starting the game
            self.score = {}
            self.score_board = {}  # dictionary containg scorers and there score
            driver.reply_message(message.chat_id, message.id, "Word Guessing game started!!")
            w = random.choice(self.li['data'])
            self.res = w[:]
            l_word = len(w)
            gap = int(3.8 / 10 * l_word)  # finding how many letters will be hidden in the word
            gap_list = random.sample(range(0, l_word - 1),
                                     gap)  # finding which positions of the letters will be hidden in the word
            w = list(w)
            for i in gap_list:
                w[i] = '_ '
            temp_w = ""
            self.w = temp_w.join(w)  # getting the final word to display
            driver.reply_message(message.chat_id, message.id,
                                 "Guess the word:\n" + self.w + "\nEnter #ans#your answer here to answer ")
            self.already_solve = 0  # variable to check whether current word is solved or not
            self.wstarted = 'yes'
            self.skip_list = []
            print(self.res)
        else:
            driver.reply_message(message.chat_id, message.id, "Game Already started!")

    # function to check answer given by user is right or not
    def ans(self, driver, message):
        if self.wstarted == 'yes':
            if message.sender.id in self.score:  # checking whether user has entered in game or not
                anss = message.content
                anss = list(anss.split("#"))
                if len(anss) == 3:
                    ans = anss[2]
                    if ans.lower() == self.res:  # checking whether answer  given is right or not
                        if self.already_solve == 0:
                            driver.reply_message(message.chat_id, message.id,
                                                 "Right Answer!You got a point\n\nType #nex_word for next word\n\nType #score to check the scores ")
                            self.already_solve = 1
                            self.score_board[
                                self.score[message.sender.id]] += 1  # updating user score if he/she is right
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

    # function to enter in the game
    def enter_game(self, driver, message):
        if self.wstarted == 'yes':
            if message.sender.id in self.score:
                driver.reply_message(message.chat_id, message.id,
                                     "You are already in game!\n\nJust answer by typing #ans#your answer here")
            else:
                nam = list(message.content.split("#"))
                if len(nam) == 3:
                    name = nam[2]
                    self.score[message.sender.id] = name  # new player added
                    self.score_board[name] = 0  # initilizing new player score to 0
                    driver.reply_message(message.chat_id, message.id,
                                         "You have entered the game..\n\nAnswer by typing #ans#your answer here")
        else:
            driver.reply_message(message.chat_id, message.id, "No Game running at present!\n Type #wordgame to start")

    # function to skip or go to next word
    def next_word_or_skip(self, driver, message):
        if self.wstarted == 'yes':
            if self.already_solve == 0 and self.c < 3:  # checking if word is not guessed then 3 people vote is required to change
                if message.sender.id in self.skip_list:  # checking whether the player is already voted or not
                    driver.reply_message(message.chat_id, message.id, "You already voted to skip\n" + str(
                        3 - self.c) + " votes needed now to skip this word")
                else:
                    self.c += 1
                    driver.reply_message(message.chat_id, message.id, str(3 - self.c) + " vote needed now")
                    self.skip_list.append(message.sender.id)
                    if self.c == 3:
                        driver.reply_message(message.chat_id, message.id, "The right Answer is:\n " + self.res)
            if self.already_solve == 1 or (
                    self.already_solve == 0 and self.c >= 3):  # if 3 persons condition fulfill word will change
                w = random.choice(self.li['data'])
                self.res = w[:]
                l_word = len(w)
                gap = int(3.8 / 10 * l_word)  # same process for choosing new word and preprocessing it
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

    # function to show current word
    def current_word(self, driver, message):
        if self.wstarted == 'yes':
            driver.reply_message(message.chat_id, message.id, "Current word:\nGuess the word:\n" + self.w)
        else:
            driver.reply_message(message.chat_id, message.id, "No Game running at present!\n Type #wordgame to start")

    # function to show the scoreboard
    def show_score(self, driver, message):
        if len(self.score_board) != 0:
            s = ""
            score_boards = dict(sorted(self.score_board.items(), key=lambda x: x[1],
                                       reverse=True))  # sorting the players on basis of high scores
            for key, value in score_boards.items():
                s += str(key) + ": " + str(value) + "\n"
            driver.reply_message(message.chat_id, message.id, s)
        else:
            driver.reply_message(message.chat_id, message.id, "Empty Score Board")

    # function for ending the game(bot owner can do this only,according the conditions for this function)
    def end_wgame(self, driver, message):
        self.wstarted = 'no'
        driver.reply_message(message.chat_id, message.id, "Game Ended!You can restart it by typing #wordgame")


# class for tic tac toe game
class tic_tac_game:

    def __init__(self, driver, message, p1, p2):
        # player list
        self.players = [p1, p2]

        # choosing which player chance randomly
        self.chance = random.choice(range(2))

        # status of game who won or loss
        self.status = ""

        # initial game map
        self.g_map = [["⬜" for i in range(3)] for j in range(3)]

        # list of place to be marked
        self.to_be_marked_list = [str(i) for i in range(1, 10)]

        # sending empty game board
        out = self.list_to_string(self.g_map)
        out2 = "Game started {} vs {} ⚔️".format("@" + self.players[0].replace("@c.us", ""),
                                                 "@" + self.players[1].replace("@c.us", ""))
        out3 = "First {} your turn \nSend #(box number) to place your mark on board.".format(
            "@" + str(self.players[self.chance]).replace("@c.us", ""))
        driver.wapi_functions.sendMessageWithMentions(message.chat_id, out + "\n" + out2, "")
        driver.wapi_functions.sendMessageWithMentions(message.chat_id, out3)

    def list_to_string(self, li):
        s = []
        for i in range(len(li)):
            s1 = ''.join(li[i])
            s.append(s1)
        s = "\n".join(s)
        return s

    def mark(self, driver, message, m):
        if self.players[self.chance] == str(message.sender.id):

            if m in self.to_be_marked_list:

                # removing marked position
                self.to_be_marked_list.remove(m)

                # finding the position to be marked in 2d list
                if int(m) % 3 == 0:
                    p1 = int(m) // 3 - 1
                    p2 = 2
                else:
                    p1 = int(m) // 3
                    p2 = int(m) % 3 - 1

                # marking the position
                if self.chance == 1:
                    self.g_map[p1][p2] = "❌"
                else:
                    self.g_map[p1][p2] = "⭕"

                # checking if somebody win or not or its a draw
                self.status = self.win_or_not(self.g_map)

                if self.status != "":
                    if self.status == "draw":
                        out1 = self.list_to_string(self.g_map)
                        out2 = "Its a Draw 🤕 \n{} {}".format("@" + self.players[0].replace("@c.us", ""),
                                                              "@" + self.players[1].replace("@c.us", ""))
                        driver.wapi_functions.sendMessageWithMentions(message.chat_id, out1 + "\n" + out2, "")
                    else:
                        out1 = self.list_to_string(self.g_map)
                        out2 = "{} won the match 🎉🎉".format("@" + self.status.replace("@c.us", ""))
                        driver.wapi_functions.sendMessageWithMentions(message.chat_id, out1 + "\n" + out2, "")
                else:
                    # shifting the chance
                    self.chance = abs(self.chance - 1)

                    out1 = self.list_to_string(self.g_map)
                    out2 = "{} your turn now.".format("@" + str(self.players[self.chance]).replace("@c.us", ""))
                    driver.wapi_functions.sendMessageWithMentions(message.chat_id, out1 + "\n" + out2, "")

            else:
                driver.reply_message(message.chat_id, message.id, "Place is already marked or invalid!")
        else:
            driver.reply_message(message.chat_id, message.id, "Not your chance boi 🤧")

    def win_or_not(self, l):
        if l[0][0] == l[0][1] and l[0][0] == l[0][2] and l[0][0] != "⬜":
            if l[0][0] == "❌":
                return self.players[1]
            else:
                return self.players[0]
        elif l[1][0] == l[1][1] and l[1][0] == l[1][2] and l[1][0] != "⬜":
            if l[1][0] == "❌":
                return self.players[1]
            else:
                return self.players[0]
        elif l[2][0] == l[2][1] and l[2][0] == l[2][2] and l[2][0] != "⬜":
            if l[2][0] == "❌":
                return self.players[1]
            else:
                return self.players[0]

        elif l[0][0] == l[1][0] and l[0][0] == l[2][0] and l[0][0] != "⬜":
            if l[0][0] == "❌":
                return self.players[1]
            else:
                return self.players[0]
        elif l[0][1] == l[1][1] and l[0][1] == l[2][1] and l[0][1] != "⬜":
            if l[0][1] == "❌":
                return self.players[1]
            else:
                return self.players[0]
        elif l[0][2] == l[1][2] and l[0][2] == l[2][2] and l[0][2] != "⬜":
            if l[0][2] == "❌":
                return self.players[1]
            else:
                return self.players[0]

        elif l[0][0] == l[1][1] and l[0][0] == l[2][2] and l[0][0] != "⬜":
            if l[0][0] == "❌":
                return self.players[1]
            else:
                return self.players[0]
        elif l[0][2] == l[1][1] and l[0][2] == l[2][0] and l[0][2] != "⬜":
            if l[0][2] == "❌":
                return self.players[1]
            else:
                return self.players[0]

        elif len(self.to_be_marked_list) == 0:
            return "draw"
        else:
            return ""

    def current_match(self, driver, message):
        out1 = self.list_to_string(self.g_map)
        out2 = "{} your turn now.".format("@" + str(self.players[self.chance]).replace("@c.us", ""))
        driver.wapi_functions.sendMessageWithMentions(message.chat_id, out1 + "\n" + out2, "")


class GFG:
    # function for getting the code
    def gfg(self, driver, message, wd, win1, win2):
        ch = 0
        try:

            srh = message.content
            srh = list(srh.split("#"))  # splitting the message in tag,question,and language
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
                a = wd.find_element_by_name('q')  # finding the google search box
                a.clear()
                a.send_keys(str(srh_title) + " gfg " + str(srh_lang))  # entering the question text
                a.send_keys(Keys.ENTER)  # pressing enter key to search
                b = wd.find_elements_by_css_selector(".g a")  # selecting all the links shown in google result
                got_it = False
                for i in range(len(b)):
                    link = b[i].get_attribute('href')
                    print(str(link))
                    if "www.geeksforgeeks.org" in str(link):  # selecting the first link that is from gfg
                        got_it = True
                        break
                if got_it == True:
                    wd.switch_to_window(win2)
                    page = wd.get(str(link))  # opening the link in second tab if we got it

                    soup = BeautifulSoup(wd.page_source, 'html.parser')

                    # get the all the code on the page with there language label by using ids of html
                    to_lang = soup.findAll("li", {"class": "responsive-tabs__list__item"})
                    if len(to_lang) == 0:
                        to_lang = soup.findAll("h2", {"class": "tabtitle"})
                    k = soup.findAll("td", {"class": "code"})

                    get_code = False
                    p = ""
                    if len(to_lang) == 0 and len(k) != 0:  # if code is there but without language label
                        p = k[0].text
                        get_code = True
                        driver.reply_message(message.chat_id, message.id, p)

                    for i in range(
                            len(to_lang)):  # getting the required code in given language if it is there on the page

                        # getting the code as string from the divs
                        all_divmix = k[0].findAll("div", {"class": "container"})
                        p = ""
                        for j in all_divmix:
                            for l in j:
                                p += l.text + "\n"

                        if str(to_lang[i].text) == "":
                            # getting the code as string from the divs
                            all_divmix = k[i].findAll("div", {"class": "container"})
                            p = ""
                            for j in all_divmix:
                                for l in j:
                                    p += l.text + "\n"

                            driver.reply_message(message.chat_id, message.id, p)
                            get_code = True
                            break
                        if str(srh_lang) in str(to_lang[i].text):
                            # getting the code as string from the divs
                            all_divmix = k[i].findAll("div", {"class": "container"})
                            p = ""
                            for j in all_divmix:
                                for l in j:
                                    p += l.text + "\n"

                            print(to_lang[i].text)
                            print(p)
                            driver.reply_message(message.chat_id, message.id, p)
                            get_code = True
                            break
                    if get_code == False:
                        driver.reply_message(message.chat_id, message.id,
                                             "Code not in {} language or code not found".format(srh_lang) + "\n" + p)
                else:
                    driver.reply_message(message.chat_id, message.id, "No data in GFG")
        except Exception as ex:
            print(ex)


class matcher:

    def __init__(self, driver, message, diff=4):
        self.diff = diff
        if diff % 2 != 0:
            self.diff += 1
        # count to check whether player won or not
        self.corr = 0

        # to check given guessing pair is valid or not
        self.match_numbers = []
        for i in range(1, diff + 1):
            for j in range(1, diff + 1):
                self.match_numbers.append(str(i) + str(j))

        # time variable to check how much time it take to complete the game
        self.tim = time.time()

        # hidden layer boxes
        self.map_cov = [["📦" for i in range(diff + 1)] for j in range(diff + 1)]
        self.map_cov[0][0] = " "
        for i in range(1, diff + 1):
            self.map_cov[0][i] = "  " + str(i) + "  "
            self.map_cov[i][0] = str(i)

        # it will the actual map of fig
        self.map = [["." for i in range(diff + 1)] for j in range(diff + 1)]
        self.map[0][0] = " "
        for i in range(1, diff + 1):
            self.map[0][i] = "  " + str(i) + "  "
            self.map[i][0] = str(i)

        # list to choose random position
        ram = []
        for i in range(diff):
            for j in range(diff):
                ram.append([i, j])

        # choosing random  fig index from emojis list
        ran_fig_list = random.sample(range(0, len(emojis)), (diff * diff) // 2)

        # filling the map with fig
        for i in range(len(ran_fig_list)):
            ran_fig = emojis[ran_fig_list[i]]

            # putting the same figure in two different position in the map of figures
            ran_pos = random.choice(ram)
            self.map[ran_pos[0] + 1][ran_pos[1] + 1] = ran_fig
            ram.remove(ran_pos)

            ran_pos2 = random.choice(ram)
            self.map[ran_pos2[0] + 1][ran_pos2[1] + 1] = ran_fig
            ram.remove(ran_pos2)

        out2 = self.list_to_string(self.map_cov)
        driver.reply_message(message.chat_id, message.id, "Game Started!!" + "\n" + out2+"\nSend #help_match see the controls.")

    def list_to_string(self, li):
        p = []
        for j in range(len(li)):
            s1 = ' '.join(li[j])
            p.append(s1)
        s = '\n'.join(p)
        return s

    def guess(self, driver, message, v1, v2):
        if v1 not in self.match_numbers or v2 not in self.match_numbers:
            driver.reply_message(message.chat_id, message.id, "Wrong input or pairs already chosen! Check again")

        else:

            l1 = list(map(int, v1))
            l2 = list(map(int, v2))

            if self.map[l1[0]][l1[1]] == self.map[l2[0]][l2[1]]:
                self.match_numbers.remove(v1)
                self.match_numbers.remove(v2)
                self.corr += 2

                if self.corr == self.diff * self.diff:
                    t_taken = str((time.time() - self.tim) // 60) + " minutes\n"
                    out = self.list_to_string(self.map)
                    driver.reply_message(message.chat_id, message.id,
                                         "*Wow! You won!!!*" + "\nin " + t_taken + "\n" + out)


                else:
                    self.map_cov[l1[0]][l1[1]] = self.map[l1[0]][l1[1]]
                    self.map_cov[l2[0]][l2[1]] = self.map[l2[0]][l2[1]]

                    out = self.list_to_string(self.map_cov)
                    driver.reply_message(message.chat_id, message.id, "Right! Continue\n" + out)
            else:
                self.map_cov[l1[0]][l1[1]] = self.map[l1[0]][l1[1]]
                self.map_cov[l2[0]][l2[1]] = self.map[l2[0]][l2[1]]
                out = self.list_to_string(self.map_cov)
                driver.reply_message(message.chat_id, message.id, "Nope! Wrong Pair" + "\n" + out)

                self.map_cov[l1[0]][l1[1]] = "📦"
                self.map_cov[l2[0]][l2[1]] = "📦"
                out = self.list_to_string(self.map_cov)
                driver.reply_message(message.chat_id, message.id, "Try Again!" + "\n" + out)

    def current_game(self, driver, message):
        out = self.list_to_string(self.map_cov)
        driver.reply_message(message.chat_id, message.id, "Your current game!\n" + out)


# class for minesweeper game
class mine:

    def __init__(self, driver, message, diff=4):

        # store visited mines
        self.vis = set()

        # store lose or win status
        self.status = ""

        # hidden map grid
        self.mine_cov_map = [["🔳" for i in range(10)] for j in range(10)]
        self.mine_cov_map[0][0] = " "
        for i in range(1, 10):
            self.mine_cov_map[0][i] = "  " + str(i) + "  "
            self.mine_cov_map[i][0] = str(i)

        # map with bombs
        self.bomb_map = [[" " for i in range(10)] for j in range(10)]
        self.bomb_map[0][0] = " "
        for i in range(1, 10):
            self.bomb_map[0][i] = "  " + str(i) + "  "
            self.bomb_map[i][0] = str(i)

        # number of bombs
        self.diff = diff * 3

        # list of chosen position by player
        self.to_be_chosen = []

        # creating list of index pair of a map to choose diff pos for bombs
        k = []
        for i in range(1, 10):
            for j in range(1, 10):
                # adding index pair in k to use it for finding sample
                k.append([i, j])
                # adding element in chosen list
                self.to_be_chosen.append(str(i) + str(j))
        self.ran_pos = random.sample(k, self.diff)
        print(self.ran_pos)

        for i in self.ran_pos:
            self.bomb_map[i[0]][i[1]] = "💣"
        out = self.listtostring(self.mine_cov_map)
        driver.reply_message(message.chat_id, message.id, "Game started! Best of luck 😁\n\n" + out)

    def choose(self, driver, message, ch):
        print(ch, "chhhh")

        if ch not in self.to_be_chosen:

            driver.reply_message(message.chat_id, message.id, "You have already chosen this box or it is invalid! 😐")

        else:

            ch = list(map(int, ch))

            # checking it is bomb or not
            if self.bomb_map[ch[0]][ch[1]] != " ":
                self.to_be_chosen.remove(self.to_str(ch[0], ch[1]))
                for i in self.ran_pos:
                    self.mine_cov_map[i[0]][i[1]] = "💣"
                out = self.listtostring(self.mine_cov_map)
                driver.reply_message(message.chat_id, message.id, "Oops! You lose the game ☹\n" + out)
                self.status = "Lose"

            else:
                que = []
                que.append(ch)
                self.vis.add(str(ch[0]) + str(ch[1]))
                while len(que) != 0:

                    pos = que[0]
                    que.pop(0)
                    q = []
                    i = pos[0]
                    j = pos[1]
                    flag = 0

                    # sw pos check
                    p1 = i + 1
                    p2 = j + 1
                    q, flag = self.check_adjacent_bomb(p1, p2, q, flag)

                    # s pos check
                    p1 = i + 1
                    p2 = j
                    q, flag = self.check_adjacent_bomb(p1, p2, q, flag)

                    # se pos check
                    p1 = i + 1
                    p2 = j - 1
                    q, flag = self.check_adjacent_bomb(p1, p2, q, flag)

                    # east pos check
                    p1 = i
                    p2 = j - 1
                    q, flag = self.check_adjacent_bomb(p1, p2, q, flag)

                    # ne pos check
                    p1 = i - 1
                    p2 = j - 1
                    q, flag = self.check_adjacent_bomb(p1, p2, q, flag)

                    # n pos check
                    p1 = i - 1
                    p2 = j
                    q, flag = self.check_adjacent_bomb(p1, p2, q, flag)

                    # nw pos check
                    p1 = i - 1
                    p2 = j + 1
                    q, flag = self.check_adjacent_bomb(p1, p2, q, flag)

                    # w pos check
                    p1 = i
                    p2 = j + 1
                    q, flag = self.check_adjacent_bomb(p1, p2, q, flag)

                    self.to_be_chosen.remove(self.to_str(i, j))
                    if flag == 0:
                        self.mine_cov_map[i][j] = "⚪"
                        que = que + q
                    else:
                        self.mine_cov_map[i][j] = emoj[flag - 1]
                if len(self.to_be_chosen) == self.diff:
                    for i in self.ran_pos:
                        self.mine_cov_map[i[0]][i[1]] = "🚩"
                    out = self.listtostring(self.mine_cov_map)
                    driver.reply_message(message.chat_id, message.id, "Wow! You have won 🎉🎉\n\n" + out)
                    self.status = "Won"
                else:
                    out = self.listtostring(self.mine_cov_map)
                    driver.reply_message(message.chat_id, message.id, "Good, Continue 🤫 \n\n" + out)

    def mark_pos(self, driver, message, ch, m):
        if ch in self.to_be_chosen:
            ch = list(map(int, ch))

            if m == 1:
                self.mine_cov_map[ch[0]][ch[1]] = "🚩"
            elif m == 0:
                self.mine_cov_map[ch[0]][ch[1]] = "🔳"
        else:
            driver.reply_message(message.chat_id, message.id, "It's already mined")
        out = self.listtostring(self.mine_cov_map)
        driver.reply_message(message.chat_id, message.id, "Marked/Unmarked\n\n" + out)

    def check_adjacent_bomb(self, p1, p2, que, flag):
        if self.check_notout_bound_pos(p1, p2):
            if self.bomb_map[p1][p2] == " ":
                st = self.to_str(p1, p2)
                if st not in self.vis:
                    que.append([p1, p2])
                    self.vis.add(st)
            else:
                flag += 1
        return [que, flag]

    def to_str(self, p1, p2):
        return str(p1) + str(p2)

    def check_notout_bound_pos(self, q, r):
        if q >= 1 and q <= 9 and r >= 1 and r <= 9:
            return True
        else:
            return False

    def listtostring(self, li):
        s = []
        for i in range(len(li)):
            s1 = ''.join(li[i])
            s.append(s1)
        s = "\n".join(s)
        return s


class compiler:

    def __init__(self, clientId, clientSec):
        self.r = pydoodle.Compiler(clientId=clientId,
                                   clientSecret=clientSec)

        self.inuse = 0

    def run(self, driver, message, lang, code):
        self.code = code
        self.lang = lang.lower()
        self.languages = ['ada', 'bash', 'bc', 'brainfuck', 'c', 'c-99', 'clisp', 'clojure', 'cobol', 'coffeescript',
                          'cpp',
                          'cpp17', 'csharp', 'd', 'dart', 'elixir', 'erlang', 'factor', 'falcon', 'fantom', 'forth',
                          'fortran', 'freebasic', 'fsharp', 'gccasm', 'go', 'groovy', 'hack', 'haskell', 'icon',
                          'intercal',
                          'java', 'jlang', 'kotlin', 'lolcode', 'lua', 'mozart', 'nasm', 'nemerle', 'nim', 'nodejs',
                          'objc',
                          'ocaml', 'octave', 'pascal', 'perl', 'php', 'picolisp', 'pike', 'prolog', 'python2',
                          'python3', 'r',
                          'racket', 'rhino', 'ruby', 'rust', 'scala', 'scheme', 'smalltalk', 'spidermonkey', 'sql',
                          'swift',
                          'tcl', 'unlambda', 'vbn', 'verilog', 'whitespace', 'yabasic']

        if lang.lower() in self.languages:

            self.inuse = 1

            result = self.r.execute(script=self.code, language=self.lang)
            res = list(result.output)[0]
            print(res)
            if "Timeout" in res:
                message.reply_message("Program Timeout:\nCauses can be INFINITE LOOP or INPUT STATEMENTS")
            else:
                try:
                    driver.wapi_functions.sendMessageWithMentions(message.chat_id, "Output-:\n" + res + "\n\n" + str(
                        result.cpuTime) + " s", "")
                except:
                    message.reply_message("Output-:\n" + res + "\n\n" + str(result.cpuTime) + " s")

            self.inuse = 0
        else:
            message.reply_message("Sorry!! Only Language supported are:-\n {} ".format(' ,'.join(self.languages)))


class cmd_suggesstion:
    def __init__(self, allcmds):
        self.all_cmd = allcmds

    def suggest(self, message, cmd):

        cmd_len = len(cmd)

        lcs_list=[]
        comman_chr_list = []

        for cm in self.all_cmd:

            # Longest comman subsequence between the given command and all cmds code

            cm_len = len(cm)

            L = [[-1] * (cm_len + 1) for i in range(cmd_len + 1)]

            for i in range(cmd_len + 1):
                for j in range(cm_len + 1):
                    if i == 0 or j == 0:
                        L[i][j] = 0
                    elif cmd[i - 1] == cm[j - 1]:
                        L[i][j] = L[i - 1][j - 1] + 1
                    else:
                        L[i][j] = max(L[i - 1][j], L[i][j - 1])

            lcs_list.append([L[cmd_len][cm_len]/cm_len,cm])


            #code to check number of comman character in cmd with all cmds
            curr_cmd=list(cmd)
            curr_li_cmd=list(cm)

            coun=0
            for i in curr_li_cmd:
                if i in curr_cmd:
                    curr_cmd.remove(i)
                    coun+=1

            comman_chr_list.append([coun/cm_len,cm])

        #sorting both the list to get high priority length at top
        lcs_list.sort()
        comman_chr_list.sort()

        fin_list= {lcs_list[-1][1], lcs_list[-2][1], comman_chr_list[-1][1], comman_chr_list[-2][1]}
        out=",".join(fin_list)

        message.reply_message("Wrong Command!!\nI think you mean one of the following:\n"+out+"\nFor more commands use #help")





# class for quiting the program (admin only according to calling if condition)
class quit_bot:
    def quit(self, driver, wd):
        wd.quit()  # quiting chrome driver
        driver.quit()  # quiting WhatsappApi driver

# Code written by Kailash Sharma

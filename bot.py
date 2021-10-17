import threading
from itertools import count
import karma_bot
from selenium import webdriver
from openwa import WhatsAPIDriver
import time
import os
import wikipedia
import psycopg2

while True:
    flag=0
    #time to noted after which whole bot restart
    s_time=time.time()

    #Change these variable before running the bot
    YOUR_MOBILE_NUMBER = "17207416585"                    # Ex-:   918273627374
    Jdoodle_clientId="f4024ff5ac6b07c27fe236582c7c5331"
    Jdoodle_clientSecret="55e17e9e99239d105df4f5e9014f08b554d007c3ed044ea798b5e66b3b49e664"


    #pre-defining varibales
    all_cmds=["#msg_count","#ludo","#ldice","#lmove","quitludo","#currludo","#last_tag","#all_cmd","#help","#run python3#","#run cpp#","#resetrun","#ticgame","#currtic","#quit_tic","#help_tic","#wordgame","#currword","#ans ","#join ","#score","#skip","#help_wgame","#gfg#","#matchgame","#help_match","#currmatch","#quitmatch","#m","#minegame","#mine ","#currmine","#minemark","#mineunmark","#help_mine","#wiki ","#add","#kick","#link","#tagall","#tagadmins","#source"]

    conn = psycopg2.connect("postgres://csqmnmlhadcckk:d2783f1d23d96549ec7f8c6aa189fc725e07f68e93407a5ddf2c883007695777@ec2-44-198-154-255.compute-1.amazonaws.com:5432/daklcdjauog639", sslmode='require')

    cur = conn.cursor()


    #dict of groups
    group=dict()
    cur.callproc('get_chats')
    getchats=cur.fetchone()[0]
    l = len(getchats) // 2
    i = 0
    j = l
    for i in range(l):
        id=getchats[i].replace("\"","")
        group[id] = int(getchats[j])
        i += 1
        j += 1
    print(group)

    #getting score_board and players list from databse
    cur.callproc('get_score')
    out=cur.fetchone()
    if out[0]==None:
        score=dict()
    else:
        out=out[0]
        l=len(out)//2
        i=0
        j=l
        score=dict()
        for i in range(l):
            score[out[i]]=int(out[j])
            i+=1
            j+=1
    cur.callproc('get_player')
    out=cur.fetchone()
    if out[0]==None:
        player=dict()
    else:
        out=out[0]
        l=len(out)//2
        i=0
        j=l
        player=dict()
        for i in range(l):
            player[out[i]]=out[j]
            i+=1
            j+=1


    # creating all classes object
    sticker = karma_bot.karma_sticker()
    Word=karma_bot.karma_word_game(score,player)

    GFG = karma_bot.GFG()
    COMP=karma_bot.compiler(Jdoodle_clientId,Jdoodle_clientSecret)
    suggest=karma_bot.cmd_suggesstion(all_cmds)

    quit = karma_bot.quit_bot()



    # object dict for matchgame
    match_player_dict = dict()

    # object dict for tic game
    tic_player_dict = dict()

    # object list for minegame
    mine_player_dict = dict()

    # object list for ludo game
    ludo_game_dict = dict()




    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    wd = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)


    li=[("user-data-dir="+os.environ.get("USER_DATA")),"--disable-dev-shm-usage","--no-sandbox"]
    driver = WhatsAPIDriver(client='chrome', headless=True,chrome_options=li,executable_path=os.environ.get("CHROMEDRIVER_PATH"))






    wd.get("https://www.google.com/")  # opening google in one tab
    win1 = wd.window_handles[0]
    wd.execute_script("window.open('');")  # opening second empty tab
    win2 = wd.window_handles[1]

    #database variables for maintaining transactions control
    db_members=0
    db_chats=0
    p_adding=0
    s_adding=0

    def main(message):
        global bot
        global db_members
        global db_chats
        global s_adding
        global p_adding
        global s_time

        if message.chat_id in group:
            all_msg.append(message)

        if (message.type == 'chat' or message.type == 'image' or message.type == 'video') and (
                (hasattr(message, 'caption') and message.caption == '#sticker') or message.content[0:1] == '#'):

            if message.chat_id not in group and db_chats==0:
                db_chats=1
                group[message.chat_id] = 1
                try:
                    cur.execute('CALL add_chat(\'{}\',\'{}\')'.format("\"" + message.chat_id + "\"",1))
                    conn.commit()
                    db_chats=0
                    message.reply_message("Send #help to check out all the features of bot ✨")
                except Exception as e:
                    print(e)
                    message.reply_message("Bot failed to start for this chat!")
                    db_chats = 0


            if message.type == 'chat' and message.content == '#on' and db_chats==0:
                db_chats=1
                if str(message.sender.id) == YOUR_MOBILE_NUMBER + "@c.us" or message.sender.id in driver.wapi_functions.getGroupAdmins(message.chat_id):
                    if  group[message.chat_id]==0:
                        group[message.chat_id] = 1
                        try:
                            cur.execute('CALL add_chat(\'{}\',\'{}\')'.format("\"" + message.chat_id + "\"",1))
                            conn.commit()
                            db_chats=0

                            message.reply_message("I-Bot is now active ✨")
                        except Exception as e:
                            print(e)
                            message.reply_message("I-Bot failed to start for this chat!")

                    else:
                        message.reply_message("I-Bot is already ON for this group")
                else:
                    message.reply_message("Command only for admins!")
                db_chats = 0
            if message.type == 'chat':
                if message.content!="#on" and message.chat_id in group and group[message.chat_id]==1:
                    if message.content == '#off' and db_chats==0 and ((str(message.sender.id) == YOUR_MOBILE_NUMBER + "@c.us") or message.sender.id in driver.wapi_functions.getGroupAdmins(message.chat_id)):
                        db_chats=1
                        try:
                            cur.execute('CALL add_chat(\'{}\',\'{}\')'.format("\"" + message.chat_id + "\"", 0))
                            conn.commit()
                            db_chats=0
                            group[message.chat_id]=0
                            message.reply_message("I-Bot is now inactive for this chat 🥺")

                        except Exception as e:
                            print(e)
                            message.reply_message("I-Bot failed to start for this chat!")
                            db_chats=0





                    # commands for help and controls
                    elif (message.content == '#help' or message.content == '#command'):
                        s = """*Welcome to the I-Bot*\n\n*Features*\n\n*1. Compiler*✅ \n-Run any language code by sending \n*#run* _language_name_# \nWrite your code here from next line\n\n-Put language name as  cpp,python3, c, java, etc\nNote-: Don't give runtime input statements or try to run infinite loop,it will give error.\n\n--------------------------------------------------\n*2. Ludo*✅ \n-Play Ludo with your friends on whatsapp. \nSend *#help_ludo* to know how to play.\n\n--------------------------------------------------\n*3. Tic Tac Toe Game*✅\n-To play send *#ticgame* _tag the number you want to play with_\n-To end the game early send *#quit_tic*\nType #help_tic for controls\n\n--------------------------------------------------\n*4. Word game*✅\n-To start send #wordgame\n-Type #help_wgame for controls\n\n--------------------------------------------------\n*5.Geeks for Geeks code extractor*✅\n-Get the code from geeks for geeks site according to the asked question.\n-To get the code for particular problem, type \n\n*#gfg#*_Your question_*#*_the language in which you want the code_\n\nEx-: ->*#gfg#merge sort#python*\n     ->*#gfg #kadane algorithm#c++*\n\n--------------------------------------------------\n*6.Match Emoji Game*✅\n\n-To start the game send *#matchgame*\n-For setting level add 2 or 4 or 6 after *#matchgame* with a space\n-For more detail send *#help_match*\n\n--------------------------------------------------\n*7.Minesweeper Game*✅.*\n\n-To start the game send *#minegame* and to chosse a pair send *#mine* _xy_ where x is row and y is column.\n-For more commands of this game use #help_mine.\n-To know how to play visit-https://www.instructables.com/How-to-play-minesweeper/\n\n--------------------------------------------------\n*8.Wikipedia Search*✅.*\n\n-Search anything on wikipedia by sending *#wiki* _title_\n\nEx. *#wiki monkey*\n\n--------------------------------------------------\n*9.Tagger and Counter*✅\n\n-Now you will not miss the tags\nCheck where you were tagged by using *#last_tag* command.\n-Use it again to check second last tag and so on.\n-You can check upto last 50 tags.\n\n-You can also check the total number of messages you have sent by using *#msg_count*\n\n--------------------------------------------------\n*Some admin commands*\n\n- *#add* _919876543210_\n- *#kick* _tag the person you want to remove_\n- *#link* for getting the link of the group\n- *#tagall* \n- *#tagadmins* \n-Note-: You can also add some text after #tagall and #tagadmins.\n\nBot created by *_Karma_*\nGithub link-:https://github.com/Shyguy99/Whatsapp-bot"""
                        driver.reply_message(message.chat_id, message.id, s)
                    elif message.content=="#help_ludo":
                        s = """*Welcome to the I-Bot Ludo*\n\nTo start the game send \n*#ludo*  _and tag the members you want to play with_\n\nTo roll the dice send\n*#ldice*\n\nTo move your _heart_ piece send\n*#lmove h*\n\nTo move your circle piece send \n*#lmove c*\n\nTo see current ludo board send\n*#currludo*\n\nTo quit your game send\n*#quitludo*"""
                        driver.reply_message(message.chat_id, message.id, s)

                    elif message.content == '#help_wgame':
                        s = """*Welcome to the Word Game*\n\n*First join by entering your name send*\n#join _your name_\n\n*To guess the word send*\n#ans _your answer_\n\n*To check the score send*\n#score\n\n*To see the current word enter*\n#currword\n\n*If unable to guess and want to skip to the next word send*\n#skip\n\n*NOTE- IT'LL REQUIRE 3 PEOPLE TO SKIP CURRENT WORD*"""
                        driver.reply_message(message.chat_id, message.id, s)
                    elif message.content == '#help_tic':
                        s = """*Welcome to Tic Tac Toe Game*\n\n*Instructions*\n\nSend the corresponding number to the block where you want to place your symbol*\n\n#1 | #2 | #3\n#4 | #5 | #6\n#7 | #8 | #9\n*To end the game early send *#quit_tic*\n*To see your current game board uses #currtic"""
                        driver.reply_message(message.chat_id, message.id, s)
                    elif message.content == "#help_match":
                        s = """*Welcome to Match Emoji Game*\n\n*To end your current game send #quitmatch\n\n*To guess the pairs send #m with two pairs which you want to try matching\n*Ex. #m xy qr means xth row and yth column match with qth row and rth column\n*To check your curren game send #currmatch"""
                        driver.reply_message(message.chat_id, message.id, s)
                    elif message.content == "#help_mine":
                        s = """*Welcome to Minesweeper Game*\n\n*To choose a position send #mine xy where x is the row and y is column\n*To check your curren game send #currmine \n*To mark a position send #minemark xy\n*To unmark a position send #mineunmark xy."""
                        driver.reply_message(message.chat_id, message.id, s)

                    # execute the python code from the message (owner command)
                    elif "#exec" in message.content:
                        if str(message.sender.id) == YOUR_MOBILE_NUMBER + "@c.us":
                            try:
                                exec(str(message.content))
                            except Exception as e:
                                message.reply_message(str(e))
                        else:
                            message.reply_message("Owner command only!")

                    # ludo game
                    elif "#ludo" in message.content:
                            s = message.content.replace("#ludo", "")
                            s=s.strip()
                            s = s.split(" ")
                            fin_s = []
                            for i in s:
                                fin_s.append(i.replace("@", "") + "@c.us")
                            fin_s.append(message.sender.id)
                            fin_s = set(fin_s)
                            print(fin_s)
                            if len(fin_s) < 2 or len(fin_s) > 4:
                                message.reply_message("Number of players must be between 2 to 4.\nCurrent number of players- {}").format(str(len(fin_s)))
                            else:

                                if len(set(fin_s).intersection(set(ludo_game_dict.keys()))) == 0:

                                    all_parti = set(driver.wapi_functions.getGroupParticipantIDs(message.chat_id))
                                    print(fin_s, all_parti)
                                    if fin_s.issubset(all_parti):
                                        fin_s = list(fin_s)
                                        p1 = fin_s[0]
                                        p2 = fin_s[1]
                                        p3 = None
                                        p4 = None
                                        if len(fin_s) > 2:
                                            p3 = fin_s[2]
                                        if len(fin_s) > 3:
                                            p4 = fin_s[3]
                                        s_time=s_time-1800
                                        ludo_game_dict[message.sender.id] = karma_bot.ludo(driver, message, p1, p2, p3,
                                                                                           p4)
                                        for i in fin_s:
                                            ludo_game_dict[i] = ludo_game_dict[message.sender.id]
                                    else:
                                        message.reply_message("Invalid Players")
                                else:
                                    message.reply_message("One or more player is already in a game.")

                    elif "#ldice" in message.content:
                        if message.sender.id in ludo_game_dict:
                            if ludo_game_dict[message.sender.id].players[message.sender.id].chance == 1:
                                if ludo_game_dict[message.sender.id].dthrow == 0:
                                    s = message.content.replace("#ldice", "")
                                    if len(s) == 1:
                                        s = int(s)
                                    else:
                                        s = 0
                                    ludo_game_dict[message.sender.id].dice(driver, message, s)
                                else:
                                    message.reply_message(
                                        "You have already threw the dice.Move your dice by sending #lmove#h or #lmove#c")
                            else:
                                message.reply_message("Not your chance")
                        else:
                            message.reply_message("You are not in the game")

                    elif "#lmove" in message.content:
                        if message.sender.id in ludo_game_dict:
                            if ludo_game_dict[message.sender.id].players[message.sender.id].chance == 1:
                                if ludo_game_dict[message.sender.id].dthrow == 1:
                                    s = message.content.replace("#lmove", "").lower()
                                    s = s.strip()
                                    if len(s)!=0:
                                        if s == "h" or s == "c":

                                            ludo_game_dict[message.sender.id].move_piece(driver, message, s)
                                            if len(ludo_game_dict[message.sender.id].cur_player_list) == 0:
                                                t = ludo_game_dict[message.sender.id].li_players[:]
                                                for pl in t:
                                                    del ludo_game_dict[pl]
                                        else:
                                            message.reply_message("Wrong piece!! Choose c or h")
                                    else:
                                        message.reply_message("Empty parameter! Choose a piece h or c\nExample:- #lmove c")
                                else:
                                    message.reply_message("First you have to throw the dice by sending #ldice")
                            else:
                                message.reply_message("Not your chance")
                        else:
                            message.reply_message("You are not in the game")

                    elif message.content == "#currludo":
                        if message.sender.id in ludo_game_dict:
                            ludo_game_dict[message.sender.id].current_board(message)

                        else:
                            message.reply_message("You are not in the game.")

                    elif message.content == "#quitludo":
                        if message.sender.id in ludo_game_dict:
                            ludo_game_dict[message.sender.id].quit(driver, message)
                            print(ludo_game_dict[message.sender.id].cur_player_list)
                            if len(ludo_game_dict[message.sender.id].cur_player_list)==1:
                                message.reply_message("Game ended!")
                                del ludo_game_dict[ludo_game_dict[message.sender.id].cur_player_list[0]]
                            del ludo_game_dict[message.sender.id]
                            message.reply_message("Quitted!!")

                        else:
                            message.reply_message("You are not in the game.")








                    # commands for playing word game

                    elif message.content == '#wordgame':
                        if Word.start == 1:

                            message.reply_message(
                                "Word Game already in progress 🏁\n Send #currword to check the word to be guessed.")
                        else:
                            Word.wgame_start(driver, message)
                    elif '#ans' in message.content[:5]:
                        if Word.start == 1:
                            if message.sender.id in Word.players.keys():
                                s=message.content.replace("#ans","")
                                s=s.strip()
                                if len(s)>2:
                                    if Word.ans(driver, message, s):
                                        threading.Thread(target=add_score, args=(Word.players[message.sender.id],)).start()

                                        Word.new_word(driver, message)
                                else:
                                    message.reply_message("Empty Answer.Write your answer after #ans\nCheck current word by sending #currword")


                            else:
                                message.reply_message("You first have to join the game\nSend #join your name")
                        else:
                            Word.wgame_start(driver, message)

                    elif '#join' in str(message.content)[:6]:
                        if Word.start == 1:
                            s=message.content.replace("#join","")
                            s=s.strip()
                            if len(s)!=0:
                                if message.sender.id in Word.players.keys():
                                    message.reply_message("You are already in the game! 🤓\nSend #ans your answer to guess.")

                                elif s in Word.players.values():
                                    message.reply_message("Name already taken!")
                                else:
                                    if p_adding == 0 and s_adding == 0:
                                        p_adding = 1
                                        s_adding = 1
                                        cur.execute('CALL add_player(\'{}\',\'{}\')'.format(message.sender.id, s))
                                        conn.commit()
                                        Word.enter_game(message, s)

                                        p_adding = 0
                                        s_adding = 0
                                    else:
                                        message.reply_message("Wait! Try again")
                            else:
                                message.reply_message("Empty Name!!Write your name after #join.")
                        else:
                            message.reply_message("Game haven't started yet!\nSend #wordgame to start.")

                    elif message.content == '#skip':
                        if Word.start == 1:
                            Word.skip(driver, message)
                        else:
                            message.reply_message("Game not started yet!\nSend #wordgame to start")

                    elif message.content == '#currword':
                        if Word.start == 1:
                            Word.current_word(driver, message)
                        else:
                            Word.wgame_start(driver, message)

                    elif message.content == '#score':
                        Word.show_score(message)

                    #to get tagged msg
                    elif message.content == "#last_tag":
                        all_get_tag_msg.append(message)
                        if db_members == 0:
                            db_members = 1
                            try:
                                cur.callproc('get_last_tag', ("\"" + message.chat_id + "\"", "\"" + message.sender.id + "\""))
                                out = cur.fetchone()
                                db_members = 0
                                if out[0] == None:
                                    message.reply_message("You don't have any tag left or your tags are updating\nTry later.")
                                else:
                                    out = out[0]
                                    msg = out
                                    message.reply_message(msg)
                            except Exception as e:
                                print(e)
                                message.reply_message("Got some error!\nCause can be:Tagged Message Deleted")
                            db_members = 0
                        else:
                            message.reply_message("Wait 2 sec. Let me process last query")

                    #to get msg_count
                    elif message.content == "#msg_count":
                        if db_members == 0:
                            db_members = 1
                            try:
                                cur.callproc('get_msg_count', ("\"" + message.chat_id + "\"", "\"" + message.sender.id + "\""))
                                out = cur.fetchone()
                                db_members = 0
                                if out[0] == None:
                                    message.reply_message("Your message count:\n*1*.")
                                else:
                                    out = out[0]
                                    message.reply_message("Your message count from 06-10-21:\n*{}*".format(out))
                            except Exception as e:
                                print(e)
                            db_members = 0

                        else:

                            message.reply_message("Wait 2 sec. Let me process last query")



                    # commands for playing Tic Tac Toe game
                    elif '#ticgame' in message.content:
                        if message.sender.id not in tic_player_dict:
                            s = message.content.split()
                            if len(s) == 2 and "@" in s[1]:
                                p2 = s[1].replace("@", "") + "@c.us"

                                if p2 not in tic_player_dict:

                                    tic_player_dict[message.sender.id] = karma_bot.tic_tac_game(driver, message,
                                                                                                message.sender.id, p2)
                                    tic_player_dict[p2] = tic_player_dict[message.sender.id]

                                else:
                                    driver.reply_message(message.chat_id, message.id,
                                                         "The person you are trying to play with is already in a game 😐")
                            else:
                                driver.reply_message(message.chat_id, message.id,
                                                     "Wrong Command 🤐!\nType #ticgame tag the person to play with.")

                        else:
                            driver.reply_message(message.chat_id, message.id,
                                                 "You are already in a game!\nQuit it by sending #quit_tic")

                    elif "#" in message.content and len(message.content) == 2 and str(message.content)[1].isdigit():
                        if message.sender.id in tic_player_dict:
                            tic_player_dict[message.sender.id].mark(driver, message, str(message.content)[1])

                            # check if match ended then remove the players
                            if tic_player_dict[message.sender.id].status != "":
                                pl = tic_player_dict[message.sender.id].players
                                del tic_player_dict[pl[0]]
                                del tic_player_dict[pl[1]]
                        else:
                            driver.reply_message(message.chat_id, message.id,
                                                 "You don't have any match!\nType #ticgame tag the person to play with. to start the game.")

                    elif message.content == "#quit_tic":
                        if message.sender.id in tic_player_dict:

                            pl = tic_player_dict[message.sender.id].players
                            pl.remove(message.sender.id)
                            del tic_player_dict[message.sender.id]
                            del tic_player_dict[pl[0]]
                            out1 = "Match quit by {}\n{} you won!!".format("@" + str(message.sender.id).replace("@c.us", ""),
                                                                              "@" + str(pl[0]).replace("@c.us", ""))
                            driver.wapi_functions.sendMessageWithMentions(message.chat_id, out1,"")

                        else:
                            driver.reply_message(message.chat_id, message.id,
                                                 "You don't have any ongoing match!\nType #ticgame tag the person to play with to start the game.")

                    elif message.content == "#currtic":
                        if message.sender.id in tic_player_dict:
                            tic_player_dict[message.sender.id].current_match()

                        else:
                            driver.reply_message(message.chat_id, message.id,
                                                 "You don't have any ongoing match!\nType #ticgame tag the person to play with. to start the game.")




                    # command for getting code from Geeks For Geeks
                    elif "#gfg" in message.content[:5]:
                        GFG.gfg(driver, message, wd, win1, win2)



                    # command for starting match game
                    elif "#matchgame" in message.content:
                        if message.sender.id not in match_player_dict:
                            s = message.content.split()
                            print(s)
                            if len(s) == 2 and s[1].isdigit() and int(s[1]) <= 6:
                                diff = int(s[1])
                                match_player_dict[message.sender.id] = (karma_bot.matcher(driver, message, diff))
                            else:
                                match_player_dict[message.sender.id] = (karma_bot.matcher(driver, message))
                        else:
                            driver.reply_message(message.chat_id, message.id,
                                                 "You already started the game!\n Send #quitmatch to end ur game")

                    # command for quiting match game
                    elif message.content == "#quitmatch":
                        if message.sender.id in match_player_dict:
                            del match_player_dict[message.sender.id]
                            driver.reply_message(message.chat_id, message.id, "Your game deleted!")
                        else:
                            driver.reply_message(message.chat_id, message.id, "You are not in the game!\n Send #matchgame to start.")

                    # command for guessing pairs in match game
                    elif "#m" in message.content[:3]:
                        if message.sender.id in match_player_dict:
                            s = message.content.replace("#m", "")
                            s=s.strip()
                            s = s.split()
                            if len(s)==2:
                                s1 = s[0]
                                s2 = s[1]
                                if s1 == s2:
                                    driver.reply_message(message.chat_id, message.id, "Don't choose same pairs")

                                elif s1.isdigit() and s2.isdigit():
                                    match_player_dict[message.sender.id].guess(driver, message, s1, s2)
                                    if match_player_dict[message.sender.id].corr == pow(match_player_dict[message.sender.id].diff,
                                                                                        2):
                                        del match_player_dict[message.sender.id]

                                else:
                                    driver.reply_message(message.chat_id, message.id, "Wrong input! Please check\n You have choose two pairs Example:- #m 12 34")
                            else:
                                message.reply_message(
                                                     "Wrong input! Please check\n You have choose two pairs \nExample:- #m 12 34")

                        else:
                            driver.reply_message(message.chat_id, message.id, "Your game haven't started yet!!\nStart it by sending #matchgame")

                    # command for checking current match game
                    elif message.content == "#currmatch":
                        if message.sender.id in match_player_dict:
                            match_player_dict[message.sender.id].current_game(driver, message)
                        else:
                            driver.reply_message(message.chat_id, message.id, "Your game haven't started yet!!")





                    # command to start mine game
                    elif "#minegame" in message.content:
                        s = message.content.split()
                        if message.sender.id not in mine_player_dict:

                            if len(s) == 2 and s[1].isdigit() and int(s[1]) <= 6 and int(s[1]) > 0:
                                if message.sender.id not in mine_player_dict:
                                    mine_player_dict[message.sender.id] = karma_bot.mine(driver, message, int(s[1]))

                            elif len(s) == 1:
                                mine_player_dict[message.sender.id] = karma_bot.mine(driver, message)
                            else:
                                driver.reply_message(message.chat_id, message.id, "Wrong input 😐")
                        else:
                            driver.reply_message(message.chat_id, message.id,
                                                 "You have already started the game!🤐\nQuit previous game to start again")

                    # command to choose position in mine map to mine
                    elif "#mine" in message.content:
                        if message.sender.id in mine_player_dict:
                            s = message.content.replace("#mine","")
                            s=s.strip()
                            if len(s)!=0:
                                if s.isdigit():
                                    mine_player_dict[message.sender.id].choose(driver, message, s)
                                    if mine_player_dict[message.sender.id].status == "Lose" or mine_player_dict[
                                        message.sender.id].status == "Won":
                                        del mine_player_dict[message.sender.id]
                                else:
                                    driver.reply_message(message.chat_id, message.id,
                                                         "Invalid command!\n Check valid command using #help_mine")
                            else:
                                message.reply_message("Empty parameter!You have to choose the box using row and column\nExample:-#mine 23")


                        else:
                            driver.reply_message(message.chat_id, message.id,
                                                 "You haven't started your game yet 😅\nStart it by sending #minegame")


                    elif "#minemark" in message.content or "#mineunmark" in message.content:
                        if message.sender.id in mine_player_dict:
                            s=message.content.replace("#minemark","")
                            s=s.replace("#mineunmark","")
                            s=s.strip()
                            if len(s)>0:
                                if s.isdigit():
                                    if "unmark" in s[0]:
                                        mine_player_dict[message.sender.id].mark_pos(driver, message, s[1], 0)
                                    else:
                                        mine_player_dict[message.sender.id].mark_pos(driver, message, s[1], 1)
                                else:
                                    driver.reply_message(message.chat_id, message.id,
                                                         "Invalid command!\n Check valid command using #help_mine")
                            else:
                                message.reply_message("Empty parameter!You have to choose the box\nExample:-#minemark 34")
                        else:
                            driver.reply_message(message.chat_id, message.id,
                                                 "You haven't started your game yet 😅\nStart it by sending #minegame")

                    elif message.content == "#currmine":
                        if message.sender.id in mine_player_dict:
                            s = mine_player_dict[message.sender.id].mine_cov_map
                            s = mine_player_dict[message.sender.id].listtostring(s)
                            driver.reply_message(message.chat_id, message.id, "Your ongoing game!\n\n" + s)
                        else:
                            driver.reply_message(message.chat_id, message.id,
                                                 "You haven't started your game yet 😅\nStart it by sending #minegame")

                    elif message.content == "#quitmine":
                        if message.sender.id in mine_player_dict:
                            del mine_player_dict[message.sender.id]
                            driver.reply_message(message.chat_id, message.id,
                                                 "You have quit your game in middle!🤭\n*LOSER!!*")
                        else:
                            driver.reply_message(message.chat_id, message.id,
                                                 "You haven't started your game yet 😅\nStart it by sending #minegame")


                    elif "#wiki" in message.content[:6]:
                        s=message.content.replace("#wiki","")
                        s=s.strip()
                        if len(s)>2:

                            try:
                                out=wikipedia.page(s[1])
                                message.reply_message('*Title* :{}\n*Source* : {}\n{}'.format(out.title,out.url,out.content))
                            except:
                                message.reply_message("Can't find anything!!")
                        else:
                            message.reply_message("Empty parameter!!You have give some word to be searched\nExample:-#wiki money")

                    elif len(message.content) > 5 and "#run " in message.content[0:5]:

                        try:

                            if COMP.inuse != 1:

                                s = message.content[1:]

                                idx = s.index("#")

                                s1 = s[:idx].strip()

                                lang = s1.replace("run ", "")

                                code = s[idx + 1:]
                                if len(code)>3:

                                    COMP.run(driver,message, lang, code)
                                else:
                                    message.reply_message("Empty Code!!Write some code after the command\Example:-\n#run python3#\nprint(\"Hello World\")")
                            else:

                                message.reply_message("Someone using the compiler.\nLet him/her finish or use #resetrun to terminate")

                        except Exception as e:

                            print(e)

                            message.reply_message("Some Error Occured")
                            COMP.inuse=0


                    elif message.content == "#runlimit":
                        message.reply_message("Limit Left: " + str(200 - int(COMP.r.usage())))
                    elif message.content=="#listlang":
                        s=','.join(COMP.languages)
                        message.reply_message("Languages supported by compiler:-\n"+s)

                    elif message.content=="#resetrun":
                        COMP.inuse=0
                        message.reply_message("Program Terminated!!")



                    #kick and add member command
                    elif "#kick" in message.content[0:6] or "#add" in message.content[:6]:
                        s=message.content.replace("#kick","")
                        s=s.replace("#add","")
                        s=s.strip()
                        if len(s)>1:
                            try:
                                if message.sender.id in driver.wapi_functions.getGroupAdmins(message.chat_id):
                                    if isAdmin(message.chat_id):
                                            if "#kick" in message.content:

                                                    if driver.remove_participant_group(message.chat_id, s.replace("@", "") + "@c.us"):
                                                        print("Participant Removed")
                                                    else:
                                                        message.reply_message("Can't remove")

                                            else:
                                                    if driver.add_participant_group(message.chat_id, s + '@c.us'):
                                                        print("Participant added")
                                                    else:
                                                        message.reply_message(
                                                            "Fail!!\n Number is invalid or Format for adding number is:\n#add 918888888888")

                                    else:
                                        driver.wapi_functions.sendMessage(message.chat_id, "Bot not admin yet")
                                else:
                                    message.reply_message('Sorry!! Admin command')
                            except Exception as e:
                                print(f"Error -> {str(e)}")
                                message.reply_message("Fail!!")
                        else:
                            message.reply_message("No person/number tagged!!")

                    #for getting group link
                    elif message.content=="#link":
                        try:
                            if message.sender.id in driver.wapi_functions.getGroupAdmins(message.chat_id):
                                if isAdmin(message.chat_id):
                                    message.reply_message(driver.wapi_functions.getGroupInviteLink(message.chat_id))

                                else:
                                    driver.wapi_functions.sendMessage(message.chat_id, "Bot not admin yet")
                            else:
                                message.reply_message('Sorry!! Admin command')
                        except Exception as e:
                            print(f"Error -> {str(e)}")
                            message.reply_message("Fail!!")

                    #to get source code
                    elif message.content=="#source":
                        message.reply_message("https://github.com/Shyguy99/Whatsapp-bot")


                    elif "#tagall" in message.content or "#tagadmins" in message.content:

                        if message.sender.id in driver.wapi_functions.getGroupAdmins(message.chat_id):
                                if "#tagadmins" in message.content:
                                    s = message.content.split("#tagadmins")

                                    all_parti = driver.wapi_functions.getGroupAdmins(message.chat_id)
                                else:
                                    s=message.content.split("#tagall")
                                    all_parti = driver.wapi_functions.getGroupParticipantIDs(message.chat_id)
                                msg=s[0]+"\n"
                                msg=msg.replace("#","")

                                for i in all_parti:
                                    msg += ' @{} '.format(i)
                                msg+=s[1]
                                driver.wapi_functions.sendMessageWithMentions(message.chat_id, msg.replace('@c.us', ''), '')

                        else:
                            message.reply_message('Sorry!! Admin command only')




                    #all bot commands
                    elif message.content=="#all_cmd":
                        out=" ,".join(suggest.all_cmd)

                        message.reply_message("All commands :\n"+out)

                    # for wrong command
                    elif message.content!="#on" and message.content!="#off":

                            size=min(12,len(message.content))
                            suggest.suggest(message,message.content[:size])
                elif message.content!="#on":
                    pass
                    #message.reply_message("I-Bot is inactive for this chat ⚰️\nAsk admin to send #on to turn it on.")

            # command for creating sticker from image
            elif (message.type == 'image' or message.type == 'video') and message.chat_id in group and group[message.chat_id]==1 :
                sticker.k_send_sticker(driver, message)



    all_msg=[]
    all_get_coun_msg=[]
    all_get_tag_msg=[]








    def msg_traverse():
        global db_members
        while True:
            if len(all_msg)==0 or db_members==1:
                continue
            else:
                db_members=1
                message=all_msg[0]
                del all_msg[0]

                try:

                    cur.execute(
                        'CALL add_count(\'{}\',\'{}\')'.format("\"" + message.chat_id + "\"", "\"" + message.sender.id + "\""))

                    conn.commit()
                    if (message.type == 'chat') or ((message.type == 'image' or message.type == 'video') and (hasattr(message, 'caption'))):
                        if message.type == 'chat':
                            msg = message.content
                        else:
                            msg = message.caption
                        if "@g.us" in message.chat_id and "@91" in msg:
                            ar = [i for i, j in zip(count(), msg) if j == "@"]
                            all_member = driver.wapi_functions.getGroupParticipantIDs(message.chat_id)
                            tag_ids_us=set()
                            for i in ar:
                                tag_id = msg[i + 1:i + 13]

                                t = tag_id + "@c.us"
                                if t in all_member:
                                    tag_ids_us.add(t)
                            for t in tag_ids_us:
                                t = "@" + t.replace("@c.us", "")
                                msg = msg.replace(t, "")
                            for t in tag_ids_us:
                                s = "Tagged in a {} by {} with the message:\n\n{}".format(message.type,
                                                                                                   message.sender.push_name, msg)

                                cur.execute('CALL add_tag_msg(\'{}\',\'{}\',\'{}\')'.format("\"" + message.chat_id + "\"",
                                                                                            "\"" + t + "\"",
                                                                                            s))
                                conn.commit()
                except Exception as e:
                    print(e)
                db_members=0
                if flag==1:
                    break
                time.sleep(0.3)

    def add_score(pname):
        global s_adding
        while s_adding!=0:
            if flag==1:
                break
            continue
        s_adding=1
        cur.execute('CALL add_score(\'{}\')'.format(pname))
        conn.commit()
        s_adding=0



    threading.Thread(target=msg_traverse).start()

    while True:
        try:
            print("Waiting for QR")
            while not driver.wait_for_login():
                    time.sleep(5)
            print("Bot started")
            bot = "on"  # setting bot status on
            isAdmin = lambda _: driver.wapi_functions.getMe()["wid"] in driver.wapi_functions.getGroupAdmins(_)
        except:
            print("Can't login trying again")
            continue
        while True:
            try:
                if driver.is_logged_in():

                    for contact in driver.get_unread(include_me=True):
                        for i in contact.messages:
                            if i.type=='chat' and i.content=="#quitbot":
                                break
                            threading.Thread(target=main, args=(i,)).start()
                            if time.time()-s_time>3600:
                                flag=1
                                break
                        if flag==1:
                            break
                else:
                    break
                if flag==1:
                    break
            except:
                print("Error Trying Again")

        if flag==1:
            wd.quit()
            driver.quit()
            break


import threading
import multiprocessing
import karma_bot

from selenium import webdriver

options = webdriver.ChromeOptions();
options.headless = True

# options.add_argument('--user-data-dir=./User_Data')
# uncomment the above statement for first you run the bot to create user data folder to store login info

from openwa import WhatsAPIDriver

wd = webdriver.Chrome(options=options)

driver = WhatsAPIDriver(client='chrome',
                        profile='./User_Data')  # remove the profile parameter first time you run the bot as first time there is no folder name this
driver.wait_for_login()

wd.get("https://www.google.com/")  # opening google in one tab
win1 = wd.window_handles[0]
wd.execute_script("window.open('');")  # opening second empty tab
win2 = wd.window_handles[1]

print("Waiting for messages....")

# creating all classes object
word_game = karma_bot.karma_word_game()
sticker = karma_bot.karma_sticker()
tic_game = karma_bot.tic_tac_game()
voice = karma_bot.voice_converse()
GFG = karma_bot.GFG()
quit = karma_bot.quit_bot()

bot="on"          #setting bot status on
all_commands=[]   #all incomming commands will be stored
def reading_message():
        global bot
        global all_commands
        while True:
            for contact in driver.get_unread(include_me=True, include_notifications=True):  # reading all incoming messages
                for message in contact.messages:
                    print(message,"pink")
                    if (message.type=='chat' or message.type=='image' or message.type=='video') and ((hasattr(message, 'caption') and message.caption == '#sticker') or message.content[0:1]=='#') and bot=='on':
                         all_commands.append(message)       #adding all commands to list
                         print(all_commands[-1],"reading")
def running_commands():
       global bot
       global all_commands
       i=0
       while True:
               while i<len(all_commands):           #running commands till there new commands added
                    message=all_commands[i]
                    i+=1
                    print(message,"running")
                    if message.type == 'chat' and message.content == '#on' and (
                            str(message.sender.id) == '918319917110@c.us' or str(message.sender.id) == '919675642959@c.us'):
                        bot = 'on'
                    if message.type == 'chat' and bot == 'on':
                        if message.content == '#off' and (
                                str(message.sender.id) == '918319917110@c.us' or str(message.sender.id) == '919675642959@c.us'):
                            bot = 'off'

                        # commands for help and controls
                        elif (message.content == '#help' or message.content == '#command'):
                            s = """*Welcome to the bot*\n\n*Features*\n\n*1. STICKER MAKER*\nSend any photo with #sticker in caption for sticker *GIF/VIDEOS NOT SUPPORTED RIGHT NOW*\n\n*SEND PHOTO*\nhttps://chat.whatsapp.com/Ie6OO51PR5z8VcBZBY5UiX\n\n*RECEIVE STICKER*\nhttps://chat.whatsapp.com/G5M7sNLTOdBFXb4tcnWYQB\n--------------------------------------------------\n*2. TEXT TO AUDIO*\nSend msg with #voice\n\nEx.-: #voice#This is bot\n\nYou can choose language also hi for hindi,\nen for English,\nbn for bengali,\nfr for French, \nja for japanese\n\nEx-: #voice#mei hu ek bot#hi\n--------------------------------------------------\n*3. Tic Tac Toe Game*\nTo play send *#tic_game#(tag the number you want to play with)*\nTo end the game early send *#end*\nType #help_tic for controls\n--------------------------------------------------\n\n*4. Word game*\nTo start send #wordgame\nType #help_wgame for controls\n--------------------------------------------------\n\n"""
                            driver.reply_message(message.chat_id, message.id, s)
                        elif message.content == '#help_wgame':
                            s = """*Welcome to the Word Game*\n\n*First register by entering your name*\nSend #enter#your name\n\n*To enter a guess enter*\n#ans#your answer\n\n*To check the score enter*\n#score\n\n*After correctly guessing,to go to the next word enter*\n#nex_word\n\n*To see the current word enter*\n#currword\n\n*If unable to guess and want to skip to the next word enter*\n#nex_word\n\n*NOTE- IT'LL REQUIRE 3 PEOPLE TO SKIP FOR THE CURRENT WORD TO GET SKIPPED*"""
                            driver.reply_message(message.chat_id, message.id, s)
                        elif message.content == '#help_tic':
                            s = """*Welcome to Tic Tac Toe Game*\n\n*Instructions*\n\nSend the corresponding number to the block where you want to place your symbol*\n\n#1 | #2 | #3\n#4 | #5 | #6\n#7 | #8 | #9\nTo end the game early send *#end_tic*\n"""
                            driver.reply_message(message.chat_id, message.id, s)


                        # commands for playing word game
                        elif message.content == '#wordgame':
                            word_game.wgame_start(driver, message)
                        elif '#ans' in message.content[:5]:
                            word_game.ans(driver, message)
                        elif '#enter' in str(message.content)[:7]:
                            word_game.enter_game(driver, message)
                        elif message.content == '#nex_word' or message.content == '#skip':
                            word_game.next_word_or_skip(driver, message)
                        elif message.content == '#currword':
                            word_game.current_word(driver, message)
                        elif message.content == '#score':
                            word_game.show_score(driver, message)
                        elif message.content == '#endwgame' and (
                                str(message.sender.id) == '918319917110@c.us' or str(message.sender.id) == '919675642959@c.us'):
                            word_game.end_wgame(driver, message)



                        # commands for playing Tic Tac Toe game
                        elif '#tic_game' in str(message.content)[0:11]:
                            tic_game.tic_game_start(driver, message)
                        elif "#" in message.content[0:3] and len(message.content) < 3:
                            tic_game.turn(driver, message)
                        elif message.content == "#end_tic":
                            tic_game.end_tic_game(driver, message)



                        # command for converting text to speech
                        elif "#voice" in message.content[0:8]:
                            voice.text_to_speech(driver, message)


                        # command for getting code from Geeks For Geeks
                        elif "#gfg" in message.content:
                            GFG.gfg(driver, message, wd, win1, win2)

                        # command for quiting
                        elif message.content == '#quit':
                            quit.quit(driver, wd)

                    # command for creating sticker from image
                    elif message.type == 'image' or message.type == 'video':
                        sticker.k_send_sticker(driver, message)


#using threads for taking commands and running them simultaneously
threading.Thread(target=reading_message).start()
threading.Thread(target=running_commands).start()
# WhatsApp Bot :fire: 
A simple Whatsapp bot made using wa-automate python library with some additional features.

## :sparkles: Installation

You can run this bot directly on your system by just following some steps:
1. Install the required libraries which are mentioned in requirements.txt 
2. Download chrome driver - [Here](https://chromedriver.chromium.org/downloads) and Add the chrome driver path to Environment Variables.
3. Change the three variables in bot.py
    - First Project_Path 
        >Set it to the path of your working folder + "\User_Data"
    
    - Second YOUR_MOBILE_NUMBER
        > add your mobile number here
    
    - Third Jdoodle_clientId
        > add your jdoodle api cliendId
    
    - Fourth Jdoodle_clientSecret
         >add your jdoodle api clientSecret(Get it from jdoodle website mentioned above just sign in and choose free plan.)
4. Now just run bot.py file scan the qr from phone for the first time.        


## :sparkles: Supported features and Commands


###  1. Compiler  ✅ 
- This is to run code using Jdoodle api which is free. Get it from [Here](https://www.jdoodle.com/compiler-api), you have to add your api keys in the code to use this feature.

- Command for this :  <code>#run cpp#</code>        (You can choose any languge in place of cpp,check list of language using <code>#listlang</code> command or from Jdoodle website.)
Write your code here from next line

-   Example:
  
        #run python3#
        for i in range(3):
            print("Hello")
- Most of the language are supported like python3, c, java, etc.

  Note: Don't give runtime input statements or try to run infinite loop,it will give error message. (You can change the code if you want to add this runtime input feature, see jdoodle doc for that.)

---

###  2. Tic Tac Toe Game  ✅ 
- You can play Tic Tac Toe game with anyone or anyone can play this game with other person in whatsapp chat.
- To play send <code>#tic_game#(tag the number you want to play with or type the sender id)</code>  
- Type <code>#help_wgame</code> for controls  
- *Instructions:*  
    Send the corresponding number to the block where you want to place your symbol  
    #1 | #2 | #3  
    #4 | #5 | #6  
    #7 | #8 | #9  
    To end the game early send <code>#quit_tic</code> 

---

### 3. Word game  ✅  
- You can play word guessing game with friends and compete each other.
- To start the game send <code>#wordgame</code>   
- Type <code>#help_wgame</code> for controls and other commands.    
  
---

### 4. Geeks for Geeks code extractor  ✅ 
- Get the code from geeks for geeks site of any problem/question.  
- To get the code for particular problem type #gfg#Your question#the language in which you want the code
-   Example: <code>#gfg#merge sort#python</code> , <code>#gfg#kadane algorithm #c++</code> 
     
> If language is not given while asking then default c++ is taken as language.

---

### 5. Match Emoji Game  ✅ 
- To start the game send <code>#matchgame</code>
- For setting level add 2 or 4 or 6 after #matchgame with a space
- example:<code>#matchgame 4</code>
> If you want to know how to play this game go through this link: [Here](https://en.wikipedia.org/wiki/Concentration_(card_game))

---

### 6. Minesweeper Game  ✅ 
- To start the game send <code>#minegame</code> and to set level place level number 1 to 6 after #minegame with a space.
- example: <code>#minegame 3</code>. Default level is 4
- To choose a box send #mine xy where x is row and y is column.
> If you want to know how to play this game go through this link: [Here](https://www.wikihow.com/Play-Minesweeper)

---

### 7. Wikipedia Search  ✅ 
- Search anything on wikipedia by using <code>#wiki title</code>
- example: <code>#wiki Albert Einstein</code>

---

### 8. Commands only for admins of a group  ✅ 
-  <code>#add 919876543210</code>
-  <code>#kick tag the person</code>
-  <code>#link</code> for link of the group
-  <code>#tagall</code> to tag all the members of the group
-  <code>#tagadmins</code> to tag all the admins of the group
    > Note: You can also add some text after #tagall and #tagadmins.
 
---
 
### 9. Commands only for the owner of the bot  ✅ 
- <code>#on</code> and <code>#off</code> for turning on and off bot for a particular group of whatsapp.  
- <code>#endwgame</code> for ending the word game.  
- <code>#all_cmd</code> to get list of all commands of bot.

---

## :sparkles: Links

[Reference (openwa)](https://github.com/open-wa/wa-automate-python)  


## :sparkles: Contributing

Pull requests are welcome! If you see something you'd like to add, please do. For drastic changes, please open an issue first.
If you want me to add something you are most welcome.


## :sparkles: Disclaimer

This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with WhatsApp or Geeks for Geeks or any of its subsidiaries or its affiliates.  
The official WhatsApp website can be found at [Here](https://whatsapp.com) and official geeks for geeks website can be  
found at [Here](https://www.geeksforgeeks.org/)

## :sparkles: Contact  
For any query you can contact me via email <a href="">readytouse99@gmail.com</a> or if you have any contribution for the project you are welcome.

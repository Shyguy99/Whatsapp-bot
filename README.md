# WhatsApp Bot
A simple Whatsapp bot made using wa-automate python library with some additional features.


## Installation

You can run this bot directly on your system by just following some steps-:
1. Install the required libraries which are mentioned in requirements.txt 
2. Download chrome driver ([Chrome Driver download link](https://chromedriver.chromium.org/downloads) ) and Add the chrome driver path to Environment Variables.
3. Change the three variables in bot.py<br/>
        -First Project_Path ---------Set it to the path of your working folder + "\User_Data"<br/>
        -Second YOUR_MOBILE_NUMBER--------add your mobile number here<br/>
        -Third Jdoodle_clientId-----------add your jdoodle api cliendId<br/>
        -Fourth Jdoodle_clientSecret------add your jdoodle api clientSecret(Get it from jdoodle website mentioned above just sign in and choose free plan.)<br/>
4. Now just run bot.py file scan the qr from phone for the first time.        

## Supported features and Commands

<p>&nbsp;</p>

**1.Compiler** ✅  
This is to run code using Jdoodle api which is free. Get it from https://www.jdoodle.com/compiler-api ,you have to add your api keys in the code to use this feature.</br>

Command for this : </br> #run cpp#        (You can choose any languge in place of cpp,check list of language using #listlang command or from Jdoodle website.)</br>
Write your code here from next line</br>

Ex:-</br>
```
#run python3#
for i in range(3):
     print("Hello")
```
Most of the language are supported like python3, c, java, etc.</br>
Note-: Don't give runtime input statements or try to run infinite loop,it will give error message. (You can change the code if you want to add this runtime input feature, see jdoodle doc for that.)


<p>&nbsp;</p>

**2. Tic Tac Toe Game**✅   
You can play Tic Tac Toe game with anyone or anyone can play this game with other person in whatsapp chat.
To play send </br><code>#tic_game#(tag the number you want to play with or type the sender id)</code>  
Type <code>#help_wgame</code> for controls  
*Instructions-:*  
    Send the corresponding number to the block where you want to place your symbol  
    #1 | #2 | #3  
    #4 | #5 | #6  
    #7 | #8 | #9  
    To end the game early send <code>#quit_tic</code> 



<p>&nbsp;</p>

**3. Word game**✅      
You can play word guessing game with friends and compete each other.
To start the game send <code>#wordgame</code>   
Type #help_wgame for controls and other commands.    
  


<p>&nbsp;</p>

**4. Geeks for Geeks code extractor**✅  
Get the code from geeks for geeks site of any problem/question.  

To get the code for particular problem type #gfg#Your question#the language in which you want the code</br>
Ex-: -><code>#gfg#merge sort#python</code>  
      -><code>#gfg#kadane algorithm #c++</code> 
     
Note-:If language is not given while asking then default c++ is taken as language.       


<p>&nbsp;</p>

**5. Match Emoji Game**✅</br>
To start the game send <code>#matchgame</code>
For setting level add 2 or 4 or 6 after #matchgame with a space</br>
Ex:-<code>#matchgame 4</code></br>
If you want to know how to play this game go through this link-: [Here](https://en.wikipedia.org/wiki/Concentration_(card_game)</br>




<p>&nbsp;</p>

**6. Minesweeper Game**✅</br>
To start the game send <code>#minegame</code> and to set level place level number 1 to 6 after #minegame with a space.</br>
Ex:- <code>#minegame 3</code>. Default level is 4</br>
To choose a box send #mine xy where x is row and y is column.</br>
If you want to know how to play this game go through this link-: [Here](https://www.wikihow.com/Play-Minesweeper)</br>


<p>&nbsp;</p>

**7. Wikipedia Search**✅</br>
Search anything on wikipedia by using
<code>#wiki title</code></br>
Ex:- <code>#wiki Albert Einstein</code>


<p>&nbsp;</p>

**Commands only for admins of a group**</br>
 <code>#add 919876543210</code></br>
 <code>#kick tag the person</code></br>
 <code>#link</code> for link of the group</br>
 <code>#tagall</code> to tag all the members of the group </br>
 <code>#tagadmins</code> to tag all the admins of the group</br>
 Note-: You can also add some text after #tagall and #tagadmins.</br>
 
 
 <p>&nbsp;</p>
 
**Commands only for the owner of the bot**</br>
<code>#on</code> and <code>#off</code> for turning on and off bot for a particular group of whatsapp.  
<code>#endwgame</code> for ending the word game.  
<code>#all_cmd</code> to get list of all commands of bot.

 <p>&nbsp;</p>


## Links

* [Reference (openwa)](https://github.com/open-wa/wa-automate-python)  

<p>&nbsp;</p>

## Contributing

Pull requests are welcome! If you see something you'd like to add, please do. For drastic changes, please open an issue first.
If you want me to add something you are most welcome.


## Disclaimer

This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with WhatsApp or Geeks for Geeks or any of its subsidiaries or its affiliates.  
The official WhatsApp website can be found at https://whatsapp.com. and official geeks for geeks website can be  
found at https://www.geeksforgeeks.org/.

## Contact  
For any query you can contact me via email <a href="">readytouse99@gmail.com</a> or if you have any contribution for the project you are welcome.

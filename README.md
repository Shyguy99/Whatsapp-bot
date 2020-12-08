# WhatsApp Bot
A simple Whasapp bot made using wa-open-python library with some additional features.

**NOTE:** I can't guarantee you will not be blocked by using this method, although it has worked for me. WhatsApp does not allow bots or unofficial clients on their platform, so this shouldn't be considered totally safe.

## Installation

You can run this bot directly on your system by just installing the required libraries,downloading chrome driver (Add the chrome driver path to Environment Variables) and by making little changes that i explained using comments in the code.


## Supported features and Commands
It can do all the simple things that openwa library can,I will not dicuss that here rather i will show you the features that i added in this bot.

**1.Send image as sticker(only image)** ✅  

Any one accept you(if you try it will give error i will fix that later) can convert image to sticker by sending image with #sticker caption.

**2.Convert text to speech** ✅  

Anyone can convert text to voice by sending a simple command.  
Send msg with #voice  
    Ex.-:#voice#This is bot  
You can choose language also hi for hindi,  
en for English,  
bn for bengali,  
fr for French,    
ja for japanese and some more.  
Ex-:#voice#mei hu ek bot#hi  


**3. Tic Tac Toe Game**✅   
You can play Tic Tac Toe game with anyone or anyone can play this game with other person in whatsapp chat.
To play send #tic_game#(tag the number you want to play with or type the sender id)  
Type #help_wgame for controls  
*Instructions-:*  
    Send the corresponding number to the block where you want to place your symbol  
    #1 | #2 | #3  
    #4 | #5 | #6  
    #7 | #8 | #9  
    To end the game early send #end_tic  


**4. Word game**✅      
You can play word guessing game with friends and compete each other.
To start the game send #wordgame   
Type #help_wgame for controls    
   *First register by entering your name*  
   Send #enter#your name  
   
   *To enter a guess enter*  
   #ans#your answer  
   
   *To check the score enter*  
   #score  
   
   *After correctly guessing,to go to the next word enter*  
   #nex_word  
   
   *To see the current word enter*  
   #currword  
   
   *If unable to guess and want to skip to the next word enter*  
   #nex_word  
   
   *NOTE- IT'LL REQUIRE 3 PEOPLE TO SKIP FOR THE CURRENT WORD TO GET SKIPPED*  


**5.Geeks for Geeks code extractor**✅  
Any person can get the code from geeks for geeks site according ro the asked question.  

To get the code for particular problem type #gfg#Your question#the language in which you want the code  
Ex-: ->#gfg#merge sort#python  
     ->#gfg #kadane algorithm #c++ 
     
Note-:If language is not given while asking then default c++ as language is taken.       
     

**Some admin/owner of bot commands**  
-#quit for terminaing the program.  
-#on and #off for pause and play the running bot.  
-#endwgame for closing the word game.  

## Links

* [Reference (openwa)](https://github.com/open-wa/wa-automate-python)  
* [Chrome Driver download link](https://chromedriver.chromium.org/downloads)  

## Contributing

Pull requests are welcome! If you see something you'd like to add, please do. For drastic changes, please open an issue first.
If you want me to add something you are most welcome.


## Disclaimer

This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with WhatsApp or Geeks for Geeks or any of its subsidiaries or its affiliates.  
The official WhatsApp website can be found at https://whatsapp.com. and official geeks for geeks website can be  
found at https://www.geeksforgeeks.org/.

## Contact  
For any query you can contact me via email <a href="">readytouse99@gmail.com</a> or if you have any contribution for the project you are welcome.

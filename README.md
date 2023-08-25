Copyright © 2023 Leo Engelberger

# Description  
enrols you into all lessons meeting your predefined criteria

run the code every time you want to book lessons

by default, it will ask for confirmation before booking your lessons


# Setup  
  
## 1. Preparations  
  
### 1.1 install Python  

Honestly if you don't know how to figure this one by googling it out this bot is not for you.  
make sure to add your python installation to your PATH variable  
  
### 1.2 download this repo  

on the main repo page there is a button code click on it and download it all as a zip file.  
  
## 1.3 unpack  

Unpack the entire zip archive into a folder of your choice  
  
## 2. configuration  
  
### 2.1 update your config.json  

- Open the config.json file in a texteditor of your choice. just make sure to save the file as a json file when you're done editing it.  
- 
###### What does it mean?  
  
`"relevant_days": ["Monday", "Wednesday"],` || Enter The days you want to go to your lessons  
`"course_name": "Manege",` || Enter the name of your sportart  
`"type_name": "Akrobatik",` || Enter the specific type of lesson you are looking for  
`"type_matter": true,` || if there are no types of lessons, or you just want to go to EVERYTHING with the name above, write false  
`"location_matter": true,` || if you don't care about the location write false  
`"locations": "CAB Move", "ASVZ Sport Center",` || list all the locations you want to go to  
`"token": "------------------------------",` || follow the instruction in 1.2  
  
### 2.2 get your token  

- go to schalter.asvz.ch, login and go to your membership overview. once there, right-click anywhere on the page and select inspect. in the window that opened on the right, look for the Network tab.  
- .Once there look for a package called MemberPerson that is not shown in red, click on it to select it and look for the wall of random letters. this is your token.  
- triple-click on it to select it in its entirety and copy it.  
- paste your token in instead of the dashes make sure you include the "Bearer " part with all Spaces.  
  
  
# Run  
## 1 start the bot  
  
  
### 1.1 open the folder you unpacked the bot into. right click and open the terminal.  
  
### 1.2 start the bot  

enter the following command into your terminal:  
'python asvz_bot.py'  
  
## 2 confirm enrolments  
  
### 2.1 All or Individual  

The Bot first lists all possible classes and asks you if you want to book all or choose specific classes, and you are done, if you type n or no read 2.2  

**if you type in y or yes it WILL enrol you in every class and the ASVZ is counting on you.  
> DISCLAIMER: I do not take any responsibility for classes you missed. Check your enrolments regularly to ensure you do not overbook**
  
### 2.2 select individual lessons  

The bot will list every lesson with its time, location, and name. if you enter y or yes you are enrolled, if you enter n or no you're not. 

> **DISCLAIMER: I do not take any responsibility for classes you missed. Check your enrolments regularly to ensure you do not overbook**

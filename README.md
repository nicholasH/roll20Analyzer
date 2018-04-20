# roll20Analyzer
A python program to analyze a roll 20 chat log.


![alt text](https://github.com/nicholasH/roll20Analyzer/blob/master/images/example.png)
# Prerequisites
- must have python 3 installed.
- must have Pip installed.

# Installation guide 
- download the master branch. 
- unzip the master-branch folder 
- In the Command Prompt navigate to the folder and type in this command to install the requirements for this program 

```
pip install -r requirements.txt
```
  
-To start the program type in the Command Prompt 

```
python main.py
```

-Or you can go to to where you saved the master branch folder and click on main.py. If this does not work, right click the file, select open with. If you want to simply run the script, find python.exe and select it 

# Sample Results 
```
{'Eric:'} 1
Total Number of Rolls: 31
Crit success: 4, Nat20: 2, Crit fail: 2, Nat1: 0
dice counter['d6( tot: 14, avg:4.071) ', 'd20( tot: 11, avg:14.455) ', 'd8( tot: 6, avg:3.833) ']
highest roll 46
Top 5 Formual[('rolling 10d6', 10), ('rolling 3d8 +4', 6), ('rolling 1d20 +7', 5), ('rolling 4d6', 4), ('rolling 1d20 +3', 4)]
points 52

{'Saeros Amastacia:'} 1
Total Number of Rolls: 41
Crit success: 3, Nat20: 1, Crit fail: 6, Nat1: 2
dice counter['d20( tot: 26, avg:11.192) ', 'd8( tot: 2, avg:1.5) ', 'd10( tot: 2, avg:7.5) ', 'd6( tot: 1, avg:5.0) ', 'd4( tot: 10, avg:2.3) ']
highest roll 43
Top 5 Formual[('rolling 10d4 + 20', 10), ('rolling 1d20 + 5', 8), ('rolling 1d20 + 7', 7), ('rolling 1d20 + 2', 6), ('rolling 1d20+10', 2)]
points 28

Character Sheets: 

{'Virlym:'} 1
Total Number of Rolls 67
Crit success: 7, Nat20: 2, Crit fail: 10, Nat1: 1
dice counterg['d4( tot: 12, avg:2.333) ', 'd20( tot: 27, avg:12.0) ', 'd6( tot: 20, avg:3.05) ', 'd8( tot: 8, avg:4.125) ']
highest roll 32
Top 5 Formual[('Rolling 5d6 ', 20), ('Rolling 1d20cs>20 + 5[DEX] + 4[PROF] + 1[MAGIC] ', 13), ('Rolling 1d4 ', 5), ('Rolling 1d4 + 5[DEX] + 1[MAGIC] ', 5), ('Rolling 1d20+10 ', 5)]
points 70


[({'Saeros Amastacia:'}, 28), ({'Eric:'}, 62), ({'Virlym:'}, 90)]
```

# Scoring 
Players get points for each crit success they get for example if player rolls a 8 on a d8 they get 8 points added to their total score. Player also get bounce points if they have most of something. The player who get the most Nat20, CritSus, nat1, and critfails get 10 points for each. The player with the highest roll also gets 10 points


# Tagging 
There are 3 types of tag single Tags, timed tags, and indefinite tags
Tags must be typed into the roll20 chat as the game is played as an emote
The tag name must be a single word
The tag Name must have a ^ before the name as in ^tagName

Single tags only tag then next roll with given tag
```
em ^swordAtk (This will make the next roll be tagged with SwordAtk)
```
Time tags will tag everything with the tag for the number of min/hours given
```
/em ^wizTower -5h (All rolls for the next 5 hours will be tagged with wizTower)
/em ^darkCave -30m (All rolls for the next 30 min will be tagged with darkCave)
```

Indefinite tags will everything with the tag until told to stop
```
/em ^underDark -start (All rolls will be tagged with underDark until told to stop)
```
all of these tags can be given the self modifier to make the only apply to the next person who rolls

```
'/em ^wizTower -5h -self (All roll by the next person who rolls will be tagged with wizTower for the next 5 hours)
'/em ^dawfFort -start -self (All roll by the next person who rolls will be tagged with dawfFort until told to stop)
```
The above examples can be the can also be written like this /em ^wizTower -self -5h or /em ^dawfFort -self -start

Ending tags
there are 2 way to end a tag the -end and -endall
-end will stop all indefinite or timed tag early with the tag name given
any player a can end any tag, having a self modifier does not stop another player from ending a tag
```
'/em ^wizTower -end
'/em ^underDark -end
```

-endall will stop all tags
```
em ^end -endall (This will end all current active tags)
```

# Setting 
user name can be saved and auto completed on login screen for roll20. 


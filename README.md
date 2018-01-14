# roll20Analyzer
A python program to analyze a roll 20 chat log.

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


# Limitation of the roll20Analyzer

As of now this program can only counts rolls for Roll 20's default dice roller. Meaning that if a player is rolling from a imported character sheet that roll is not counted in the results. 

# Sample Results 
```
{'Vorastrix:'} 1
Total Number of Rolls 19
Crit success: 3, Nat20: 1, Crit fail: 3, Nat1: 0
Counter({'d6': 10, 'd20': 9})
highest roll 32
Top 5 Formual[('rolling 1d20+8', 2), ('rolling 5d6', 2), ('rolling 1d20', 1), ('rolling 1d20 +3', 1), ('rolling 1d20+13', 1)]
points 32

{'Saeros Amastacia:'} 1
Total Number of Rolls 4
Crit success: 0, Nat20: 0, Crit fail: 0, Nat1: 0
Counter({'d20': 4})
highest roll 22
Top 5 Formual[('rolling 1d20 + -1', 1), ('rolling 1d20 + 1', 1), ('rolling 2d20kh1+5', 1)]
points 0

{'Bubbles Voronda:'} 1
Total Number of Rolls 10
Crit success: 1, Nat20: 0, Crit fail: 1, Nat1: 1
Counter({'d20': 9, 'd10': 1})
highest roll 15
Top 5 Formual[('rolling 1d20 +3', 4), ('rolling d20 +9', 3), ('rolling 1d20+4', 1), ('rolling 1d20 + 2', 1), ('rolling 1d10 +5', 1)]
points 10

[({'Saeros Amastacia:'}, 0), ({'Bubbles Voronda:'}, 10), ({'Vorastrix:'}, 72)]
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

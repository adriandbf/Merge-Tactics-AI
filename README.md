# Merge-Tactics-AI
In this project we tried to make an agent play 
- python 

# Technical decisions and dependencies
## Docker:
TO DO

## Emulator: 
The game clash royal itself is run in an android emulator on our laptops to allow interaction by our program. Because of compability we choose **BlueStacks** as our emulator. BlueStacks is available for Darwin and Windows for free. For Linux an alternative must be considered. Bluestacks can be downloaded directly from the BlueStacks Website: https://www.bluestacks.com/download.html (accesed 25.10.2025)

## Visual models:
In order to get the information we need from the game, our program takes screenshots and then detects the information on those with different visual models. 

For detecting the numbers that indicate the health of the player **EasyOCR** was used. To download EasyOCR run 'pip install easyocr'.

For detecting the classes of the troops in the arena and the classes of the cards that we could play a customized visual model was necessary. Therefore we created two workflows with **Roboflow**. To acces those models follow the instructions below: 
1) If you don't have an account yet, create one for free and sign in on Roboflow (https://roboflow.com/, accesed 25.10.2025).
2) Click on this links to get acces to the model:
    card_detection:
    troop_detection: 
3) Click the fork button to copy the workflow into your account.
4) Click on Deploy to get your workspace name and your API key. Enter both of these in the designated spots in the detections.py file. 

For detecting the amount of elixir ...
TO DO

All other information  from the screen (ranking, player position, ...) is just detected by getting the colour of specific pixels on the screen with **pyautogui** and our program can extract all the information we need from the colour of these pixels. This might be a non intuitive workaround but improved our performance as we don't need to send screenshots to visual models first to detect the information. 


TO DO:
- insert Roboflow links
- Python
- Pytorch
- Windows/Darwin
- EasyOCR
- DQN
- PPO
- pyautogui

# implementing decisions
- reward function

# How to run this project
TO DO
1) install all from above in dependencies
2) Docker stuff
) to start press teh button
update pixel values
run commands

# Results
TO DO 
- PPO survival
- PPO combat
- DQN survival
- DQN combat
- random agent as comparison 

# Possible extensions and open issues
- Currently the model is not rewarded for a whole game in general. The ranking at the end of the game therefore does not influence the training. This could be added if we would want to extend this project.
- Currently there are three actions (clicking one of the three cards). This could be improved by extending the action space to enable the model to also do nothing and wait as an action, sell troups which are on the bank or to change the poitions of troops in the arena.
- Currently the model only gets the classes of the troops on the field as information for the state. If it were to place troops in the arena, it could be implemented as well to give it the positions of all the troops in the arena as information in the state array.
- The current reward function is suitable base for this project. However the impact of selecting a card is not directly influencing a change in the health of players and also a change in the health of players is not always due to the last card played. So just considering the change of the healthbars after clicking a card as a reward is not sufficent if this project is to be extended and used often. 
- The performance of the whole project could be improved as depending on the laptop used we had some troubles with the execuition times. 
- The detection of the numbers of the health of the players (extract_health_from_image() in env.py) is not working perfectly accurate. This could be a focus for further improvement. 
- It would be nice to have an easier way to set up all the variables for the actions class. To get the specific pixel values we always needed to place the mouse in the specific positions, get the pixel data and enter the values manually. 


# Credits
As an inspiration the GitHuB project CRBot-public from krazyness (https://github.com/krazyness/CRBot-public/blob/main/dqn_agent.py, accesed 24.10.2025) was used. The base of the files train.py and agent.py were extracted from the CRBot-public project and then adjusted to our needs. All other files were developed by the authors of this project (Adrian and Vera).

# Authors
Adrian Fudge   
Vera Schmitt 
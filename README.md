# Merge-Tactics-AI
In this python project we tried to make an agent play Clash Royal. The basic structire of this project is shown in the UML diagram (UML_diagram.PNG). A short demonstration of the agent we trained in this project is shown in the demo-video (). We decided to implement and train a DQN strategy. To reward the agent we decided to use the information of the decreasing health bars of the agent itself and the enimies in the game. The SelfDefensePriority is a weight between 0 and 1 that indicates if the priority should be to survive as long as possible or th defeat the other persons as fast as possible. In our training we focused on SelfDefensePriority = 1 (survival mode) and SelfDefensePriority = 0 (combat mode). To implement and train the model pytorch was used. 

The input for our model is a state vector that contains all the information about what is going on in the arena. The first 3 values are the class_ids of the cards that can be choosen to play, the forth value the amount of elixir, the fifth to eight value are the health values of all players, the ninth value idicates which of the health values is our own and the rest of the array is filled up with the class_ids of the troops that are currently in the arena. 

TO DO: insert filename of demo
TO DO: decibe which game we are playing in clash royal and from which level on it is available

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

TO DO: insert Roboflow links

For detecting the amount of elixir **cv2** was used to compare the screenshot taken to template images of the elixir values up to five. With five we can already afford every card so all values above will be set by default to 5 to. To download cv2 run 'pip install opencv-python':

All other information  from the screen (ranking, player position, ...) is just detected by getting the colour of specific pixels on the screen with **pyautogui** and our program can extract all the information we need from the colour of these pixels. This might be a non intuitive workaround but improved our performance as we don't need to send screenshots to visual models first to detect the information. 


# How to run this project
1) TO DO: Docker + set up everything described in Technical decisions and dependencies
2) Start the Clash Royal game in your emulator.
3) As we need a lot of screenshots for this programm to work the pixels need to be specified for the positions of the areas to be captured. Go to the action file and adjust all the values in the init-function to match your game layout. Afterwards check that your screenshots taking by the program show the right areas and functions in the action class are working right. 
4) TO DO: describe which commands to run to start the project 

# Results
TO DO: DQN survival
TO DO: DQN combat
TO DO: random agent as comparison 

# Possible extensions and open issues
- The models could be trained more and compared to each other. 
- Currently the model is not rewarded for a whole game in general. The ranking at the end of the game therefore does not influence the training. This could be added if we would want to extend this project.
- Currently there are three actions (clicking one of the three cards). This could be improved by extending the action space to enable the model to also do nothing and wait as an action, sell troups which are on the bank or to change the poitions of troops in the arena.
- Currently the model only gets the classes of the troops on the field as information for the state. If it were to place troops in the arena, it could be implemented as well to give it the positions of all the troops in the arena as information in the state array.
- The current reward function is suitable base for this project. However the impact of selecting a card is not directly influencing a change in the health of players and also a change in the health of players is not always due to the last card played. So just considering the change of the healthbars after clicking a card as a reward is not sufficent if this project is to be extended and used often. 
- The performance of the whole project could be improved as depending on the laptop used we had some troubles with the execuition times. 
- The detection of the numbers of the health of the players (extract_health_from_image() in env.py) is not working perfectly accurate. This could be a focus for further improvement. 
- It would be nice to have an easier way to set up this project, e. g. all the variables for the actions class. To get the specific pixel values we always needed to place the mouse in the specific positions, get the pixel data and enter the values manually.
- A Linux extension could be implemented as this project only runs on Windows and Darwin.
- Right now only the DQN agent is implemented, However the project is all set up to plug in a PPO agent as well and test it on this one. 
- Our testing is not clean yet and should be implemented better so that it is easier to test. 


# Credits
As an inspiration the GitHuB project CRBot-public from krazyness (https://github.com/krazyness/CRBot-public/blob/main/dqn_agent.py, accesed 24.10.2025) was used. The base of the files train.py and agent.py were extracted from the CRBot-public project and then adjusted to our needs. All other files were developed by the authors of this project (Adrian and Vera).

# Authors
Adrian Fudge   
Vera Schmitt 
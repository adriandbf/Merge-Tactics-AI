# Merge-Tactics-AI
In this python project we tried to make an agent play Clash Royal. The basic structire of this project is shown in the UML diagram (UML_diagram.PNG). A short demonstration of the agent we trained in this project is shown in the demo-video. We decided to implement and train a DQN strategy. To reward the agent we decided to use the information of the decreasing health bars of the agent itself and the enimies in the game. The SelfDefensePriority is a weight between 0 and 1 that indicates if the priority should be to survive as long as possible or th defeat the other persons as fast as possible. In our training we focused on SelfDefensePriority = 1 (survival mode) and SelfDefensePriority = 0 (combat mode). To implement and train the model pytorch was used. 

The input for our model is a state vector that contains all the information about what is going on in the arena. The first 3 values are the class_ids of the cards that can be choosen to play, the forth value the amount of elixir, the fifth to eight value are the health values of all players, the ninth value idicates which of the health values is our own and the rest of the array is filled up with the class_ids of the troops that are currently in the arena. 

# Technical Decisions and Dependencies

## 🐳 Running Merge-Tactics-AI with Docker

### 1. Pull the image
```bash
docker pull adriandbf/merge-tactics-ai:latest
```

### 2. Run the container
```bash
docker run -it --rm \
  -v ./models:/app/models \
  -v ./screenshots:/app/screenshots \
  adriandbf/merge-tactics-ai
```

### 3. Open an interactive shell
```bash
docker run -it --rm --entrypoint bash adriandbf/merge-tactics-ai
```

To run the program, use:
```bash
xvfb-run -a python train.py
```

## Emulator: 
The game clash royal itself is run in an android emulator on our laptops to allow interaction by our program. Because of compability we choose **BlueStacks** as our emulator. BlueStacks is available for Darwin and Windows for free. For Linux an alternative must be considered. Bluestacks can be downloaded directly from the BlueStacks Website: https://www.bluestacks.com/download.html (accesed 25.10.2025)

## Visual models:
In order to get the information we need from the game, our program takes screenshots and then detects the information on those with different visual models. 

For detecting the numbers that indicate the health of the player **EasyOCR** was used. To download EasyOCR run 'pip install easyocr'.

For detecting the classes of the troops in the arena and the classes of the cards that we could play a customized visual model was necessary. Therefore we created two workflows with **Roboflow**. To acces those models follow the instructions below: 
1) If you don't have an account yet, create one for free and sign in on Roboflow (https://roboflow.com/, accesed 25.10.2025).
2) Click on this links to get access to the model:
- [Card Detection Workflow](https://app.roboflow.com/workflows/embed/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ3b3JrZmxvd0lkIjoiWmxZSnR0S0hqOUV6N0tNM2EzWXYiLCJ3b3Jrc3BhY2VJZCI6InhRTzc2cHpRYThNb2MydktxeTlkb093aGlYZzIiLCJ1c2VySWQiOiJ4UU83NnB6UWE4TW9jMnZLcXk5ZG9Pd2hpWGcyIiwiaWF0IjoxNzYxMzI3MzA2fQ.T0j070mcJH8WmDnUBX02XY7LvZv8Wzo9uHBi5D_DA0w)
- [Troop Detection Workflow](https://app.roboflow.com/workflows/embed/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ3b3JrZmxvd0lkIjoiT09SdDJodVFXTXZ5RXVTdTBqWTQiLCJ3b3Jrc3BhY2VJZCI6InhRTzc2cHpRYThNb2MydktxeTlkb093aGlYZzIiLCJ1c2VySWQiOiJ4UU83NnB6UWE4TW9jMnZLcXk5ZG9Pd2hpWGcyIiwiaWF0IjoxNzYxNTM1MzM1fQ.uFf0Tl4BR2AHAshK4e16N2PApn3TVDCNbhF5NSev1gY)

3) Click the fork button to copy the workflow into your account.
4) Click on Deploy to get your workspace name and your API key. Enter both of these in the designated spots in the detections.py file. 

For detecting the amount of elixir **cv2** was used to compare the screenshot taken to template images of the elixir values up to five. With five we can already afford every card so all values above will be set by default to 5 to. To download cv2 run 'pip install opencv-python':

All other information  from the screen (ranking, player position, ...) is just detected by getting the colour of specific pixels on the screen with **pyautogui** and our program can extract all the information we need from the colour of these pixels. This might be a non intuitive workaround but improved our performance as we don't need to send screenshots to visual models first to detect the information. 


# How to run this project
1) Docker + set up everything described in Technical decisions and dependencies
2) Start the Clash Royal game in your emulator.
3) As we need a lot of screenshots for this programm to work the pixels need to be specified for the positions of the areas to be captured. Go to the action file and adjust all the values in the init-function to match your game layout. Afterwards check that your screenshots taking by the program show the right areas and functions in the action class are working right. 
4) Running the train.py file starts the program

# Results
 ## 📊 Model Performance

### Troop Distribution Per Episode
![Accuracy Graph](graphs/hist_troops_deployed.png)
Troops Deployed per Episode
The Troops Deployed per Episode graph shows fluctuating deployment behavior for both the Survival and Combat models. The Combat strategy exhibits more aggressive troop deployment, with frequent peaks and higher variance, suggesting a reactive or opportunistic approach. The Survival strategy, while generally more conservative, demonstrates a few sharp increases that may correspond to critical in-game situations or learning adjustments over episodes.

### Total Reward Distribution Per Episode
![Loss Graph](graphs/hist_total_reward.png)
Total Reward per Episode
In the Total Reward per Episode graph, the Combat model achieves higher rewards overall but also experiences larger drops, indicating a riskier and more volatile strategy. The Survival model, by contrast, maintains relatively stable but lower rewards, reflecting a safer, more consistent approach that prioritizes longevity over short-term gains. This contrast highlights a trade-off between aggressive optimization and sustained performance stability.

For corrrectly interpreting this values it is important to know that in survival mode there are only negative rewards as the reward is the health decrease whlie in the combat model the rewards are only positive for decreasing the health of enimies. Also in the combat mode the health of all the enemies is added up, which leads to the two rewards not having the same scale and beeing comparable. Other values (e. g. positive values in the survival reward function) might be due to missdetecting the health numbers and default beeing set to 10 if teh detection goes wrong. 
Also the total amount at the end of the game does not directly indicate how good it plays. It is only temporary accurate for the step that is taken and not as a total sum of the game. 


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
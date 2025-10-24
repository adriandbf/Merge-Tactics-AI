# Merge-Tactics-AI
TO DO: Introduction
An AI agent that interacts with the merge tactics environment to play games.


# Technical decisions/Implementing decisions
TO DO:
- Roboflow
- Bluestacks
- Python
- Pytorch
- Windows/Darwin
- EasyOCR
- DQN
- PPO

# How to run this project
TO DO

# Possible extensions and open issues
- Currently the model is not rewarded for a whole game in general. The ranking at the end of the game therefore does not influence the training. This could be added if we would want to extend this project.
- Currently there are three actions (clicking one of the three cards). This could be improved by extending the action space to enable the model to also do nothing and wait as an action, sell troups which are on the bank or to change the poitions of troops in the arena.
- Currently the model only gets the classes of the troops on the field as information for the state. If it were to place troops in the arena, it could be implemented as well to give it the positions of all the troops in the arena as information in the state array.
- The current reward function is suitable base for this project. However the impact of selecting a card is not directly influencing a change in the health of players and also a change in the health of players is not always due to the last card played. So just considering the change of the healthbars after clicking a card as a reward is not sufficent if this project is to be extended and used often. 
- The performance of the whole project could be improved as depending on the laptop used we had some troubles with the execuition times. 
- The detection of the numbers of the health of the players (extract_health_from_image() in env.py) is not working perfectly accurate. This could be a focus for further improvement. 

# Credits
As an inspiration the GitHuB project CRBot-public from krazyness (https://github.com/krazyness/CRBot-public/blob/main/dqn_agent.py, accesed 24.10.2025) was used. The base of the files train.py and agent.py were extracted from the CRBot-public project and then adjusted to our needs. All other files were developed by the authors of this project (Adrian and Vera).
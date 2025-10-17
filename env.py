from actions import Actions
from detections import Detection
import numpy as np
import time
import os

# to do: refactor-statesize in constant

class MergeTacticsEnv:
    def __init__(self):
        # maximal state_size -3 troops in the arena can be included in the calculations
        self.state_size = 20         
        self.action_size = 3         
        self.state = np.zeros(self.state_size, dtype=np.int32)  
        self.done = False
        self.actor = Actions()
        self.detector = Detection()

        self.screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(self.screenshots_dir, exist_ok=True)

    # Once docker is setup were gonna have to fix the detection file and make the program more modular
    # def setup_roboflow(self):
    #     api_key = os.getenv('ROBOFLOW_API_KEY')
    #     if not api_key:
    #         raise ValueError("ROBOFLOW_API_KEY environment variable is not set. Please check your .env file.")
        
    #     return InferenceHTTPClient(
    #         api_url="http://localhost:9001"
    #         api_key=api_key
    #     )
    
    # def setup_card_roboflow(self):
    #     api_key = os.getenv('ROBOFLOW_API_KEY')
    #     if not api_key:
    #         raise ValueError("ROBOFLOW_API_KEY environment variable is not set. Please check your .env file.")
        
    #     return InferenceHTTPClient(
    #         api_url="http://localhost:9001",
    #         api_key=api_key
    #     )

    # this method should start a new game and reset the parameters
    def reset(self):
        self.actor.press_replay_button()
        self.done = False
        self.state = self._get_observation()
        return self.state

    # a function that performs a given action in the actual game and returns the next_state, reward, done-flag
    # TO DO: implement done flag
    def step(self, action_index):
        # Check if match ended TODO

        # assume action_index from 0 to 2
        self.actor.select_card(action_index)
        self.actor.capture_area()
        self.actor.capture_card_area()

        next_state = self._get_observation()
        reward = self._compute_reward(self.state, next_state)
        self.state = next_state

        return next_state, reward, self.done
    
    def _get_observation(self):
        # detect troops + cards
        troops = self.detector.detect_troops()
        cards = [self.detector.detect_card(i) for i in range(3)]
        troop_classes = [t['class_id'] for t in troops]
        card_classes = [c[0]['class_id'] if c else 0 for c in cards]

        obs = card_classes + troop_classes
        if len(obs) < self.state_size:
            obs += [0] * (self.state_size - len(obs))
        return np.array(obs[:self.state_size], dtype=np.int32)

    def _compute_reward(self, old_state, new_state):
        # Simple placeholder: +1 if any troop or card class changes
        return 1 if not np.array_equal(old_state, new_state) else 0
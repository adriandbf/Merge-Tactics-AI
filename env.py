from actions import Actions
from detections import Detection
import numpy as np
import time
import os
import easyocr
from PIL import Image, ImageOps

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
        self.health_p1 = 12
        self.health_p2 = 12
        self.health_p3 = 12
        self.health_p4 = 12
        self.reader = easyocr.Reader(['en'], gpu=False)

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
        # improvement: add error functions if int detection didn't work
        # improvement ideas: detect player we are actually playing and only take his loss of health
        # problem: changes may need time, so probably we are also just seeing the outcome of earlier 
        # actions and not from tej current one

        # weight between 0 and 1 that determines how much emphasize the reward function gives to defending 
        # the own health in comparison to brining the health of the other charakters down
        # 0.5 -> both are treatet as equaly important
        # 1 -> only defending the own health is important 
        # 0 -> only brining the health of the other charakters down is important 
        weight = 0.5

        # default value if healthe couldn't be detected
        health_default = 6

        self.actor.capture_healthbars()

        new_health_p1 = self.extract_health_from_image("screenshots/health_p1.png", health_default)
        new_health_p2 = self.extract_health_from_image("screenshots/health_p1.png", health_default)
        new_health_p3 = self.extract_health_from_image("screenshots/health_p1.png", health_default)
        new_health_p4 = self.extract_health_from_image("screenshots/health_p1.png", health_default)

        print(f"New healths: {new_health_p1} {new_health_p2} {new_health_p3} {new_health_p4}")

        # to do: adjust, now assuming p4 is self
        # losing parts of the own health is giving negativ reward while all losses of enemies health 
        # give positive reward (including all players, not only the one we are currently playing)
        reward = weight * (self.health_p4 - new_health_p4) * (-1) + (1-weight) * (self.health_p1 - new_health_p1 + self.health_p2 - new_health_p2 + self.health_p3 - new_health_p3)
        print(f"Reward: {reward}")

        # setting the new values as the health values as a base for the next step
        self.health_p1 = new_health_p1
        self.health_p2 = new_health_p2
        self.health_p3 = new_health_p3
        self.health_p4 = new_health_p4

        # Simple placeholder: +1 if any troop or card class changes
        # return 1 if not np.array_equal(old_state, new_state) else 0

        return reward
    

    def extract_health_from_image(self, file_path, default_health):
        try:
            img = Image.open(file_path)
            img = ImageOps.invert(img.convert('RGB'))
            img = img.resize((img.width * 2, img.height * 2))
            img_np = np.array(img)
            results = self.reader.readtext(img_np)
            print(results)

            if results:
                _, text, _ = results[0]
                clean_text = text.strip()
                number = int(clean_text)
                if 0 <= number <= 12:
                    return number
                else:
                    return default_health
            else:
                return default_health
        except Exception:
            return default_health
    
# testing screen capture functions
def main():

    m = MergeTacticsEnv()

    old_state = np.array([5, 10, 10])
    new_state = np.array([7, 9, 11])

    m._compute_reward(old_state, new_state)


if __name__ == "__main__":
    main()
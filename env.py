from actions import Actions
from detections import Detection
import numpy as np

# to do: refactor-statesize in constant

class ClashRoyaleEnv:
    def __init__(self):
        # maximal state_size -3 troups in the arena can be included in the calculations
        self.state_size = 20         
        self.action_size = 3         
        self.state = np.zeros(self.state_size, dtype=np.int32)  
        self.done = False

    # this method should start a new game and reset the parameters
    def reset(self):
        Actions.press_replay_button

    # a function that performs a given action in teh actual game and returns the next_state, reward, done-flag
    # TO DO: implement done flag
    # TO DO: implement reward
    def step(self, action_index):
        # assume action_index from 0 to 2
        Actions.select_card()
        Actions.capture_area
        Actions.capture_card_area

        # get detection arrays
        detector = Detection()
        troops = detector.detect_troops()
        card_1 = detector.detect_card(0)
        card_2 = detector.detect_card(1)
        card_3 = detector.detect_card(2)

        # extract class information 
        troops_classes = []
        for troop in troops:
            troops_classes.append(troop['class_id'])
        card_1_class = card_1['class_id']
        card_2_class = card_2['class_id']
        card_3_class = card_3['class_id']

        next_state_array = [card_1_class] + [card_2_class] + [card_3_class] + troops_classes

        if len(next_state_array) < self.state_size:
            next_state_array += [0] * (self.state_size - len(state_list))
        else:
            next_state_array = next_state_array[:self.state_size]

        next_state = np.array(next_state_array, dtype=np.int32)
        
        return next_state, 1, False

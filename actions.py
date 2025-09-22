import pyautogui
import os
from datetime import datetime
import time
import platform

class Actions:
    def __init__(self):
        self.os_type = platform.system()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_folder = os.path.join(self.script_dir, 'main_images')
        
        if self.os_type == "Darwin":
            self.TOP_LEFT_X = 1036
            self.TOP_LEFT_Y = 284
            self.BOTTOM_RIGHT_X = 1442
            self.BOTTOM_RIGHT_Y = 784
            self.FIELD_AREA = (self.TOP_LEFT_X, self.TOP_LEFT_Y, self.BOTTOM_RIGHT_X, self.BOTTOM_RIGHT_Y)

            self.WIDTH = self.BOTTOM_RIGHT_X - self.TOP_LEFT_X
            self.HEIGHT = self.BOTTOM_RIGHT_Y - self.TOP_LEFT_Y

            self.CARD_BAR_X = 1058
            self.CARD_BAR_Y = 856
            self.CARD_BAR_WIDTH = 1312 - 1058
            self.CARD_BAR_HEIGHT = 956 - 856
        elif self.os_type == "Windows":
            pass #TODO: Get cords for windows device when blue stacks height is sized to full screen and the window is as far right as possible without cutting off the application

        self.card_keys = {
            0: '1',  # Changed from 1 to 0
            1: '2',  # Changed from 2 to 1
            2: '3',  # Changed from 3 to 2
        }
        
        self.current_card_positions = {}

    def capture_area(self, save_path):
        screenshot = pyautogui.screenshot(region=(self.TOP_LEFT_X, self.TOP_LEFT_Y, self.WIDTH, self.HEIGHT))
        screenshot.save(save_path)

    def capture_card_area(self, save_path):
        """Capture screenshot of card area"""
        screenshot = pyautogui.screenshot(region=(
            self.CARD_BAR_X, 
            self.CARD_BAR_Y, 
            self.CARD_BAR_WIDTH, 
            self.CARD_BAR_HEIGHT
        ))
        screenshot.save(save_path)

        card_width = self.CARD_BAR_WIDTH
        cards = []

        for i in range(3):
            left = i * card_width
            card_img = screenshot.crop((left, 0, left * card_width, self.CARD_BAR_HEIGHT))
            save_path = os.path.join(self.script_dir, 'screenshots', f"card_{i+1}.png")
            card_img.save(save_path)
            cards.append(save_path)

        return cards
    
    def count_elixir(self):
        #TODO
        pass

# testing screen capture functions
def main():
    a = Actions()
    a.capture_area("area.png")
    a.capture_card_area("card_area.png")

if __name__ == "__main__":
    main()
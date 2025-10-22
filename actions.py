import pyautogui
import cv2
import os
import numpy as np
from datetime import datetime
import time
import platform
import easyocr

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
            self.card_width = self.CARD_BAR_WIDTH/3

            self.ELIXIR_X = 1322
            self.ELIXIR_Y = 900
            self.ELIXIR_WIDTH = 1381 - 1322
            self.ELIXIR_HEIGHT = 961 - 900

            # to do: insert actual values, this are only placeholders
            self.HEALTH_WIDTH = 1
            self.HEALTH_HEIGHT = 1
            self.HEALTH_Y = 1
            self.HEALTH_X_P1 = 1
            self.HEALTH_X_P2 = 1
            self.HEALTH_X_P3 = 1
            self.HEALTH_X_P4 = 1

            # to do: insert actual values, this are only placeholders
            self.HEALTHBAR_Y = 1
            self.HEALTHBAR_X_P1 = 1
            self.HEALTHBAR_X_P2 = 1
            self.HEALTHBAR_X_P3 = 1
            self.HEALTHBAR_X_P4 = 1

        elif self.os_type == "Windows":
            self.TOP_LEFT_X = 1476
            self.TOP_LEFT_Y = 366
            self.BOTTOM_RIGHT_X = 1796
            self.BOTTOM_RIGHT_Y = 717
            self.FIELD_AREA = (self.TOP_LEFT_X, self.TOP_LEFT_Y, self.BOTTOM_RIGHT_X, self.BOTTOM_RIGHT_Y)

            self.WIDTH = self.BOTTOM_RIGHT_X - self.TOP_LEFT_X
            self.HEIGHT = self.BOTTOM_RIGHT_Y - self.TOP_LEFT_Y

            self.CARD_BAR_X = 1476
            self.CARD_BAR_Y = 807
            self.CARD_BAR_WIDTH = 1707 - 1476
            self.CARD_BAR_HEIGHT = 902 - 807
            self.card_width = self.CARD_BAR_WIDTH/3

            self.ELIXIR_X = 1728
            self.ELIXIR_Y = 854
            self.ELIXIR_WIDTH = 1769 - 1728
            self.ELIXIR_HEIGHT = 896-854

            self.HEALTH_WIDTH = 12
            self.HEALTH_HEIGHT = 11
            self.HEALTH_Y = 112
            self.HEALTH_X_P1 = 1492
            self.HEALTH_X_P2 = 1615
            self.HEALTH_X_P3 = 1737
            self.HEALTH_X_P4 = 1860

            self.HEALTHBAR_Y = 121
            self.HEALTHBAR_X_P1 = 1385
            self.HEALTHBAR_X_P2 = 1508
            self.HEALTHBAR_X_P3 = 1630
            self.HEALTHBAR_X_P4 = 1754

        self.card_keys = {
            0: '1',  # Changed from 1 to 0
            1: '2',  # Changed from 2 to 1
            2: '3',  # Changed from 3 to 2
        }
        
        self.current_card_positions = {}

        # click in game window for keyboard presses to show up there without performing any action
        if self.os_type == "Windows":
            pyautogui.click(1407, 868)

        elif self.os_type == "Darwin":
            pyautogui.click(1407, 868)

    def capture_area(self, save_path=None):
        if save_path is None:
            save_path = os.path.join(self.script_dir, "screenshots", "area.png")
        screenshot = pyautogui.screenshot(region=(self.TOP_LEFT_X, self.TOP_LEFT_Y, self.WIDTH, self.HEIGHT))
        screenshot.save(save_path)

    def capture_card_area(self, save_path=None):
        """Capture screenshot of card area"""
        if save_path is None:
            save_path = os.path.join(self.script_dir, "screenshots", "card_area.png")
        screenshot = pyautogui.screenshot(region=(
            self.CARD_BAR_X, 
            self.CARD_BAR_Y, 
            self.CARD_BAR_WIDTH, 
            self.CARD_BAR_HEIGHT
        ))
        screenshot.save(save_path)

        cards = []

        for i in range(3):
            left = i * self.card_width
            card_img = screenshot.crop((left, 0, left + self.card_width, self.CARD_BAR_HEIGHT))
            save_path = os.path.join(self.script_dir, 'screenshots', f"card_{i+1}.png")
            card_img.save(save_path)
            cards.append(save_path)

        return cards

    # TODO: fix windows
    def count_elixir(self):
        """Detect current elixir count using template or pixel-based detection depending on OS."""
        try:
            if self.os_type == "Darwin":
                # macOS: template image matching
                region = (
                self.ELIXIR_X,
                self.ELIXIR_Y,
                self.ELIXIR_WIDTH,
                self.ELIXIR_HEIGHT
                )
                for i in range(0, 5, 1):  # check higher elixir values first
                    image_file = os.path.join(self.images_folder, f"{i}elixir.png")
                    if not os.path.exists(image_file):
                        continue  # skip if missing

                    try:
                        location = pyautogui.locateOnScreen(
                            image_file,
                            confidence=0.5,
                            grayscale=True,
                            #region=region
                        )
                        if location:
                            print(f"[DEBUG] Elixir image matched: {i} ({image_file})")
                            return i
                    except Exception as e:
                        pass
                        #print(f"[ERROR] locateOnScreen failed for {image_file}: {e}") # for debugging

                print("[WARN] No elixir image matched — assuming 5")
                return 5

            elif self.os_type == "Windows":
                # Windows: count purple bars by pixel color sampling
                target_color = (225, 128, 229)
                tolerance = 80
                count = 0

                # The x-range and y position should match where bars appear in your resolution
                for x in range(1512, 1892, 38):  # adjust spacing if needed
                    try:
                        r, g, b = pyautogui.pixel(x, 989)
                        if (
                            abs(r - target_color[0]) <= tolerance and
                            abs(g - target_color[1]) <= tolerance and
                            abs(b - target_color[2]) <= tolerance
                        ):
                            count += 1
                    except Exception as e:
                        print(f"[WARN] pixel read failed at x={x}: {e}")

                print(f"[DEBUG] Elixir detected (Windows): {count}")
                return min(count, 5)

            else:
                print("[WARN] Unsupported OS type — returning 0")
                return 0

        except Exception as e:
            print(f"[ERROR] Elixir detection failed: {e}")
            return 0

    def select_card(self,action_nr):
        # assume action_nr between 0 and 2
        pyautogui.click(self.CARD_BAR_X + ((action_nr +1) - 0.5) * self.card_width , self.CARD_BAR_Y + 0.5 * self.CARD_BAR_HEIGHT)
    
    def press_replay_button(self):

        if self.os_type == "Windows":
            self.REPLAY_BUTTON_X = 1527
            self.REPLAY_BUTTON_Y = 870

        elif self.os_type == "Darwin":
            self.REPLAY_BUTTON_X = 1123
            self.REPLAY_BUTTON_Y = 904

        pyautogui.click(self.REPLAY_BUTTON_X, self.REPLAY_BUTTON_Y)

    def capture_healthbars(self):
        
        save_path = os.path.join(self.script_dir, "screenshots", "health_p1.png")
        screenshot = pyautogui.screenshot(region=(self.HEALTH_X_P1, self.HEALTH_Y, self.HEALTH_WIDTH, self.HEALTH_HEIGHT))
        screenshot.save(save_path)
        
        save_path = os.path.join(self.script_dir, "screenshots", "health_p2.png")
        screenshot = pyautogui.screenshot(region=(self.HEALTH_X_P2, self.HEALTH_Y, self.HEALTH_WIDTH, self.HEALTH_HEIGHT))
        screenshot.save(save_path)

        save_path = os.path.join(self.script_dir, "screenshots", "health_p3.png")
        screenshot = pyautogui.screenshot(region=(self.HEALTH_X_P3, self.HEALTH_Y, self.HEALTH_WIDTH, self.HEALTH_HEIGHT))
        screenshot.save(save_path)

        save_path = os.path.join(self.script_dir, "screenshots", "health_p4.png")
        screenshot = pyautogui.screenshot(region=(self.HEALTH_X_P4, self.HEALTH_Y, self.HEALTH_WIDTH, self.HEALTH_HEIGHT))
        screenshot.save(save_path)

    def get_current_player_position(self):
        # returns a value between 1 and 4 to indicate our position in the healthbars, or default_position if detection didn't work
        # red healthbar color values: (237, 101, 101)
        # blue healthbar color values: (151, 209, 234)
        self.default_position = 1

        colour1 = pyautogui.pixel(self.HEALTHBAR_X_P1, self.HEALTHBAR_Y)
        colour2 = pyautogui.pixel(self.HEALTHBAR_X_P2, self.HEALTHBAR_Y)
        colour3 = pyautogui.pixel(self.HEALTHBAR_X_P3, self.HEALTHBAR_Y)
        colour4 = pyautogui.pixel(self.HEALTHBAR_X_P4, self.HEALTHBAR_Y)

        if colour1 == (151, 209, 234):
            return 1
        elif colour2 == (151, 209, 234):
            return 2
        elif colour3 == (151, 209, 234):
            return 3
        elif colour4 == (151, 209, 234):
            return 4
        else:
            return self.default_position


        


# testing screen capture functions
def main():

    folder = "screenshots"

    a = Actions()
    a.capture_area(os.path.join(folder, "area.png"))
    a.capture_card_area(os.path.join(folder, "card_area.png"))
    a.select_card(1)
    a.capture_healthbars()
    a.get_current_player_position()

if __name__ == "__main__":
    main()
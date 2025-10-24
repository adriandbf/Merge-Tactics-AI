import pyautogui
import cv2
from PIL import ImageGrab
import os
import numpy as np
import platform


class Actions:
    def __init__(self):
        self.os_type = platform.system()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_folder = os.path.join(self.script_dir, 'main_images')
        
        if self.os_type == "Darwin":
            self.TOP_LEFT_X = 1036
            self.TOP_LEFT_Y = 334
            self.BOTTOM_RIGHT_X = 1442
            self.BOTTOM_RIGHT_Y = 834
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
            self.HEALTH_WIDTH = 1096 - 1083
            self.HEALTH_HEIGHT = 147 - 137
            self.HEALTH_Y = 137
            self.HEALTH_X_P1 = 1083
            self.HEALTH_X_P2 = 1210
            self.HEALTH_X_P3 = 1339
            self.HEALTH_X_P4 = 1467

            # to do: insert actual values, this are only placeholders
            self.HEALTHBAR_Y = 144
            self.HEALTHBAR_X_P1 = 969
            self.HEALTHBAR_X_P2 = 1097
            self.HEALTHBAR_X_P3 = 1225
            self.HEALTHBAR_X_P4 = 1353

            # to do: insert actual values, this are only placeholders
            # a pixel with a colour that it only has when a game is done
            self.IS_DONE_X = 1006*2 # Multiplied by 2 for retina display
            self.IS_DONE_y = 267*2
            self.IS_DONE_COLOUR = (26,26,32)

            # to od: replace this values with the actual values
            # a pixel in all the placement bars that changes to yellow if it is our bar, that exact yellow is the color you should enter
            self.RANKING_X = 1
            self.RANKING_FRIST_Y = 1
            self.RANKING_SECOND_Y = 2
            self.RANKING_THIRD_Y = 3
            self.RANKING_FOURTH_Y = 4
            self.RANKING_SELF_COLOR = (1,1,1)

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

            # a pixel with a colour that it only has when a game is done
            self.IS_DONE_X = 1414
            self.IS_DONE_y = 189
            self.IS_DONE_COLOUR = (22,22,15)

            # to od: replace this values with the actual values
            # a pixel in all the placement bars that changes to yellow if it is our bar, that exact yellow is the color you should enter
            self.RANKING_X = 1551
            self.RANKING_FRIST_Y = 294
            self.RANKING_SECOND_Y = 413
            self.RANKING_THIRD_Y = 527
            self.RANKING_FOURTH_Y = 642
            self.RANKING_SELF_COLOR = (229, 172, 46)

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
        """Detect elixir"""
        try:
            if self.os_type == "Darwin":
                # macOS: template image matching
                region = (
                    self.ELIXIR_X,
                    self.ELIXIR_Y,
                    self.ELIXIR_WIDTH + self.ELIXIR_X,
                    self.ELIXIR_HEIGHT + self.ELIXIR_Y
                )

                # Take region screenshot (high precision, retina-safe)
                screenshot = ImageGrab.grab(bbox=region)
                screen_rgb = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

                best_match_val = 0
                best_elixir = None

                for i in range(5, -1, -1):  # check higher elixir values first
                    image_file = os.path.join(self.images_folder, f"{i}elixir.png")
                    if not os.path.exists(image_file):
                        continue  # skip if missing

                    template = cv2.imread(image_file, cv2.IMREAD_COLOR)
                    if template is None:
                        continue

                    res = cv2.matchTemplate(screen_rgb, template, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(res)

                    if max_val > 0.9 and max_val > best_match_val:
                        best_match_val = max_val
                        best_elixir = i
                if best_elixir is not None:
                    print(f"[DEBUG] Elixir detected: {best_elixir} (confidence={best_match_val:.2f})")
                    self.last_elixir = best_elixir
                    return best_elixir
                else:
                    print("[WARN] No elixir match found — assuming previous or max (5)")
                    return getattr(self, "last_elixir", 5)

            else:
                # fallback or Windows implementation
                return 5

        except Exception as e:
            print(f"[ERROR] Elixir detection failed: {e}")
            return getattr(self, "last_elixir", 0)

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
        
    def detect_is_done(self):
        color = pyautogui.pixel(self.IS_DONE_X, self.IS_DONE_y)
        if color == self.IS_DONE_COLOUR:
            return True
        else:
            return False
        
    # this function should only be called in the is_done state for right values
    # returns the ranking from 1 to 4 
    def get_ranking(self):

        default_ranking = 4

        color = pyautogui.pixel(self.RANKING_X, self.RANKING_FRIST_Y)
        if color == self.RANKING_SELF_COLOR:
            return 1
        
        color = pyautogui.pixel(self.RANKING_X, self.RANKING_SECOND_Y)
        if color == self.RANKING_SELF_COLOR:
            return 2
        
        color = pyautogui.pixel(self.RANKING_X, self.RANKING_THIRD_Y)
        if color == self.RANKING_SELF_COLOR:
            return 3
        
        color = pyautogui.pixel(self.RANKING_X, self.RANKING_FOURTH_Y)
        if color == self.RANKING_SELF_COLOR:
            return 4
        
        return default_ranking
        

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
from inference_sdk import InferenceHTTPClient
import os
import easyocr
import platform
from PIL import Image, ImageOps
import numpy as np
import cv2


client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    # insert your api key here
    api_key="*************"
)

class Detection:

    def __init__(self):
        self.os_type = platform.system()
        self.reader = easyocr.Reader(['en'], gpu=False)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_folder = os.path.join(self.script_dir, 'elixir_template_images')

    def detect_troops(self):
        try:
            image_path = f"screenshots/arena.png"
            result = client.run_workflow(
                workspace_name="vera-8vhle",
                workflow_id="troopdetection",
                images={"image": image_path},
                use_cache=True
            )
            preds = result[0]["predictions"]["predictions"]
            return preds
        except Exception as e:
            print("Troop detection failed:", e)
            return []

    def detect_card(self, card_nr):
        image_path = f"screenshots/card_{card_nr+1}.png"
        try:
            result = client.run_workflow(
                workspace_name="vera-8vhle",
                workflow_id="carddetection-2",
                images={"image": image_path},
                use_cache=True
            )
            preds = result[0]["predictions"]["predictions"]
            return preds
        except Exception as e:
            print(f"Card {card_nr} detection failed:", e)
            return []
        
    def detect_health(self, player_number):
        default_health = 10
        default_player_number = 1  # default player if player_number not between 1 and 4
        if 1 <= player_number <= 4:
            file_path = f"screenshots/health_p{player_number}.png"
        else:
            file_path = f"screenshots/health_p{default_player_number}.png"

        if self.os_type == "Darwin":
            scale_factor = 8
        elif self.os_type == "Windows":
            scale_factor = 5

        try:

            img = Image.open(file_path)
            img = ImageOps.invert(img.convert('RGB'))
            img = img.resize((img.width * scale_factor, img.height * scale_factor))
            img_np = np.array(img)
            results = self.reader.readtext(img_np)

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
        
    def detect_elixir(self):
    
        try:
                file_path = f"screenshots/elixir.png"

                # Take region screenshot (high precision, retina-safe)
                screenshot = Image.open(file_path)
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

        except Exception as e:
            print(f"[ERROR] Elixir detection failed: {e}")
            return getattr(self, "last_elixir", 0)
        
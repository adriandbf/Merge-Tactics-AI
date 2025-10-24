from inference_sdk import InferenceHTTPClient
import os
import easyocr
import platform
from PIL import Image, ImageOps
import numpy as np


client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    # insert your api key here
    api_key="*************"
)

class Detection:

    def __init__(self):
        self.os_type = platform.system()
        self.reader = easyocr.Reader(['en'], gpu=False)

    def detect_troops(self):
        try:
            image_path = f"screenshots/area.png"
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
        
    def detect_health(self, file_path, default_health):
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
from inference_sdk import InferenceHTTPClient
# TO DO: Insert new model 

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="UJ8Z7Y81V4psRKlzyU7d"
)

class Detection:

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
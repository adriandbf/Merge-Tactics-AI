from inference_sdk import InferenceHTTPClient

# TO DO: Insert new model 

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=""
)

class Detection:

    def detect_troops(self):
        result2 = client.run_workflow(
            workspace_name="vera-8vhle",
            workflow_id="troopdetection",
            images={
                "image": "area.png"
            },
            use_cache=True # cache workflow definition for 15 minutes
        )
        preds2 = result2[0]["predictions"]["predictions"]
        return preds2

    def detect_card(self, card_nr):
        image_path = f"screenshots/card_{card_nr+1}.png"
        result1 = client.run_workflow(
            workspace_name="vera-8vhle",
            workflow_id="carddetection-2",
            images={
                "image": image_path
            },
            use_cache=True # cache workflow definition for 15 minutes
        )
        preds1 = result1[0]["predictions"]["predictions"]
        return preds1
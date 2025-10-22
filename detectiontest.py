from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="Ql9J5N8ZaQruGzkj3KF4"
)


# doesnt work with multiple card images in one png, have to split cards into 3 seperate pngs
image_path = f"screenshots/card_1.png"
result1 = client.run_workflow(
    workspace_name="adriandbf",
    workflow_id="carddetection",
    images={
        "image": image_path
    },
    use_cache=True # cache workflow definition for 15 minutes
)

image_path = f"screenshots/area.png"
result2 = client.run_workflow(
    workspace_name="adriandbf",
    workflow_id="troopdetection",
    images={
        "image": image_path
    },
    use_cache=True # cache workflow definition for 15 minutes
)

preds1 = result1[0]["predictions"]["predictions"]
preds2 = result2[0]["predictions"]["predictions"]

for p in preds1:
    print(p['class'])

for p in preds2:
    print(p['class'])

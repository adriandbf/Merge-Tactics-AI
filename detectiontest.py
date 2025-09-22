from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=""
)

result1 = client.run_workflow(
    workspace_name="adriandbf",
    workflow_id="carddetection",
    images={
        "image": "card_area.png"
    },
    use_cache=True # cache workflow definition for 15 minutes
)

# print(result)

result2 = client.run_workflow(
    workspace_name="adriandbf",
    workflow_id="troopdetection",
    images={
        "image": "area.png"
    },
    use_cache=True # cache workflow definition for 15 minutes
)

preds1 = result1[0]["predictions"]["predictions"]
preds2 = result2[0]["predictions"]["predictions"]

for p in preds1:
    print(p['class'])

for p in preds2:
    print(p['class'])
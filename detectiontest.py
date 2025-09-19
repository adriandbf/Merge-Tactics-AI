from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="YOUR API KEY"
)

result = client.run_workflow(
    workspace_name="adriandbf",
    workflow_id="carddetection",
    images={
        "image": "knight.png"
    },
    use_cache=True # cache workflow definition for 15 minutes
)

# print(result)

result2 = client.run_workflow(
    workspace_name="adriandbf",
    workflow_id="troopdetection",
    images={
        "image": "troopstest.png"
    },
    use_cache=True # cache workflow definition for 15 minutes
)

preds = result2[0]["predictions"]["predictions"]

for p in preds:
    print(p['class'])
from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="YOUR_API_KEY"
)

result = client.run_workflow(
    workspace_name="adriandbf",
    workflow_id="custom-workflow",
    images={
        "image": "knight.png"
    },
    use_cache=True # cache workflow definition for 15 minutes
)

print(result)

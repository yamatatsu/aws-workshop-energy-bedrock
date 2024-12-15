import base64
import boto3
import json
from PIL import Image
from random import randint
import io


def generate_image(img_path, prompt):
    bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Load the input image from disk.
    # IMPORTANT: The image width and height must both be 1024 pixels or less.
    with open(img_path, "rb") as image_file:
        input_image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    # Configure the inference parameters.
    inference_params = {
        "taskType": "INPAINTING",
        "inPaintingParams": {
            "text": prompt,
            "negativeText": "bad quality, low res",
            "image": input_image_base64,
            "maskPrompt": "body of pipeline",
        },
        "imageGenerationConfig": {
            "numberOfImages": 3,  # Number of variations to generate
            "quality": "standard",  # Allowed values are "standard" or "premium". NOTE: When I set this to "premium", streamlit API get timeout error.
            "height": 1024,
            "width": 1024,
            "cfgScale": 8.0,
            "seed": randint(0, 100000),  # Use a random seed
        },
    }

    # Invoke the model.
    response = bedrock_runtime.invoke_model(
        modelId="amazon.nova-canvas-v1:0", body=json.dumps(inference_params)
    )

    # Convert the JSON string to a dictionary.
    response_body = json.loads(response["body"].read())

    # Loop through the generated images and save each to disk.
    images = response_body["images"]
    for i in range(len(images)):
        image_data = images[i]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        output_file_name = f"output-{i + 1}.png"
        image.save(output_file_name)

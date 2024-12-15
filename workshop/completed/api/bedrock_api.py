import json
import boto3


# Rewritten for using with nova by yamatatsu.


session = boto3.Session(region_name="us-east-1")

bedrock = session.client(service_name="bedrock-runtime")

bedrock_model_id = "amazon.nova-lite-v1:0"  # set the foundation model

system_list = [{"text": "What is the largest city in New Hampshire?"}]
message_list = [{"role": "user", "content": [{"text": "Researching cities about US"}]}]
inf_params = {"max_new_tokens": 500, "top_p": 0.9, "top_k": 20, "temperature": 0.7}

body = json.dumps(
    {
        # "prompt": anthropic.HUMAN_PROMPT+prompt+anthropic.AI_PROMPT,
        # "max_tokens_to_sample": 1024
        "schemaVersion": "messages-v1",
        "messages": message_list,
        "system": system_list,
        "inferenceConfig": inf_params,
    }
)  # build the request payload

#
response = bedrock.invoke_model(
    body=body,
    modelId=bedrock_model_id,
    accept="application/json",
    contentType="application/json",
)  # send the payload to Bedrock

#
response_body = json.loads(response.get("body").read())  # read the response

print(response_body)

res = {
    "output": {
        "message": {
            "content": [
                {
                    "text": "The largest city in New Hampshire is Manchester. It is the most populous city in the state and serves as a significant economic and cultural hub. Manchester is located in Hillsborough County and is situated along the Merrimack River. \n\nOther notable cities in New Hampshire include Concord (the state capital), Nashua, and Portsmouth. Each of these cities has its own unique character and attractions, but Manchester stands out as the largest by population."
                }
            ],
            "role": "assistant",
        }
    },
    "stopReason": "end_turn",
    "usage": {
        "inputTokens": 14,
        "outputTokens": 82,
        "totalTokens": 96,
        "cacheReadInputTokenCount": None,
        "cacheWriteInputTokenCount": None,
    },
}

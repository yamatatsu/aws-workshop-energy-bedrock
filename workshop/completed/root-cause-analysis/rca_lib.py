import boto3
import anthropic
from typing import Dict

session = boto3.Session()
bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client


claude_system_prompt = [{"text": '''You are Claude, an AI assistant created by Anthropic to be helpful,
                harmless, and honest. Your goal is to provide informative and substantive responses
                to queries while avoiding potential harms.'''}]

models: Dict[str, callable] = {
    "bedrock titan": ["amazon.titan-text-express-v1", []],
    "bedrock claude 3.5 sonnet v2": ["anthropic.claude-3-5-sonnet-20241022-v2:0", claude_system_prompt],
    "bedrock claude 3 sonnet": ["anthropic.claude-3-sonnet-20240229-v1:0", claude_system_prompt],
    "bedrock llama 3.1": ["meta.llama3-1-8b-instruct-v1:0", []],
    "bedrock mistral large 2": ["mistral.mistral-large-2407-v1:0", []]
}

char_limits: Dict[str, int] = {
    "bedrock titan": 100000,
    "bedrock claude 3.5 sonnet v2": 200000,
    "bedrock claude 3 sonnet": 200000,
    "bedrock llama 3.1": 8000,
    "bedrock mistral large 2": 32000
}

def converse_model(model_id, messages, system_prompts=[], inference_config={}, additional_model_fields={}):
    response = bedrock.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields
    )
    return response['output']['message']

def call_bedrock(model, messages):
    model_id = models[model][0]
    system_prompts = models[model][1]
    return converse_model(model_id, messages, system_prompts)

def get_answers(summary, query, model):
    if query == "cancel":
        response = [{"content": [{"text": 'It was swell chatting with you. Goodbye for now'}]}]
    else:
        message = {"role": "user", "content": [{"text": summary}, {"text": query}]}
        messages = [message]
    
    response = call_bedrock(model, messages)
    return response["content"][0]["text"]

def upload_file_get_summary(file_name, model):
    with open(file_name, "rb") as doc_file:
        doc_bytes = doc_file.read()

    user_prompt = "Describe the motor specifications based on the provided document"
    message = {"role": "user", "content": [{"text": user_prompt}]}

    message["content"].append(
                    {
                        "document": {
                            "format": "pdf",
                            "name": "Document 1",
                            "source": {
                                "bytes": doc_bytes
                            }
                        },
                    }
                )
    messages = [message]
    summary = call_bedrock(model, messages)
    return doc_bytes, summary["content"][0]["text"]
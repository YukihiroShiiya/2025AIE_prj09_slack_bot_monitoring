# src/bedrock_client.py

import boto3
import json
from guideline_loader import build_prompt
from botocore.exceptions import ClientError

def call_bedrock_violation_score(post_text: str) -> str:
    """
    Amazon Nova Lite (amazon.nova-lite-v1:0) モデル向け
    ガイドライン遵守スコアを取得
    """
    prompt = build_prompt(post_text)
    #print(prompt)
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    conversation = [
        {
            "role": "user",
            "content": [{"text": prompt}]
        }
    ]

    try:
        response = client.converse(
            modelId="amazon.nova-lite-v1:0",
            messages=conversation,
            inferenceConfig={
                "maxTokens": 512,
                "temperature": 0.2,
                "topP": 0.9
            },
        )

        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke model. Reason: {e}")
        return ""

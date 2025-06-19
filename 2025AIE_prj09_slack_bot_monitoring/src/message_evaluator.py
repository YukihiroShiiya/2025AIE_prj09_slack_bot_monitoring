# src/message_evaluator.py

import re
from bedrock_client import call_bedrock_violation_score

def evaluate_message(item: dict) -> dict:
    """
    DynamoDBの1件のSlack投稿に対して評価し、整形したスコアデータを返す
    """
    text = item.get('text', '')
    if not text:
        return None

    response_text = call_bedrock_violation_score(text)

    # スコア抽出
    match = re.search(r"違反点数\s*[:：]\s*(\d+),\s*賞賛点数\s*[:：]\s*(\d+)", response_text)
    if not match:
        return None

    violation_score = int(match.group(1))
    praise_score = int(match.group(2))

    return {
        "user_id": item["user_id"],
        "user_name": item.get("user_name", ""),
        "timestamp": item["timestamp"],
        "channel_id": item.get("channel_id", ""),
        "message_ts": item.get("message_ts", ""),
        "text": text,
        "violation_score": violation_score,
        "praise_score": praise_score
    }

from slack_client import get_channel_messages
from dynamodb_client import save_message_to_dynamodb

def fetch_and_save_messages(channel_id: str, oldest=None, latest=None, limit=200):
    """
    Slackの投稿を取得し、DynamoDBに保存する（任意で期間指定可能）
    """
    messages = get_channel_messages(
        channel_id=channel_id,
        oldest=oldest,
        latest=latest,
        limit=limit
    )

    print(f"✅ 取得件数: {len(messages)}")

    for msg in messages:
        save_message_to_dynamodb(msg)

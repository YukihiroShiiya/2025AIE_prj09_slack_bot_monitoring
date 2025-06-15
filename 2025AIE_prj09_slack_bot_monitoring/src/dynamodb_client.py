import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "slack_messages"  # ご自身のテーブル名に置き換えてください

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def save_message_to_dynamodb(item):
    """
    1件のSlackメッセージをDynamoDBに保存
    """
    try:
        table.put_item(Item=item)
        print(f"✅ 保存: {item['message_ts']}")
    except ClientError as e:
        print(f"❌ エラー: {e.response['Error']['Message']}")

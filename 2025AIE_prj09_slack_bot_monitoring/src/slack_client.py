from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import yaml
import os
from datetime import datetime

def load_config():
    """
    config/config.yaml を読み込んで辞書で返す
    """
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_channel_messages(channel_id, oldest=None, latest=None, limit=200):
    """
    指定チャンネルの投稿を取得（期間指定対応）
    :param channel_id: SlackのチャンネルID
    :param oldest: 開始時刻（Unixタイムスタンプの float 文字列または数値）
    :param latest: 終了時刻（Unixタイムスタンプの float 文字列または数値）
    :param limit: 最大取得件数（最大1000）
    :return: 整形済みメッセージリスト
    """
    config = load_config()
    client = WebClient(token=config["slack"]["bot_token"])

    try:
        # 引数で None の値は除外
        params = {
            "channel": channel_id,
            "limit": limit
        }
        if oldest:
            params["oldest"] = str(oldest)
        if latest:
            params["latest"] = str(latest)

        response = client.conversations_history(**params)

        messages = []
        for msg in response.get("messages", []):
            messages.append({
                "message_ts": msg.get("ts"),
                "user_id": msg.get("user", "BOT"),
                "channel_id": channel_id,
                "text": msg.get("text"),
                "timestamp": datetime.fromtimestamp(float(msg.get("ts"))).isoformat(),
                "reaction_count": len(msg.get("reactions", [])),
                "reactions": [r.get("name") for r in msg.get("reactions", [])] if "reactions" in msg else []
            })

        return messages

    except SlackApiError as e:
        print(f"Slack API エラー: {e.response['error']}")
        return []

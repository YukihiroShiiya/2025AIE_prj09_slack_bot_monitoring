# src/guideline_loader.py

import yaml
import os

def load_guidelines():
    """
    YAMLファイルからガイドラインリストを読み込む
    """
    path = os.path.join(os.path.dirname(__file__), "..", "config", "guidelines.yaml")
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("guidelines", [])

def load_prompt_template():
    """
    YAMLファイルからプロンプトテンプレートを読み込む
    """
    path = os.path.join(os.path.dirname(__file__), "..", "config", "prompt_template.yaml")
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("template", "")

def build_prompt(post_text: str) -> str:
    """
    YamlからガイドラインとFew-shot例を読み込み、プロンプトを生成
    """
    # config/prompt_template.yaml を読み込む
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "prompt_template.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    guidelines = config.get("guidelines", [])
    examples = config.get("examples", [])

    prompt = "あなたは社内ガイドライン遵守チェックの専門AIです。\n"
    prompt += "以下のガイドラインに照らして、投稿がどの程度『ガイドラインを守っているか』を評価してください。\n"
    prompt += "出力はスコアの半角数値 0～100 の範囲です。\n\n"

    prompt += "【ガイドライン】\n"
    for rule in guidelines:
        prompt += f"- {rule}\n"

    if examples:
        prompt += "\n【例】\n"
        for ex in examples:
            prompt += f"投稿: {ex['input']}\nスコア: {ex['output']}\n"

    prompt += f"\n【投稿内容】\n\"\"\"{post_text}\"\"\"\n"
    prompt += "\n【出力フォーマット】\n- スコア（0～100の数値）:"

    return prompt
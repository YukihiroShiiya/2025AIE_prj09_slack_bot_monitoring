import os
import yaml

def build_prompt(post_text: str) -> str:
    """
    prompt_template.yaml と guidelines.yaml を組み合わせて最終プロンプトを構築
    """
    # ファイルパス
    base_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(base_dir, "..", "config", "prompt_template.yaml")
    guideline_path = os.path.join(base_dir, "..", "config", "guidelines.yaml")

    # YAML読み込み
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_config = yaml.safe_load(f)

    with open(guideline_path, "r", encoding="utf-8") as f:
        guideline_config = yaml.safe_load(f)

    # 各要素取り出し
    template_text = prompt_config.get("template", "")

    guideline_list = guideline_config.get("guidelines", [])

    # 安全対策
    if not template_text:
        raise ValueError("テンプレート本文が読み込めませんでした（templateが空です）")

    # 🔧 ガイドラインを文字列に整形
    formatted_guidelines = ""
    for guideline in guideline_list:
        formatted_guidelines += f"- {guideline}\n"

    # 🔧 テンプレートにガイドラインと投稿内容を埋め込む
    prompt = template_text.replace("{guidelines}", formatted_guidelines.strip())
    prompt = prompt.replace("{text}", post_text)

    return prompt

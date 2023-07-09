import os
import openai

BAIDU_API_KEY = "iYbU5qD7NI7WQfZoxupGGtaG"
BAIDU_SECRET_KEY = "aYGMc1cuwfoLr58vFprRj7p4HX2bGtx7"

# 设置 openai 的 api key
os.environ["OPENAI_API_KEY"]="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"
openai.api_key = os.getenv("OPENAI_API_KEY")

project_dir="E:\DeskTop\ds2"
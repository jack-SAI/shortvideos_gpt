from GUI_videoGenProj.config import *

def generate_script(product_info):
    """
    Args:
        product_info: str, the information of the product.

    Returns:
        script: str, the script for the short video.
    """

    # 定义一个自定义的提示，用于生成文案
    setprompt1 = "我需要使用GPT为我写一条适合短视频的文案，我将会提供一部分关于短视频内容的属性信息。 " \
               "全程中文，大概我需要200字左右。 需要尽量使用短句，少用长句，少使用连词。 " \
               "风格尽量通俗有趣，接地气。可以适当幽默 #短视频内容属性信息：" + product_info + "\n\n文案："


    # 使用 openai 的 Completion 接口，根据提示生成文案
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个有创造力的视频文案作家，你的语言有吸引力有张力。"},
                {"role": "user", "content": setprompt1},
            ],
            temperature=0.5,
            presence_penalty=0.9,
        )
        script = response['choices'][0]['message']['content']
        return script
    except Exception as e:
        print("\genScripts:Failed to generate script: " + str(e))
        return None
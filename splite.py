from GUI_videoGenProj.config import *
import re

def split_script(script):
    """
    Args:
        script: str, the script for the short video.

    Returns:
        sentences: list of str, the list of independent sentences.
    """

    # 定义一个自定义的提示，用于拆分文案
    myprompt = "对我给出的资料，我需要你把它拆分成意义独立的句子块。即单独看这一段句子块，意义也是独立完整的。" \
               "可以作为一个部件拼到其他地方,每一个句子块不应太长，符合的情况下尽可能拆分。每两个句子块之间用$分割" \
               "（务必一定切记记得用$分割)。不要使用1.2.3.等序号，不用要换行分割，不要加任何多余的" \
               "分隔符\n我给出的资料：" + script + "\n\n句子："

    # 使用 openai 的 Completion 接口，根据提示拆分文案
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[
                {"role": "system", "content": "你是一位十分严谨的对语言敏感的文字工作者.（务必一定切记记得按要求用$分割)"},
                {"role": "user", "content": myprompt},
            ],
            temperature=0.1,
            max_tokens=1500,
            n=1,
        )
        print("GPT拆分的结果：")
        print(response['choices'][0]['message']['content'])
        blocks = response['choices'][0]['message']['content'].split("$")

        blocks = list(filter(lambda x: x.strip() != "", blocks))
        print('没有处理过特殊字符的blocks：'+str(blocks))

        # 去掉 \n 这个要单独去掉
        blocks = [block.replace('\n', '') for block in blocks]

        #去掉不合法的\n
        def remove_special_chars(s):
            # 定义一个包含特殊字符的字符串
            special_chars = "\\/:*?\"<>|"
            # 使用 re.sub() 方法替换掉特殊字符为空字符串
            return re.sub(f"[{special_chars}]", "", s)
        blocks = [remove_special_chars(s) for s in blocks]
        print('处理之后特殊字符后：(不包括\\n)' + str(blocks))


        # 打印结果
        print('处理之后特殊字符后：'+str(blocks))

        # #去掉空字符串
        # blocks = list(filter(lambda x: x.strip() != "", blocks))
        #去掉太长的句子
        # blocks = [block for block in blocks if len(block) <= 45]

        return blocks
    except Exception as e:
        print("Failed to split script: " + str(e))
        return None

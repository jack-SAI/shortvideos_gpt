import logging
import os.path
import time

from moviepy.editor import *
from moviepy.video.tools.credits import credits1
from moviepy.editor import CompositeVideoClip, AudioFileClip

from GUI_videoGenProj.config import *



def composevideo_1_concate(scriptslist,project_folder):
    res_cliplist = pre_process(scriptslist,project_folder)
    output_files_list = []

    clips = [VideoFileClip(v) for v in res_cliplist]
    final_clip = concatenate_videoclips(clips)

    output_path = os.path.join(project_folder, "works", time.strftime("%Y%m%d_%H%M%S") + ".mp4")
    final_clip.write_videofile(output_path)
    # 将视频文件的地址添加到列表中
    output_files_list.append(output_path)
    # 返回列表作为结果
    return output_files_list

def pre_process(scriptlist,project_folder):
    durations = []
    print(scriptlist)
    for file in scriptlist:
        clip = VideoFileClip(file)
        durations.append(clip.duration)
    clips = [VideoFileClip(v) for v in scriptlist]
    # 定义一个空列表，用于存储生成的视频文件的地址
    output_files_list = []
    # 读取背景图片，并转换成无声的视频片段
    bg_image = os.path.join(project_folder, "config", "background.jpg")
    bg_clip = ImageClip(bg_image)
    # 获取背景尺寸
    bg_size = bg_clip.size
    # 遍历视频片段列表中的每个元素
    res_cliplist = []
    res_output_files_list = []
    for i, clip in enumerate(clips):
        # 对每个视频片段进行等比例缩放，并适应背景尺寸
        clip = clip.resize(bg_size)
        # 创建合成视频片段对象，并指定尺寸
        res_clip = CompositeVideoClip([bg_clip, clip], size=bg_size)
        # 设置视频片段的位置为居中
        res_clip = res_clip.set_pos("center")
        # 将合成视频片段对象写入到一个视频文件中
        res_cliplist.append(res_clip)
        res_clip_output_path = os.path.join(project_folder, "middle",
                                            time.strftime("%Y%m%d_%H%M%S") + "_" + str(i) + ".mp4")
        res_clip.write_videofile(
            res_clip_output_path,
            fps=30,
            codec='mpeg4',
            preset='ultrafast',
            audio_codec="libmp3lame",
            threads=4)
        res_output_files_list.append(res_clip_output_path)
    return res_output_files_list

if __name__=="__main__":
    output=composevideo_1_concate(['E:\\DeskTop\\ds2\\videoclips\\AIGC介绍4\\现如今，它已成为PGC、UGC之后新型内容生产方式的代表形式，.mp4','E:\\DeskTop\\ds2\\videoclips\\AIGC介绍4\\那很可能就是 AIGC——通过人工智能技术生成的内容。.mp4'],
                           "E:\\DeskTop\\ds2")
    print(output)
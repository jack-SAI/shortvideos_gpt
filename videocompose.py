import logging
import os.path
import time

from moviepy.editor import *
from moviepy.video.tools.credits import credits1
from moviepy.editor import CompositeVideoClip, AudioFileClip

from GUI_videoGenProj.config import *


m=4


def composevideo_2_compose_TAI(script, audiof, imgf,subroot):
    # 加载一个图片clip
    clip = ImageClip(imgf)
    audio = AudioFileClip(audiof)
    final = clip
    final_video = final.set_audio(audio)
    final_video = CompositeVideoClip([final_video])

    video_path = os.path.join(subroot,
                              f"{script}")  # 修改图片文件的路径，增加 index 参数

    if not os.path.exists(subroot):
        os.mkdir(subroot)
    if not os.path.exists(video_path):
        final_video.write_videofile(
            video_path+'.mp4',
            fps=30,
            codec='mpeg4',
            preset='ultrafast',
            audio_codec="libmp3lame",
            threads=4
        )
        return video_path+'.mp4'


def composevideo_2_compose_TAI_listver(scriptlist, audioflist, imgflist,project_folder,name):
    # 定义一个空列表，用于存储生成的音频文件的地址
    save_files_list = []
    # 遍历文本列表中的每个元素
    subroot = os.path.join(project_folder, 'videoclips',f'{name}')
    if not os.path.exists(subroot):
        os.mkdir(subroot)
    for i in range(len(scriptlist)):
        save_file = composevideo_2_compose_TAI(scriptlist[i], audioflist[i], imgflist[i],subroot)
        save_files_list.append(save_file)
    # 返回生成的视频片段的所在目录为结果，因为这里已经搞一段落了
    # return os.path.join(project_folder,'videoclips')
    return save_files_list

if __name__=="__main__":
    addressv=composevideo_2_compose_TAI_listver(['你是否有过眼前一亮的视频内容，让你不得不赞叹“这内容也太冷静了吧！”？','那很可能就是 AIGC——通过人工智能技术生成的内容。'],
                                       ['E:\\DeskTop\\ds2\\audios\\你是否有过眼前一亮的视频内容，让你不得不赞叹“这内容也太冷静了吧！”？.mp3','E:\\DeskTop\\ds2\\audios\\那很可能就是 AIGC——通过人工智能技术生成的内容。.mp3'],
                                       ['E:\\DeskTop\\ds2\\imgcrawl\\视频内容、冷静、赞叹\\20230628_000334.jpg','E:\\DeskTop\\ds2\\imgcrawl\\视频内容、冷静、赞叹\\20230628_000334.jpg'],
                                       "E:\\DeskTop\\ds2",'两个片段实验')

    print(addressv)
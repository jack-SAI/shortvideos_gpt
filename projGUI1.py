# 导入 tkinter 库
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename

import tkinter.filedialog as filedialog
# import json
import csv
import tkinter.messagebox
import os
from tkinter import simpledialog
from tkinter import font
from tkinter import messagebox




from GUI_videoGenProj.genscripts import *
from GUI_videoGenProj.splite import *
from GUI_videoGenProj.text2audio import *
from GUI_videoGenProj.keywordAbs import *
from GUI_videoGenProj.picAcquire import *
from  GUI_videoGenProj.videocompose import *
from GUI_videoGenProj.videoconcate import *
from GUI_videoGenProj.config import *




# 定义全局变量
project_dir = "" # 项目文件夹地址



# 定义函数

def isTooLong(str,lenth):
    if len(str)>lenth:
        return 1
    else:
        return 0

def select_project_dir():
    # 选择项目文件夹地址
    global project_dir
    project_dir = askdirectory()
    project_dir = os.path.abspath(project_dir)
    print("项目文件夹地址:", project_dir)

def init_project_dir():
    # 初始化项目文件夹，即在项目文件夹下创建那些文件夹
    global project_dir
    if project_dir == "":
        messagebox.showwarning("警告","未选择项目文件夹地址！")
        return
    else:
        import os
        sub_dirs = ["scripts", "scriptlist", "audios", "imgcrawl", "imggen", "videoclips", "config", "middle", "works"]
        for sub_dir in sub_dirs:
            os.makedirs(os.path.join(project_dir, sub_dir), exist_ok=True)
        print("初始化项目文件夹成功")

def tvsmtable_save():
    # 导出 tree 的内容，保存 tvsmtable 的内容，保存在 scriptlist 文件夹中，保存为 csv 格式，需要用户对文件进行手动命名
    global project_dir
    if project_dir == "":
        messagebox.showwarning("警告","未选择项目文件夹地址！")
        return
    else:
        import csv
        filename = filedialog.asksaveasfilename(title='保存文件', filetypes=[('csv文件', '*.csv')], defaultextension='.csv')  # 弹出对话框，让用户输入文件名
        if filename:  # 如果文件名不为空
            try:
                with open(filename, 'w', newline='') as f:  # 打开文件
                    writer = csv.writer(f)  # 创建 csv 写入器
                    writer.writerow(COLUMNS)  # 写入表头
                    for item in treeview.get_children(''):  # 遍历表格内容
                        writer.writerow(treeview.item(item, 'values'))  # 写入每一行数据
                print("导出 table 的内容成功")
            except Exception as e:  # 捕获异常
                print("导出 table 的内容失败：", e)  # 弹出错误信息

def tvsmtable_load():
    # 导入信息进 tvsmtable，选择文件，将文件信息导入进 tvsmtable
    global project_dir
    if project_dir == "":
        messagebox.showwarning("警告","未选择项目文件夹地址！")
        return
    else:
        filepath = askopenfilename(initialdir=os.path.join(project_dir, "scriptlist"), filetypes=[("CSV files", "*.csv")])
        if filepath:
            import csv
            with open(filepath, "r") as f:
                reader = csv.reader(f)  # 创建 csv 读取器
                next(reader)  # 跳过表头
                for i, row in enumerate(reader):  # 遍历每一行数据
                    if len(row) == len(COLUMNS):  # 如果数据列数和表头列数相同
                        treeview.insert('', i, values=row)  # 插入数据到表格中
            print("导入信息进 tvsmtable 成功")
        else:
            return

def clear():
    # 清空表格内容
    for item in treeview.get_children(''):  # 遍历表格内容
        treeview.delete(item)  # 删除每一行数据
    print("清空表格成功")

def import_data():
    # 导入表格内容，选择文件，将文件信息以追加的方式填入表格
    global project_dir
    if project_dir == "":
        messagebox.showwarning("警告","未选择项目文件夹地址！")
        return
    else:
        filepath = askopenfilename(initialdir=os.path.join(project_dir, "scriptlist"), filetypes=[("CSV files", "*.csv")])
        if filepath:
            import csv
            with open(filepath, "r") as f:
                reader = csv.reader(f)  # 创建 csv 读取器
                next(reader)  # 跳过表头
                for row in reader:  # 遍历每一行数据
                    if len(row) == len(COLUMNS):  # 如果数据列数和表头列数相同
                        treeview.insert('', 'end', values=row)  # 追加数据到表格中
            print("追加导入表格内容成功")



def set_cell_value(event):
    for item in treeview.selection():
        # item = I001
        item_text = treeview.item(item, "values")
        # print(item_text[0:2])  # 输出所选行的值
    column = treeview.identify_column(event.x)  # 列
    row = treeview.identify_row(event.y)  # 行
    cn = int(str(column).replace('#', ''))
    rn = int(str(row).replace('I', ''))
    print(column)
    print(row)
    print(cn)
    print(rn)
    entryedit = Text(root, width=10 + (cn - 1) * 16, height=1)
    entryedit.place(x=19 + (cn - 1) * 130, y=54 + rn * 20)

    def saveedit():
        editvalue=entryedit.get(0.0, "end").replace("\n", "")
        if isTooLong(editvalue,20)==1 :
            messagebox.showwarning("警告","修改内容过长或为空")
        treeview.set(item, column=column, value=editvalue)
        entryedit.destroy()
        okb.destroy()
        uokb.destroy()

    def unsaveedit():
        entryedit.destroy()
        okb.destroy()
        uokb.destroy()
        treeview.set(item, column=column, value=old_value)  # 还原原来的值

    old_value = treeview.set(item, column=column)  # 获取双击之前的值

    okb = ttk.Button(root, text='OK', width=6, command=saveedit)
    okb.place(x=90 + (cn - 1) * 242, y=54 + rn * 20)

    uokb = ttk.Button(root, text='cancel', width=6, command=unsaveedit)
    uokb.place(x=180 + (cn - 1) * 242, y=54 + rn * 20)


def import_scripts():
    global project_dir
    if project_dir == "":
        messagebox.showwarning("警告","未选择项目文件夹地址！")
        return
    filepath = askopenfilename(initialdir=os.path.join(project_dir, "scripts"))
    if filepath:
        # 读取文件内容
        with open(filepath, "r") as f:
            script = f.read()
        text_box.insert(1.0,script)


def genscripts():
    # 调用 GPT 生成文案功能，生成的文案保存在“srcipts”文件夹下，命名细节在后文对应的模块中叙述。同时将生成的文案展示在下面的文案显示框中。
    global project_dir
    if project_dir == "":
        messagebox.showwarning("警告","未选择项目文件夹地址！")
        return
    else:
        # 获取用户输入的短视频内容属性信息
        product_info = simpledialog.askstring("输入", "请输入短视频内容属性信息：")
        # 调用 generate_script 函数，根据短视频内容属性信息生成文案
        script = generate_script(product_info)
        print(script)
        if script:
            # 保存文件，自动命名为输入的短视频内容属性信息的前四个字+时间（time.strftime("%Y%m%d_%H%M%S")）
            import time
            filename = time.strftime("%Y%m%d_%H%M%S") + ".txt"#product_info[:4] +
            filepath = os.path.join(project_dir, "scripts", filename)
            with open(filepath, "w",errors='ignore') as f:
                f.write(script)
            # 展示再文案显示框
            text_box.delete(1.0, END) # 清空文本框
            text_box.insert(1.0, script) # 插入文案
            # messagebox.showinfo("提示", "生成文本成功")
        else:
            messagebox.showinfo("提示", "生成文本失败")


def sciptssplite():
    # 调用文案拆分功能，选择一个文案文件进行文案拆分，拆分的文案填充 tvsmtable 的 a 列“文案片段”
    global project_dir
    if project_dir == "":
        messagebox.showwarning("警告","未选择项目文件夹地址！")
        return
    else:
        # 选择一个文案文件
        filepath = askopenfilename(initialdir=os.path.join(project_dir, "scripts"))
        if filepath:
            # 读取文件内容
            with open(filepath, "r") as f:
                script = f.read()
            # 调用 split_script 函数，根据文案拆分成句子块
            sentences = split_script(script)
            if sentences:
                # 填充 tvsmtable 的 a 列，同时给其他列赋值为空字符串
                for i in range(len(sentences)):
                    treeview.insert('', i, values=(sentences[i], "", "", "", "", ""))
                print("文案拆分成功")
            else:
                messagebox.showinfo("提示", "文案拆分失败")


def text2audio():
    # 调用音频生成模块，对应 tvsmtable 中 a 列文案片段，产生的音频片段，填充 tvsmtable 的 d 列“对应的音频文件地址”
    global project_dir
    if project_dir == "":
        messagebox.showwarning("警告","未选择项目文件夹地址！")
        return
    else:
        # 获取 tvsmtable 中 a 列文案片段的内容
        texlist = []
        for item in treeview.get_children(''):  # 遍历表格内容
            texlist.append(treeview.item(item, 'values')[0])  # 获取每一行的第一列数据
        # 调用 textlist2audio 函数，根据文本列表生成音频文件列表
        save_files_list = textlist2audio(project_dir,texlist)
        if save_files_list:
            # 填充 tvsmtable 的 d 列
            for i in range(len(save_files_list)):
                treeview.set(treeview.get_children('')[i], column=3, value=save_files_list[i])  # 设置每一行的第四列数据
            print("音频生成成功")
        else:
            messagebox.showinfo("提示", "音频合成失败")


def text2keywords():
    # 调用关键词提取功能，对应 tvsmtable 中 a 列文案片段，产生的关键词 list 填充 tvsmtable 的 c 列“对应的关键词”
    global project_dir
    if project_dir == "":
        messagebox.showwarning("警告","未选择项目文件夹地址！")
        return
    else:
        # 获取 tvsmtable 中 a 列文案片段的内容
        blocklist = []
        for item in treeview.get_children(''):  # 遍历表格内容
            blocklist.append(treeview.item(item, 'values')[0])  # 获取每一行的第一列数据
        # 调用 keywab_fromscripts_listver 函数，根据文本列表生成关键词列表
        keywords_list = keywab_fromscripts_listver(blocklist)
        if keywords_list:
            # 填充 tvsmtable 的 c 列
            for i in range(len(keywords_list)):
                treeview.set(treeview.get_children('')[i], column=2, value=keywords_list[i])  # 设置每一行的第三列数据
            print("关键词提取成功")
        else:
            messagebox.showinfo("提示", "关键词提取失败")




def text2img():
    # 调用图片获取模块，对应 tvsmtable 中 b 列“补充要求”和 c 列“对应的关键词”进行图片的爬取或 dalle 模型生成。产生的图片文件的地址填充 tvsmtable 的 e 列
    global project_dir
    if project_dir == "":
        messagebox.showwarning("警告","未选择项目文件夹地址！")
        return
    else:
        # 弹出一个对话框，要求输入默认下载的图片的数量 downloadnum
        downloadnum = simpledialog.askinteger("输入", "请输入默认下载的图片的数量（1-5）：", minvalue=1, maxvalue=5)
        if downloadnum:  # 如果输入不为空
            # 获取 tvsmtable 中 b 列“补充要求”和 c 列“对应的关键词”的内容
            n = []  # 定义一个空列表 n，用于存储补充要求
            keywords = []  # 定义一个空列表 keywords，用于存储关键词
            for item in treeview.get_children(''):  # 遍历表格内容
                n.append(treeview.item(item, 'values')[1])  # 获取每一行的第二列数据，添加到 n 列表中
                keywords.append(treeview.item(item, 'values')[2])  # 获取每一行的第三列数据，添加到 keywords 列表中
            # 对 n 列表进行处理，如果输入是['*1', '*2', '*3', '*4', '*5']这几个之一，那么不管他，如果不是的话，就把对应的 n[i] 替换成 downloadnum
            for i in range(len(n)):  # 遍历 n 列表中的每个元素
                print(n)
                n[i]=n[i].replace('\n','')
                if n[i] in ['*1', '*2', '*3', '*4', '*5']:  # 如果元素不属于 ['*1', '*2', '*3', '*4', '*5'] 列表
                    n[i]=n[i]
                else:
                    n[i] = str(downloadnum)  # 就把元素替换成 downloadnum 的字符串形式
            # 调用 get_pics 函数，根据关键词和补充要求生成图片文件列表
            print(n)
            pics = get_pics(keywords, n, project_dir)
            print(pics)
            if pics:
                # 填充 tvsmtable 的 e 列
                for i in range(len(pics)):
                    treeview.set(treeview.get_children('')[i], column=4, value=pics[i])  # 设置每一行的第五列数据
                print("图片获取成功")
            else:
                messagebox.showinfo("提示", "图片获取失败")


def videocompose():
    # 调用视频合成功能。对应 tvsmtable 中 a 列，d 列，e 列合成视频片段，根据其对应的文件的地址，合成视频片段，产生的视频文件的地址填充 tvsmtable 的 f 列
    global project_dir
    if project_dir == "":
        messagebox.showwarning("警告","未选择项目文件夹地址！")
        return
    else:
        # 弹出一个对话框，要求输入视频片段的名称 name
        name = simpledialog.askstring("输入", "请输入视频片段的名称：")
        if name:  # 如果输入不为空
            # 获取 tvsmtable 中 a 列，d 列，e 列的内容
            scriptlist = []
            audioflist = []
            imgflist = []
            for item in treeview.get_children(''):  # 遍历表格内容
                scriptlist.append(treeview.item(item, 'values')[0])
                audioflist.append(treeview.item(item, 'values')[3])
                imgflist.append(treeview.item(item, 'values')[4])
            save_files_list = composevideo_2_compose_TAI_listver(scriptlist, audioflist, imgflist, project_dir, name)
            if save_files_list:
                for i in range(len(save_files_list)):
                    treeview.set(treeview.get_children('')[i], column=5, value=save_files_list[i])
                print("视频合成成功")
            else:
                messagebox.showinfo("提示", "视频合成失败")

def videoconcate():
    # 调用视频拼接模块，对应 tvsmtable 中 f 列，将那些视频片段对应拼接起来，组成一个长视频。文件保存在“works”下
    global project_dir
    if project_dir == "":
        messagebox.showwarning("警告","未选择项目文件夹地址！")
        return
    else:
        # 获取 tvsmtable 中 f 列的内容
        scriptslist = []  # 定义一个空列表 scriptslist，用于存储视频片段
        for item in treeview.get_children(''):  # 遍历表格内容
            scriptslist.append(treeview.item(item, 'values')[5])  # 获取每一行的第六列数据，添加到 scriptslist 列表中
        # 调用 composevideo_1_concate 函数，根据视频片段和项目文件夹地址生成长视频文件列表
        output_files_list = composevideo_1_concate(scriptslist, project_dir)
        if output_files_list:
            print("视频拼接成功")
            print("长视频文件的地址是：", output_files_list[0])  # 打印长视频文件的地址
        else:
            messagebox.showinfo("提示", "视频拼接失败")






# 创建窗体对象
root = Tk()
# 设置窗体标题
root.title("基于 GPT 的短视频生成系统")
# 设置窗体大小和位置
root.geometry("1500x600+10+100")




# root.option_add('*Font', 'Fira 50')
default_font = font.nametofont("TkDefaultFont")
default_font.configure(family="SimSun", size=20)


# 创建选择项目文件夹地址按键
select_dir_btn = ttk.Button(root, text="选择项目文件夹地址", command=select_project_dir)
# 设置按键位置和大小
select_dir_btn.place(x=10, y=10, width=200, height=40)

# 创建初始化项目文件夹按键
init_dir_btn = ttk.Button(root, text="初始化项目文件夹", command=init_project_dir)
# 设置按键位置和大小。
init_dir_btn.place(x=220, y=10, width=200, height=40)

# 定义常量
COLUMNS = ("文案片段", "补充要求", "对应的关键词", "对应的音频文件地址", "对应的图片文件地址", "产生的对应的视频片段的文件地址")
WIDTHS = (200, 100, 100, 200, 200, 200)

header_font = font.Font(size=20)
# 创建一个用 tree 实现的表格，我们叫它 tvsmtable 吧（treeview scripts elements table），6列内容，分别是 a 文案片段 b 补充要求 c 对应的关键词 d 对应的音频文件地址 e 对应的图片文件地址 f 产生的对应的视频片段的文件地址。都是可单独再编辑的。其中，当然，用户可以编辑 b 列补充要求来进行一些预定的细化操作。
treeview = ttk.Treeview(root, show="headings", columns=COLUMNS) # 创建表格对象
treeview.bind('<Double-1>', set_cell_value)
# 创建自定义字体

# 设置表头样式
# treeview.heading("文案片段", text="文案片段", anchor="center", font=("Arial", 12)) # 更改字体大小为12


# 设置表格每列的宽度和对齐方式
for i in range(len(COLUMNS)):
    treeview.column(COLUMNS[i], width=WIDTHS[i], anchor='center')
# 设置表格每列的标题
for col in COLUMNS:
    treeview.heading(col, text=col)

# 修改表头文本的标签样式
style = ttk.Style()
style.configure("Treeview.Heading", font=("SimSun", 16))
style2 = ttk.Style()
style2.configure("Treeview", font=("SimSun", 13))

# 设置表格位置和大小
treeview.place(x=10, y=50, width=1460, height=300)

# 创建导出 tree 的内容按键，任何时候都可以点击，保存 tvsmtable 的内容，保存在 scriptlist 文件夹中，保存为 json 格式，需要用户对文件进行手动命名。调用函数名 tvsmtable_save()
export_btn = ttk.Button(root, text="导出table内容", command=tvsmtable_save)
# 设置按键位置和大小
export_btn.place(x=10, y=360, width=200, height=40)

# 创建导入信息进 tvsmtable 按键。选择文件，将文件信息导入进 tvsmtable。调用函数名 tvsmtable_load()
import_btn = ttk.Button(root, text="导入信息进table", command=tvsmtable_load)
# 设置按键位置和大小
import_btn.place(x=220, y=360, width=200, height=40)

# 创建生成文本按键，调用 GPT 生成文案功能，生成的文案保存在“srcipts”文件夹下，命名细节在后文对应的模块中叙述。同时将生成的文案展示在下面的文案显示框中。调用函数名 genscripts()
gen_text_btn = ttk.Button(root, text="生成文本", command=genscripts)
# 设置按键位置和大小
gen_text_btn.place(x=430, y=360, width=200, height=40)

# 创建文案显示的一个文本框
text_box = Text(root)
# 设置文本框位置和大小
text_box.place(x=10, y=400, width=1460, height=100)

# 创建导入文案按键。选择一个文案文件夹，可以导入
import_text_btn = ttk.Button(root, text="导入文本", command=import_scripts)
# 设置按键位置和大小
import_text_btn.place(x=640, y=360, width=200, height=40)

# 创建文案拆分按键。调用文案拆分功能，选择一个文案文件进行文案拆分，拆分的文案填充 tvsmtable 的 a 列“文案片段”。 调用函数名 sciptssplite()
split_text_btn = ttk.Button(root, text="文案拆分", command=sciptssplite)
# 设置按键位置和大小
split_text_btn.place(x=850, y=360, width=200, height=40)

# 创建音频生成按键。调用音频生成模块，对应 tvsmtable 中 a 列文案片段，产生的音频片段，填充 tvsmtable 的 d 列“对应的音频文件地址”。调用函数名 text2audio()
gen_audio_btn = ttk.Button(root, text="音频生成", command=text2audio)
# 设置按键位置和大小
gen_audio_btn.place(x=1060, y=360, width=200, height=40)

# 创建关键词提取按键，调用关键词提取功能，对应 tvsmtable 中 a 列文案片段，产生的关键词 list 填充 tvsmtable 的 c 列“对应的关键词”。调用函数名 text2keywords()
extract_keywords_btn = ttk.Button(root, text="关键词提取", command=text2keywords)
# 设置按键位置和大小
extract_keywords_btn.place(x=1270, y=360, width=200, height=40)

# 创建图片获取按键，对应 tvsmtable 中 b 列“补充要求”和 c 列“对应的关键词”进行图片的爬取或 dalle 模型生成。具体选择那种方式由补充要求给出，具体如何处理在下面会详细叙述。产生的图片文件的地址填充 tvsmtable 的 e 列。文件也会根据情况保存在本地，自动命名，命名问题在后文该模块的描述中细说。调用函数名 text2img()
get_img_btn = ttk.Button(root, text="图片获取", command=text2img)
# 设置按键位置和大小
get_img_btn.place(x=10, y=510, width=200, height=40)

# 创建视频片段合成模块，调用视频合成功能。对应 tvsmtable 中 a 列，d 列，e 列合成视频片段，根据其对应的文件的地址，合成视频片段，产生的视频文件的地址填充 tvsmtable 的 f 列。文件也会保存在本地，自动命名，命名问题在后文该模块的描述中细说。调用函数名 videocompose()
compose_video_btn = ttk.Button(root, text="视频片段合成", command=videocompose)
# 设置按键位置和大小
compose_video_btn.place(x=220, y=510, width=200, height=40)

# 创建视频拼接模块，对应 tvsmtable 中 f 列，将那些视频片段对应拼接起来，组成一个长视频。文件保存在“works”下。调用函数名 videoconcate()
concate_video_btn = ttk.Button(root, text="视频拼接", command=videoconcate)
# 设置按键位置和大小
concate_video_btn.place(x=430, y=510, width=200, height=40)

# 创建清空表格的按键。调用函数名 clear()
clear_btn = ttk.Button(root, text="清空表格", command=clear)
# 设置按键位置和大小
clear_btn.place(x=640, y=510, width=200, height=40)

# 创建追加导入表格内容的按键。选择文件，将文件信息以追加的方式填入表格。调用函数名 import_data()
append_btn = ttk.Button(root, text="追加导入表格内容", command=import_data)
# 设置按键位置和大小
append_btn.place(x=850, y=510, width=200, height=40)



root.mainloop()

import jmcomic
import re
import shutil
import zipfile
from wxauto import *
import os

# 从文本文件中读取内容
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


# 获取当前微信客户端
wx = WeChat()


# 获取会话列表
wx.GetSessionList()

jm_code = "111111"

while 1:
    msgs = wx.GetAllMessage(savepic=True)   # 获取聊天记录，及自动下载图片
    if msgs[-1].type == 'friend':
            sender = msgs[-1].sender_remark  # 获取备注名
            question = f'{sender.rjust(20)}：{msgs[-1].content}'
            print(question)
            res = re.search(r'jm(\d+)', question)
            if res:
                jm_code1 = res.group(1)
                print("提取的数字为：", jm_code1)
                if jm_code1 != jm_code:
                    jm_code = jm_code1
                    jmcomic.download_album(jm_code) 
                    # 当前目录路径
                    当前目录 = os.getcwd()

                    # 压缩包名称
                    压缩包名 = f"{jm_code}.zip"
                    压缩包路径 = os.path.join(当前目录, 压缩包名)

                    # 创建一个 Zip 文件
                    with zipfile.ZipFile(压缩包路径, 'w', zipfile.ZIP_DEFLATED) as 压缩包:
                        for 项目名 in os.listdir(当前目录):
                            项目路径 = os.path.join(当前目录, 项目名)
                            # 如果是文件夹才进行压缩
                            if os.path.isdir(项目路径):
                                for 根路径, _, 文件列表 in os.walk(项目路径):
                                    for 文件名 in 文件列表:
                                        文件完整路径 = os.path.join(根路径, 文件名)
                                        相对路径 = os.path.relpath(文件完整路径, 当前目录)
                                        压缩包.write(文件完整路径, arcname=相对路径)
                    print(f"✅ 所有文件夹已压缩为 {jm_code}.zip")

                    who = 'jm下载群'
                    file = [
                        rf'C:\Users\QuQiZhouSi\Desktop\wechat-auto-jmcomic\{jm_code}.zip',
                    ]
                    wx.SendFiles(filepath=file, who=who)

                    # 删除所有子文件夹
                    for 项目名 in os.listdir(当前目录):
                        项目路径 = os.path.join(当前目录, 项目名)
                        if os.path.isdir(项目路径):
                            shutil.rmtree(项目路径)

                    # 删除压缩包
                    if os.path.exists(压缩包路径):
                        os.remove(压缩包路径)

                    print("✅ 所有文件夹和压缩包已删除")

                else:
                    print("未找到格式为 'jm数字' 的子串")
        


# import re

# # 原始字符串
# 原字符串 = "abcjm123453413xyzjm678test"

# # 正则表达式查找匹配 "jm" 后跟一串数字的子串
# 匹配结果 = re.search(r'jm(\d+)', 原字符串)

# if 匹配结果:
#     数字部分 = 匹配结果.group(1)
#     print("提取的数字为：", 数字部分)
# else:
#     print("未找到格式为 'jm数字' 的子串")

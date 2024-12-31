#version 0627-2
import os
from openai import AzureOpenAI
import json

# text_root_path=st.text_input("请输入总的txt文件夹路径，比如D:\XXX\卧室,D:\XXX\厨房,D:\XXX\客厅,输入D:\XXX即可",value="")
text_root_path=r"D:\lprojects\AI标签\打标图和txt\水壶00"
    ##所有txt文件读取合并并去重
def read_txt_files(text_root_path):
    all_tags=set()
    for folder,subfolder,files in os.walk(text_root_path):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    all_tags.update(content.split(','))
    return all_tags

all_tags=read_txt_files(text_root_path)
all_tags_list=list(all_tags)
x_of_tags=all_tags_list[0:10]
x_of_tags_str='\n'.join(x_of_tags)
all_tags_str='\n'.join(all_tags_list)
#这样输出的东西和苏泊尔词库提取的prompt_database.txt是一样的，都是一个短语一行
print(x_of_tags_str)
os.makedirs("output", exist_ok=True)
with open("output/x_of_tags.txt", 'w', encoding='utf-8') as f:
    f.write(x_of_tags_str)
with open("output/all_tags.txt", 'w', encoding='utf-8') as f:
    f.write(all_tags_str)


import os
import sys

# # 获取utils目录的路径
# current_dir = os.path.dirname(os.path.abspath(__file__))
# # 将utils目录添加到系统路径
# sys.path.append(current_dir)

# 现在可以导入了
from utils.azure_client import get_client
import os
from openai import AzureOpenAI
import json

# text_root_path=st.text_input("请输入总的txt文件夹路径，比如D:\XXX\卧室,D:\XXX\厨房,D:\XXX\客厅,输入D:\XXX即可",value="")
text_root_path=r"D:\lprojects\AI标签\打标图和txt\水壶00"
    ##所有txt文件读取合并并去重
def read_txt_files(text_root_path):
    all_tags = set()
    for folder, subfolder, files in os.walk(text_root_path):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    all_tags.update(content.split(','))
                    # # 按逗号分割，并处理每个标签
                    # tags = [tag.strip().lower() for tag in content.split(',') if tag.strip()]
                    # all_tags.update(tags)
    return all_tags

client=get_client()

##每次gpt处理X个tags，然后拼接起来，直到处理完所有tags。按照原代码每次最大处理100行
##怕是因为gpt-4o的上下文长度限制，所以需要分批处理。
def gpt_classfiy(x_of_tags, prompt):
    # 将标签列表转换为字符串
    #这个修改将标签列表转换为用换行符分隔的字符串。这样可以确保发送给 GPT API 的消息内容是正确的字符串格式。
    tags_str = '\n'.join(x_of_tags)  # 添加这行
    
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": tags_str},  # 使用转换后的字符串
    ]
    response = client.chat.completions.create(
        model="gpt-4o", # 或者使用gpt-4模型model = "gpt-4"
        messages=messages,
    )
    result = response.choices[0].message.model_dump_json(indent=2)
    data = json.loads(result)
    return data['content']

def gpt_classfiy_all(all_tags, prompt, max_tags):
    # 将 set 转换为 list
    all_tags = list(all_tags)
    new_tags_all = ""  # 将变量声明移到函数内部
    for i in range(0, len(all_tags), max_tags):
        x_of_tags = all_tags[i:i+max_tags]
        new_tags = gpt_classfiy(x_of_tags, prompt)
        new_tags_all += new_tags
        print(f"Processing line {i+1} of {len(all_tags)}")
    print(new_tags_all)
    return new_tags_all

    i = 1
    while True:
        filename = f"{i:03d}.{extension}"
        if not os.path.exists(os.path.join(directory, filename)):
            return filename
        i += 1


main_product="水壶Kettle"
category="地点、装饰风格、氛围、光强、光源方向、主体产品视角、主体产品位置、主体产品细节、其他物品、背景、背景清晰度、窗外风景"
eg="""
office scenario地点  
bedroom地点  
minimalistic modern home style装饰风格  
warm tone氛围  
light color氛围  
evening ambiance氛围  
bright atmosphere光强  
light from the left side光源方向  
eye-level view主体产品视角  
side view主体产品视角  
Kettle on a side table主体产品位置  
Kettle on kitchen countertop主体产品位置  
white ribbed electric kettle with silver accents and white plastic handle主体产品细节  
grey electric kettle主体产品细节  
two glass mugs with drinks on beige plate其他物品  
porcelain teacup with saucer其他物品  
cream-colored coffee maker in the background背景  
blurred background背景清晰度  
scenic outdoor view through window窗外风景  
"""

prompt=f"""
主体产品是{main_product}。
每行的英文词组————tag是需要判断分类的的内容，请输出一种类别（{category}）在英文词组的后面。中间用一个tab制表符隔开。
输出的格式：
Engligh tag   对应的类别
尝试根据"```"包围的文字中，归纳分类标准，并进行分类。
一些分类案例如下：
```
{eg}
```
"""
##上面这个prompt是能够得到统一格式的。但是输出到excel里面少了许多东西。

prompt=f"""
主体产品是{main_product}。
第一列是需要判断类别的句子，请输出一种类别（{category}）在第二列。中间用一个tab制表符隔开。
尝试根据"```"包围的文字中，归纳分类标准，并进行分类。
其他分类案例如下：
```
{eg}
```
"""
# 有这些，就能够得到 open lid  主体产品细节这种结构了。但是就是中文英文之间的距离不太一样，并且不是相同的分类
# 放在一块儿的，就是很散。见dump/output
# 但是有很多分类错误的。可能得再处理一下。
# new_tags=gpt_classfiy_all(read_txt_files(text_root_path),prompt,100)
# output_path = r"D:\lprojects\AI标签\试验\output.txt"
# with open(output_path, 'w', encoding='utf-8') as f:
#     print("Writing to", output_path)
#     f.write(new_tags)

#将new_tags写入output.txt
def write_txt(new_tags,output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        print("Writing to", output_path)
        f.write(new_tags)



##将txt文件转换为excel文件
import pandas as pd

def process_txt_to_excel(input_file, output_file):
    # 创建一个字典来存储不同标签的内容
    categories = {
        '其他物品': [],
        '主体产品细节': [],
        '主体产品位置': [],
        '窗外风景': [],
        '背景': [],
        '氛围': [],
        '地点': [],
        '装饰风格': [],
        '光源方向': [],
        '背景清晰度': [],
        '主体产品视角': [],
        '光强': []
    }
    
    # 读取文件
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    # 处理每一行,这个方法还有局限，主要还是看gpt返回的分类文字格式是什么样的。解决方法：把这个方法巩固成涵盖多种情况的或者
    #给gpt的prompt里面，让他返回的格式是固定的。
    for line in lines:
        line = line.strip()
        if line and '\t' in line:  # 确保行不为空且包含制表符
            parts = line.split('\t')
            if len(parts) >= 2:  # 确保至少有2个部分
                english_text = parts[0]
                category = parts[-1]  # 取最后一部分作为类别
                if category in categories:
                    categories[category].append(english_text.strip())
    
    # 找出最长的列的长度
    max_length = max(len(items) for items in categories.values())
    
    # 将所有列填充到相同长度
    for category in categories:
        categories[category].extend([''] * (max_length - len(categories[category])))
    
    # 创建DataFrame
    df = pd.DataFrame(categories)
    
    # 保存到Excel
    df.to_excel(output_file, index=True)
    print(f"已成功将数据保存到 {output_file}")

import os
import pandas as pd

input_file=r"D:\lprojects\AI标签\打标图和txt\水壶00\output.txt"
output_file=r"D:\lprojects\AI标签\打标图和txt\水壶00\output222.xlsx"
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
        
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        lines_count=len(lines)
        print(lines_count)
        for line in lines:
            line = line.strip()
            #print(line)
            # 从右边分割一次，这样可以确保类别在最后一部分
            parts = line.rsplit(None, 1)  # None表示按任意空白字符分割
            
            if len(parts) >= 2:  # 确保至少有2个部分
                english_text = parts[0]
                category = parts[1]  # 最后一部分作为类别
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

process_txt_to_excel(input_file, output_file)

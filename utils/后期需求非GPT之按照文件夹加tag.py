import os
styles = ["Dopamine-style", "Creamy-style"]
scenarios = ["bedroom", "dining room", "living room", "kitchen"]

root_path = r"\\192.168.0.1\share2\01设计组\乐屋\1205处理完数据集"
for folderpath, subfolders, files in os.walk(root_path):
    if files:
        for file in files:
            if file.endswith(".txt"):
                # 获取文件名中的风格和场景
                style_translation = ""
                scenario_translation = ""
                
                # 匹配风格
                if "多巴胺" in file:
                    style_translation = "Dopamine-style"
                elif "奶油" in file:
                    style_translation = "Creamy-style"
                
                # 匹配场景
                if "卧室" in file:
                    scenario_translation = "bedroom"
                elif "餐厅" in file:
                    scenario_translation = "dining room"
                elif "客厅" in file:
                    scenario_translation = "living room"
                elif "厨房" in file:
                    scenario_translation = "kitchen"
                
                if style_translation and scenario_translation:
                    # 读取文件内容
                    with open(os.path.join(folderpath, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 在触发词后面添加翻译
                    trigger = "lewu_design, "  # 实际的触发词
                    new_content = content.replace(trigger, f"{trigger}{style_translation}, {scenario_translation}, ")
                    
                    # 写回文件
                    with open(os.path.join(folderpath, file), 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"处理文件: {file}")
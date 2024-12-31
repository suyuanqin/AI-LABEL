import os 
import streamlit as st
from utils.azure_client import get_client
from utils.gpt_词库提取 import read_txt_files,gpt_classfiy_all,write_txt,process_txt_to_excel
import json

st.title("打标后处理")

tab0,tab1,tab2=st.tabs(["自定义tag和逗号位置一键添加tag",
                             "中英图阅读",
                             "所有tags根据维度提取成词库"])
if 'class_folders' not in st.session_state:
    st.session_state.class_folders = []
if 'folder_tags' not in st.session_state:
    st.session_state.folder_tags = {}


with tab0:
    def add_tag(text_folder_path, new_tag, index):
        # 添加进度提示
        progress_text = st.empty()
        progress_text.write("开始处理文件...")
        total_files = len(os.listdir(text_folder_path))
        progress_bar = st.progress(0)
        processed_files = 0
        
        # 创建新的输出文件夹
        new_text_folder_path = os.path.join(text_folder_path, f"{new_tag}")
        os.makedirs(new_text_folder_path, exist_ok=True)
        
        for file in os.listdir(text_folder_path):
            if file.endswith(".txt"):
                # 读取原始文件内容
                with open(os.path.join(text_folder_path, file), "r", encoding="utf-8") as f:
                    content = f.read().strip()
                
                # 将内容按逗号分割
                parts = content.split(',')
                
                # 确保index是整数
                idx = int(index)
                
                # 在指定位置插入新标签
                if idx <= len(parts):
                    parts.insert(idx, new_tag)
                    new_content = ','.join(parts)
                    
                    # 写入新文件
                    new_file_path = os.path.join(new_text_folder_path, file)
                    with open(new_file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                
                processed_files += 1
                progress_bar.progress(processed_files / total_files)
                st.write(f"已处理{processed_files}个文件，还剩{total_files-processed_files}个文件")
        
        progress_text.write("处理完成！✨")
    st.write("根据文件夹添加tag方法三")
    text_folder_path=st.text_input("请输入txt文件路径",value=r"xxx\tags",key="text_folder_path")
    new_tag=st.text_input("请输入新tag",value="",key="new_tag")
    index=st.text_input("请输入新tag在哪个位置加,输入数字，不超过TXT文件中的逗号数量",value="", key="index")
    if st.button("添加tag",key="add_tag"):
        add_tag(text_folder_path,new_tag,index)

with tab1:
    def translate_text(text,language):
        prompt=f"请将以下标签翻译成{language}：{text}"
        client = get_client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}, 
                      {"role": "user", "content": [{"type": "text", "text": text}]}])
        result = response.choices[0].message.model_dump_json(indent=2)
        data = json.loads(result)
        translated_text = data['content'].replace('\n', '')
        return translated_text
    st.write("中英文和图片对比阅读")
    text=st.text_input("请输入英文",value="")
    if st.button("翻译"):
        st.write(translate_text(text,"中文"))
    image_path=st.text_input("请输入图片路径",value="")
    if st.button("阅读"):
        st.image(image_path,width=128)

with tab2:
    st.write("词库提取成表格形式")
    text_root_path=st.text_input("请输入总的txt文件夹路径，比如D:\XXX\卧室,D:\XXX\厨房,D:\XXX\客厅,输入D:\XXX即可",value="",key="tags_root_path")
    output_path=st.text_input("请输入输出路径",value=r"D:\lprojects\AI标签\试验",key="tags_output_path")
    output_path_xlsx=os.path.join(output_path,"output.xlsx")
    output_path_txt=os.path.join(output_path,"output.txt")
    prompt=st.text_input("请输入prompt",value="")
    if st.button("提取",key="extract"):
        st.progress(0)
        ##所有txt文件读取合并并去重
        all_tags=read_txt_files(text_root_path)
        st.progress(10)
        all_tags_list=list(all_tags)
        st.progress(20)
        new_tags=gpt_classfiy_all(all_tags_list,prompt,100)
        st.progress(90)
        write_txt(new_tags,output_path_txt)
        process_txt_to_excel(output_path_txt,output_path_xlsx)
        st.progress(100)
        st.success("提取完成！✨")

# with tab0:
#     st.write("比如不同视角文件夹的图片，根据文件夹名字添加tag")
#     st.write("注意事项：是根据图片文件名和txt文件名进行匹配，所以需要图片和txt文件名一致")
#     root_folder=st.text_input("请输入根文件夹路径",value=r"D:\lprojects\AI_npc\场景")
#     txt_folder=st.text_input("请输入打标tag文件夹路径",value=r"D:\lprojects\AI_npc\tag")
#     def folder_name_to_tag(root_folder):
#         class_folders=[]
#         for folderpath,subfolder,files in os.walk(root_folder):
#             if subfolder:
#                 class_folders.append(subfolder)
#         return class_folders
#     st.session_state.class_folders=folder_name_to_tag(root_folder)
#     st.write(st.session_state.class_folders)

#     # 为每个文件夹创建一个输入框和提交按钮
#     for folder_list in st.session_state.class_folders:
#         for folder in folder_list:  # 因为class_folders是嵌套列表
#             col1, col2, col3 = st.columns([2, 2, 1])
            
#             with col1:
#                 st.write(folder)
            
#             with col2:
#                 tag_input = st.text_input(
#                     label="输入标签",
#                     key=f"input_{folder}",
#                     value=st.session_state.folder_tags.get(folder, "")  # 如果已有值则显示
#                 )
            
#             with col3:
#                 if st.button("提交", key=f"submit_{folder}"):
#                     st.session_state.folder_tags[folder] = tag_input
#                     st.success(f"已添加标签: {folder} -> {tag_input}")

#     # 显示当前的所有标签映射
#     st.write("当前文件夹标签映射：")
#     st.write(st.session_state.folder_tags)

     
#     def add_class_tag(root_folder,txt_folder):
#         # 添加进度提示
#         progress_text = st.empty()
#         progress_text.write("开始处理文件...")
        
#         txt_files=[]
#         for file in os.listdir(txt_folder):
#             if file.endswith(".txt"):
#                 txt_files.append(file)
#         st.write(f"总的txt_files数量：{len(txt_files)}")
                
#         # 获取总文件数用于进度显示
#         total_files = sum(len([f for f in files if f.endswith((".png","jpg","jpeg"))])
#                          for _, _, files in os.walk(root_folder))
#         progress_bar = st.progress(0)
#         processed_files = 0

#         for folderpath,subfolder,files in os.walk(root_folder):
#             for file in files:
#                 if file.endswith((".png","jpg","jpeg")):
#                    progress_text.write(f"正在处理: {file}")
#                    image_name,image_ext=os.path.splitext(file)
#                    if image_name in [f.split('.')[0] for f in txt_files]:
#                        folder_name=os.path.basename(folderpath)
#                        tag=st.session_state.folder_tags.get(folder_name,"")
#                        if tag:
#                            try:
#                                # 先读取原内容
#                                with open(os.path.join(txt_folder, image_name+".txt"), "r", encoding="utf-8") as f:
#                                    original_content = f.read().strip()
                               
#                                # 组合新内容
#                                new_content = f"{original_content}, {tag}" if original_content else tag
                               
#                                # 写入新内容
#                                with open(os.path.join(txt_folder, image_name+".txt"), "w", encoding="utf-8") as f:
#                                    f.write(new_content)
#                            except FileNotFoundError:
#                                # 如果文件不存在，直接创建新文件
#                                with open(os.path.join(txt_folder, image_name+".txt"), "w", encoding="utf-8") as f:
#                                    f.write(tag)
                   
#                    processed_files += 1
#                    progress_bar.progress(processed_files / total_files)
        
#         progress_text.write("处理完成！✨")
#     if st.button("添加tag"):
#         add_class_tag(root_folder,txt_folder)

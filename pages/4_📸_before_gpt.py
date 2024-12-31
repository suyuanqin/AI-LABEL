import streamlit as st
import os
import base64
from utils.前期需求_filter_image import judge_remove_image
from utils.前期需求非GPT之改图片格式 import all_rename_image
from utils.azure_client import get_client

import json


st.title("各种前期处理小工具")
#init st.session_state
if "tags" not in st.session_state:
    st.session_state.tags = ""  # 初始化tags为空字符串
if "tags_translated" not in st.session_state:
    st.session_state.tags_translated = ""  # 初始化tags_translated为空字符串

tab0,tab1,tab2=st.tabs(["传图试打标看效果","筛选小于400像素图片","图片格式全部转成jpg"])
def gpt_tagnn(image_base64,prompt):
        client = get_client()
        mime_type = 'image/jpeg'

        if mime_type:
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {
                        "url": f"data:{mime_type};base64,{image_base64}"
                    }}
                ]}
            ]
        else:
            st.error("不支持的图片格式")
            return None

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        result = response.choices[0].message.model_dump_json(indent=2)
        data = json.loads(result)
        gpttags = data['content']#.replace('\n', '')#不要去掉换行符

        return gpttags
def translate_text(text,language):
    prompt=f"请将以下标签翻译成{language}：{text}"
    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": [{"type": "text", "text": text}]}])
    result = response.choices[0].message.model_dump_json(indent=2)
    data = json.loads(result)
    translated_text = data['content'].replace('\n', '')
    return translated_text

with tab0:
    st.write("开发中")
    prompt = st.text_area("请输入prompt：", value="", key="single_image_prompt")
    uploaded_image = st.file_uploader("请上传图片", type=["jpg", "jpeg", "png"], key="single_image_uploader")
    translate_checkbox = st.checkbox("是否翻译成中文", value=True, key="translate_checkbox")
    
    if uploaded_image:
        st.image(uploaded_image,width=128)
        image_base64 = base64.b64encode(uploaded_image.read()).decode("utf-8")
        
    if st.button("开始打标", key="single_image_btn"):
        tags = gpt_tagnn(image_base64, prompt)
        st.success("打标完成！")
        print(tags)
        st.markdown(tags)
        st.session_state.tags = tags
        
        if translate_checkbox:
            tags_translated = translate_text(tags, "Chinese")
            st.markdown(tags_translated)
            st.session_state.tags_translated = tags_translated

    # 批量打标部分
    st.divider()
    folder_path = st.text_input("请输入需要批量打标的图片文件夹路径：", key="batch_tag_path")
    
    if st.button("开始批量打标", key="batch_tag_btn"):
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(folder_path, file)
                    with open(img_path, "rb") as image_file:
                        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
                    
                    # 生成标签
                    tags = gpt_tagnn(image_base64, prompt)
                    if translate_checkbox:
                        tags = translate_text(tags, "Chinese")
                    
                    # 保存为同名txt文件
                    txt_path = os.path.splitext(img_path)[0] + '.txt'
                    with open(txt_path, 'w', encoding='utf-8') as f:
                        f.write(tags)
                    
                    st.write(f"已完成 {file} 的打标")
            
            st.success("批量打标完成！")
        else:
            st.error("文件夹路径不存在！")

with tab1:
    folder_path = st.text_input("请输入图片文件夹路径：", value="D:\lprojects\AI_npc\场景",key="filter_small_image")
    dump_path=os.path.join(folder_path,"弃用")

    def filter_image(folder_path,dump_path,status_placeholder):
        status_text = ""  # 初始化状态文本
        for file in os.listdir(folder_path):
            if file.endswith((".png","jpg","jpeg")):
                T_F=judge_remove_image(os.path.join(folder_path, file),dump_path)
                if T_F:
                    status_text += f"已筛选 {file}\n"  # 将新状态附加到现有状态
                    status_placeholder.text(status_text)  # 更新状态显示


    # 创建一个按钮，并检查是否被点击
    if st.button("开始筛选图片",key="filter_small_image_btn"):
        # 确保dump_path目录存在
        os.makedirs(dump_path, exist_ok=True)
        status_placeholder = st.empty()
        # 执行筛选函数
        filter_image(folder_path,dump_path,status_placeholder)
        # 可以添加完成提示
        st.success("图片筛选完成！")

with tab2:
    root_path = st.text_input("请输入图片文件夹路径：", value="D:\lprojects\AI_npc\场景",key="all_otherformat2jpg")
    if st.button("开始转换图片格式", key="all_otherformat2jpg_btn"):
        # 创建一个空容器用于显示状态
        status_placeholder = st.empty()
        # 传入status_placeholder到要调用的函数中
        all_rename_image(root_path, status_placeholder)
        # 处理完成后显示成功消息
        st.success("图片格式转换完成！")

import streamlit as st
import os

from utils.前期需求_filter_image import judge_remove_image
from utils.前期需求非GPT之改图片格式 import all_rename_image
from utils.azure_client import get_client
# from utils.后期gpt批量去重_翻译 import translate_text就是这个导致每次这个页面很久都打不开
import json


st.title("各种前期处理小工具")
tab0,tab1=st.tabs(["筛选小于400像素图片","图片格式全部转成jpg"])


with tab0:
    st.write("开发中")
    # folder_path = st.text_input("请输入图片文件夹路径：", value="D:\lprojects\AI_npc\场景",key="filter_small_image")
    # dump_path=os.path.join(folder_path,"弃用")

    # def filter_image(folder_path,dump_path,status_placeholder):
    #     status_text = ""  # 初始化状态文本
    #     for file in os.listdir(folder_path):
    #         if file.endswith((".png","jpg","jpeg")):
    #             T_F=judge_remove_image(os.path.join(folder_path, file),dump_path)
    #             if T_F:
    #                 status_text += f"已筛选 {file}\n"  # 将新状态附加到现有状态
    #                 status_placeholder.text(status_text)  # 更新状态显示


    # # 创建一个按钮，并检查是否被点击
    # if st.button("开始筛选图片",key="filter_small_image_btn"):
    #     # 确保dump_path目录存在
    #     os.makedirs(dump_path, exist_ok=True)
    #     status_placeholder = st.empty()
    #     # 执行筛选函数
    #     filter_image(folder_path,dump_path,status_placeholder)
    #     # 可以添加完成提示
    #     st.success("图片筛选完成！")

with tab1:
    st.write("开发中")
    # root_path = st.text_input("请输入图片文件夹路径：", value="D:\lprojects\AI_npc\场景",key="all_otherformat2jpg")
    # if st.button("开始转换图片格式", key="all_otherformat2jpg_btn"):
    #     # 创建一个空容器用于显示状态
    #     status_placeholder = st.empty()
    #     # 传入status_placeholder到要调用的函数中
    #     all_rename_image(root_path, status_placeholder)
    #     # 处理完成后显示成功消息
    #     st.success("图片格式转换完成！")




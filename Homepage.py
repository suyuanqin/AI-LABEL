import streamlit as st

st.set_page_config(page_title="AITool", layout="wide")

st.title("欢迎使用 AITool")

st.markdown("""
### 功能介绍
- 📝 **TXT Editor**: GPT图片打标工具
- 🖼️ **IMG Editor**: 图片编辑工具（开发中）
- ⚙️ **Settings**: 系统设置
- 📸 **before gpt**: 图片前期的处理工具（格式转换，筛除小图，单张图试打标）（开发中）
- 🎇 **after gpt**: 图片后期的处理工具（在文件夹中一键添加tag）

请在左侧边栏选择要使用的功能。
""") 
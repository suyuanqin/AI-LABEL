import streamlit as st

# Web interface for user inputs
st.title("Tag Classification Tool")

main_product = st.text_input("Enter main product (e.g. 水壶Kettle):", value="水壶Kettle")

# Use text_area for category input with default values
default_categories = "地点、装饰风格、氛围、光强、光源方向、主体产品视角、主体产品位置、主体产品细节、其他物品、背景、背景清晰度、窗外风景"
category = st.text_area("Enter categories (separated by '、'):", value=default_categories)

# Example input can also be customizable
default_examples = """
office scenario地点  
bedroom地点  
minimalistic modern home style装饰风格  
# ... (other examples)
"""
eg = st.text_area("Enter classification examples:", value=default_examples)

# Generate prompt only when user inputs are ready
if st.button("Generate Classification"):
    prompt = f"""
    主体产品是{main_product}。
    第一列是需要判断类别的句子，请输出一种类别（{category}）在第二列。中间用一个tab制表符隔开。
    尝试根据"```"包围的文字中，归纳分类标准，并进行分类。
    其他分类案例如下：
    ```
    {eg}
    ```
    """
    # Continue with existing processing...
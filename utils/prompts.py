import streamlit as st

@st.cache_data
def generate_prompt0():
    prompt = """
    You are a product photography analyzer.

    Task:
    Based on the picture I gave you, describe the content in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length
    """
    return prompt

@st.cache_data
def generate_prompt1():
    prompt = """
    You are a product photography analyzer.

    Task:
    - Analyze the product photo and generate detailed English tags describing the following aspects:
      1. Main product details (e.g., material, features, texture, design)
      2. Main product perspective (e.g., top view, side view, eye-level view)
      3. Decorative style (e.g., modern, minimalist, vintage)
      4. Atmosphere (e.g., calm, cozy, vibrant)
      5. Color scheme (e.g., neutral tones, pastel colors, bright colors)
      6. Lighting (e.g., soft natural light, bright, dim, high contrast)
      7. Decorative elements (e.g., plants, books, sculptures)
      8. Background (e.g., blurred, clear, outdoor, indoor)

    - Provide the tags in a comma-separated format.
    - Each tag should be concise and no more than 20 words.
    """
    return prompt

@st.cache_data
def generate_prompt2():
    prompt = """
    You are a product photography analyzer.

    Task:
    Based on the picture I gave you, describe the content in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. Main product details (e.g., material, features, texture, design)
    2. Main product perspective (e.g., top view, side view, eye-level view)
    3. Decorative style (e.g., modern, minimalist, vintage)
    4. Atmosphere (e.g., calm, cozy, vibrant)
    5. Color scheme (e.g., neutral tones, pastel colors, bright colors)
    6. Lighting (e.g., soft natural light, bright, dim, high contrast)
    7. Decorative elements (e.g., plants, books, sculptures)
    8. Background (e.g., blurred, clear, outdoor, indoor)
    """
    return prompt

@st.cache_data
def generate_prompt3():
    prompt = """
    You are a product photography analyzer.

    Task:
    Based on the picture I gave you, describe the content in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. Main product details (e.g., material, features, texture, design)
    2. Main product perspective (e.g., top view, side view, eye-level view)
    3. Decorative style (e.g., modern, minimalist, vintage)
    4. Atmosphere (e.g., calm, cozy, vibrant)
    5. Color scheme (e.g., neutral tones, pastel colors, bright colors)
    6. Lighting (e.g., soft natural light, bright, dim, high contrast)
    7. Other objects besides the main product 
    8. Background (e.g., blurred, clear, outdoor, indoor)
    """
    return prompt

@st.cache_data
def generate_prompt4():
    prompt = """
    You are a product photography analyzer.

    Task:
    Based on the picture I gave you, describe the content in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. Main product details
    2. Main product perspective
    3. Decorative style
    4. Atmosphere
    5. Color scheme
    6. Lighting
    7. Other objects besides the main product 
    8. Background
    """
    return prompt

@st.cache_data
def generate_prompt5():
    prompt = """
    You are a product photography analyzer.

    Task:
    Based on the picture I gave you, describe the content in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. Main product details(e.g., color, material, features, texture, design)
    2. Main product perspective(e.g., top view, side view, eye-level view)
    3. Main product location(e.g., on the table, on the shelf, on the floor)
    4. Decorative style(e.g., modern, minimalist, vintage)
    5. Atmosphere(e.g., calm, cozy, vibrant)
    6. Color scheme(e.g., neutral tones, pastel colors, bright colors)
    7. Lighting (e.g., soft natural light, bright, dim, high contrast)
    8. Lighting direction(e.g., from the left, from the right, from the top, from the bottom)
    9. Other objects besides the main product 
    10. Background
    """
    return prompt

@st.cache_data
def generate_prompt6():
    main_product = "Kettle"
    prompt = f"""
    You are a product photography analyzer.
    main_product: {main_product}

    Task:
    Based on the picture I gave you, describe the content in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. Main product details(e.g., color, material, features, texture, design)
    2. Main product perspective(e.g., top view, side view, eye-level view)
    3. Main product location(e.g., on the table, on the shelf, on the floor)
    4. Decorative style(e.g., modern, minimalist, vintage)
    5. Atmosphere(e.g., calm, cozy, vibrant)
    6. Color scheme(e.g., neutral tones, pastel colors, bright colors)
    7. Lighting (e.g., soft natural light, bright, dim, high contrast)
    8. Lighting direction(e.g., from the left, from the right, from the top, from the bottom)
    9. Other objects besides the main product 
    10. Background
    """
    return prompt

@st.cache_data
def generate_prompt7():
    prompt= f"""
    You are a room design analyzer.
    
    Task:
    Based on the picture I gave you, describe the content in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. 房间的装修风格
    2. 房间的色彩搭配
    3.房间灯光
    3.1灯光类型（自然光，人工光）
    3.2灯光亮度（明亮，昏暗，柔和，强烈）
    3.3灯光颜色（暖光，冷光，中性光）
    4. 房间的家具
    5. 家具的形状，颜色，材质，装饰图案
    6. 房间的装饰品
    7. 房间的墙壁
    8. 房间的地面
    8. 房间的天花板
    9. 房间的窗户
    10. 房间的门
    """
    return prompt

@st.cache_data
def generate_prompt8():
    prompt = """
      You are a product image analyzer.
    
    Task:
    Based on the picture I gave you, describe the content in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. 产品的外观
    1.1 产品的形状
    1.2 详细描述产品各个部件
    1.3 产品的颜色
    1.4 产品的材质
    1.5 产品部件的装饰工艺（压花，哑光等等）
    2光线
    等等
    从上到下进行描述，不要遗漏
    tags全部都是**英文**in English*
    """
    return prompt

def call_generate_function(prompt_index):
    """根据序号调用想要的prompt生成函数"""
    function_name = f"generate_prompt{prompt_index}"
    if function_name in globals():  # 检查函数是否存在
        return globals()[function_name]
    else:
        raise ValueError(f"Function {function_name} not found!")

def get_prompt_options():
    return {
        0: "基础模板 - 简单标签生成",
        1: "详细分类模板 - 8个方面详细分析",
        2: "简洁分类模板 - 8个方面简要分析",
        3: "修改分类模板 - 包含其他物体描述",
        4: "简化分类模板 - 无示例自由描述",
        5: "扩展分类模板 - 10个方面详细分析",
        6: "产品特定模板 - 水壶专用分析",
        7: "房间特定模板 - 乐屋专用分析",
        8: "海尔洗衣机模板 - 海尔产品专用分析（无视角版）",
    }
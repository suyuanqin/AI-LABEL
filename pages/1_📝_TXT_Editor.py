import streamlit as st
import os
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import json
import pickle
import time

# 添加项目根目录到Python路径
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from utils.prompts import get_prompt_options, call_generate_function, generate_prompt0, generate_prompt1, generate_prompt2, generate_prompt3, generate_prompt4, generate_prompt5, generate_prompt6
from utils.azure_client import get_client, encode_image
from utils.增删改查之add_by_order import process_add_by_order
from utils.增删改查之add新维度 import process_new_dimension
from utils.增删改查之add水印识别 import add_watermark, process_watermark
from utils.add_operations import add_new_dimension, add_folder_tag

# 缓存文件路径
CACHE_FILE = "history_cache.pkl"

def save_history_to_cache():
    """保存历史记录到缓存文件"""
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(st.session_state.history, f)

def load_history_from_cache():
    """从缓存文件加载历史记录"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            return pickle.load(f)
    return []

st.title("TXT Editor")

# 共享的路径输入，放在标签页之前
root_path = st.text_input("请输入图片文件夹路径：", value="E:\DSY\AILabel\dataset\水壶1")

tab0, tab1, tab2, tab3, tab4 = st.tabs(["4o初始打标", "增", "删", "改", "查"])

with tab0:
    st.header("GPT图片打标工具")
    
    # 移除这里的路径输入
    prompt_options = get_prompt_options()
    prompt_index = st.selectbox(
        "选择prompt模板：", 
        options=list(prompt_options.keys()),
        format_func=lambda x: prompt_options[x]
    )
    trigger = st.text_input("请输入trigger词", value="SUPORBJ,")
    
    # 显示历史记录
    if 'history' not in st.session_state:
        st.session_state.history = load_history_from_cache()
        
    history_container = st.empty()  # 创建一个容器用于更新历史记录
    
    def update_history_display():
        """更新历史记录显示"""
        if st.session_state.history:
            with history_container.container():
                st.subheader("处理历史记录")
                history_df = pd.DataFrame(st.session_state.history)
                st.dataframe(history_df)
                
                # 创建两列
                col1, col2 = st.columns([1, 5])
                with col1:
                    # 导出按钮 - 使用时间戳作为唯一key
                    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                    if st.button("导出历史记录", key=f"export_btn_{current_time}"):
                        export_filename = f"tag_history_{current_time}.csv"
                        history_df.to_csv(export_filename, index=False, encoding='utf-8-sig')
                        st.success(f"历史记录已导出为: {export_filename}")

    def gpt_tag(image_path, prompt):
        client = get_client()
        image_base64 = encode_image(image_path)
        file_extension = os.path.splitext(image_path)[1].lower()[1:]

        mime_type = 'image/png' if file_extension == 'png' else 'image/jpeg' if file_extension == 'jpg' else None

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
        new_dimension = data['content'].replace('\n', '')

        return new_dimension

    def process_images():
        if not root_path:
            st.error("请输入有效的文件夹路径")
            return
            
        # 清除之前的历史记录
        st.session_state.history = []
            
        # 创建tag子文件夹
        tag_folder = os.path.join(root_path, "tag")
        os.makedirs(tag_folder, exist_ok=True)
        
        # 进度条和状态显示
        progress_bar = st.progress(0)
        status_text = st.empty()
        time_text = st.empty()  # 添加时间显示
        
        # 创建一个容器来显示处理结果
        result_container = st.container()
        
        # 获取所有图片文件
        image_files = []
        for folderpath, subfolders, files in os.walk(root_path):
            for file in files:
                if file.endswith((".jpg", ".png")):
                    image_files.append((folderpath, file))
        
        total_files = len(image_files)
        start_time = time.time()  # 记录开始时间
        
        for idx, (folderpath, file) in enumerate(image_files):
            file_name, file_ext = os.path.splitext(file)
            image_path = os.path.join(folderpath, file)
            
            # 更新进度和状态
            current_progress = (idx + 1) / total_files
            progress_bar.progress(current_progress)
            status_text.text(f"正在处理: {file} ({idx+1}/{total_files})")
            
            # 计算时间估计
            if idx > 0:  # 至少处理一个文件后才开始估计
                elapsed_time = time.time() - start_time
                avg_time_per_file = elapsed_time / (idx + 1)
                remaining_files = total_files - (idx + 1)
                estimated_remaining_time = avg_time_per_file * remaining_files
                
                # 格式化时间显示
                elapsed_mins, elapsed_secs = divmod(int(elapsed_time), 60)
                remaining_mins, remaining_secs = divmod(int(estimated_remaining_time), 60)
                
                time_text.text(f"""
                已运行: {elapsed_mins}分{elapsed_secs}秒
                预计还需: {remaining_mins}分{remaining_secs}秒
                平均每个文件: {avg_time_per_file:.1f}秒
                """)
            
            try:
                function_name = call_generate_function(prompt_index)
                prompt = function_name()
                tags = gpt_tag(image_path, prompt)
                
                if tags:
                    # 修改文件命名方式，不添加序号
                    new_text_path = os.path.join(tag_folder, file_name + ".txt")
                    with open(new_text_path, "w", encoding="utf-8") as f:
                        full_text = trigger + tags
                        f.write(full_text)
                    
                    # 添加到历史记录，包含标签内容
                    st.session_state.history.append({
                        "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "文件": file,
                        "模板": prompt_options[prompt_index],
                        "状态": "成功",
                        "输出路径": new_text_path,
                        "标签内容": full_text
                    })
                    # 使用容器显示成功消息
                    with result_container:
                        st.success(f"""
                        成功处理: {file}
                        使用模板: {prompt_options[prompt_index]}
                        生成标签: {full_text}
                        """)
                    
            except Exception as e:
                # 记录失败的处理
                st.session_state.history.append({
                    "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "文件名": file,
                    "模板": prompt_options[prompt_index],
                    "状态": f"失败: {str(e)}",
                    "输出路径": "-",
                    "标签内容": "-"
                })
                # 使用容器显示错误消息
                with result_container:
                    st.error(f"""
                    处理失败: {file}
                    使用模板: {prompt_options[prompt_index]}
                    错误信息: {str(e)}
                    """)
            
        # 显示最终运行时间
        total_time = time.time() - start_time
        total_mins, total_secs = divmod(int(total_time), 60)
        time_text.text(f"总运行时间: {total_mins}分{total_secs}秒")
        
        # 保存历史记录到缓存
        save_history_to_cache()
        
        status_text.text("处理完成！")
        st.success(f"所有文件已处理完成，结果保存在 {tag_folder}")

    # 处理按钮
    if st.button("开始处理"):
        process_images()

    # 显示历史记录
    update_history_display() 

with tab1:
    st.header("增加标签")
    
    add_type = st.radio(
        "选择增加方式",
        ["按顺序添加", "新维度添加", "水印识别", "文件夹标签", "自定义标签"]
    )
    
    # 移除这里的路径输入，使用共享的 root_path
    if add_type == "按顺序添加":
        # 读取原始文件
        st.subheader("按顺序添加新标签")
        origin_suffix = st.text_input("原始文件后缀", value="_new_dimension4")
        target_position = st.text_input("目标位置描述", value="在XXX之后")
        ##因为原始process_add_by_order.py里面是以image名字为准的，所以需要在有image的文件夹里使用这个
        if st.button("开始按顺序添加"):
            try:
                with st.spinner("理中..."):
                    client = get_client()  # 获取 Azure OpenAI 客户
                    results, error = process_add_by_order(root_path, origin_suffix, target_position, client)
                    
                    if error:
                        st.error(f"处理失败: {error}")
                    else:
                        # 显示处理结果
                        success_count = sum(1 for r in results if r["status"] == "success")
                        error_count = sum(1 for r in results if r["status"] == "error")
                        
                        st.success(f"成功处理 {success_count} 个文件")
                        if error_count > 0:
                            st.warning(f"处理失败 {error_count} 个文件")
                        
                        # 显示详细结果
                        for result in results:
                            if result["status"] == "success":
                                st.success(f"""
                                处理成功: {result['file']}
                                生成标签: {result['content']}
                                """)
                            else:
                                st.error(f"""
                                处理失败: {result['file']}
                                错误信息: {result['error']}
                                """)
                                
            except Exception as e:
                st.error(f"处理失败: {str(e)}")
    
    elif add_type == "新维度添加":
        st.subheader("添加新维度标签")
        
        # 添加维度说明
        st.markdown("""
        ### 维度说明
        不同的维度代表不同的分析角度：
        
        1. **房间设计维度** (索引=1)
           - 分析空间的整体设计风格
           - 包含：风格、配色、家具布局、照明、空间利用等
           - 适用于：整体场景分析
        
        2. **产品细节维度** (索引=2)
           - 分析产品的具体细节特征
           - 包含：材质、设计特点、表面纹理、颜色变化等
           - 适用于：产品特征分析
        
        3. **交互分析维度** (索引=3)
           - 分析产品的使用和交互方式
           - 包含：手柄设计、握持舒适度、倾倒机制、安全特性等
           - 适用于：产品使用场景分析
        """)
        
        # 添加分隔线
        st.markdown("---")
        
        # 添加提示词索引选择器，带有详细说明
        col1, col2 = st.columns([1, 2])
        with col1:
            prompt_index = st.number_input(
                "提示词索引",
                min_value=1,
                max_value=3,
                value=1,
                help="选择要使用的分析维度的索引号"
            )
        
        with col2:
            dimension_names = {
                1: "房间设计维度 - 分析空间整体设计",
                2: "产品细节维度 - 分析产品具体特征",
                3: "交互分析维度 - 分析产品使用方式"
            }
            st.info(f"当前选择的维度：{dimension_names[prompt_index]}")
        
        # 添加示例输出说明
        with st.expander("查看示例输出"):
            examples = {
                1: "房间设计维度示例标签:\nmodern minimalist style, neutral color palette, open floor plan,\nambient lighting with natural sunlight, efficient space utilization,\nminimal decorative elements, calm and serene atmosphere",
                2: "产品细节维度示例标签:\nbrushed stainless steel material, ergonomic curved design,\nsmooth matte surface texture, gradient silver to black finish,\n360-degree swivel base, premium build quality, unique spout design",
                3: "交互分析维度示例标签:\ncomfortable grip handle, easy-pour spout design,\none-touch lid mechanism, anti-slip base feature,\nintuitive button placement, ergonomic handle angle,\nsuitable for single-hand operation"
            }
            st.markdown(f"### 维度 {prompt_index} 的示例输出：\n\n{examples[prompt_index]}")
        
        if st.button("开始添加新维度"):
            try:
                with st.spinner("处理中..."):
                    client = get_client()
                    results, error = process_new_dimension(root_path, prompt_index, client)
                    
                    if error:
                        st.error(f"处理失败: {error}")
                    else:
                        # 显示处理结果
                        success_count = sum(1 for r in results if r["status"] == "success")
                        error_count = sum(1 for r in results if r["status"] == "error")
                        
                        st.success(f"成功处理 {success_count} 个文件")
                        if error_count > 0:
                            st.warning(f"处理失败 {error_count} 个文件")
                        
                        # 显示详细结果
                        for result in results:
                            if result["status"] == "success":
                                with st.expander(f"查看结果: {result['file']}"):
                                    st.success(f"""
                                    处理成功: {result['file']}
                                    生成标签: {result['content']}
                                    """)
                            else:
                                with st.expander(f"查看错误: {result['file']}"):
                                    st.error(f"""
                                    处理失败: {result['file']}
                                    错误信息: {result['error']}
                                    """)
                                
            except Exception as e:
                st.error(f"处理失败: {str(e)}")
    
    elif add_type == "水印识别":
        st.subheader("水印识别")
        
        if st.button("开始识别水印"):
            try:
                with st.spinner("处理中..."):
                    client = get_client()  # 获取 Azure OpenAI 客户端
                    results, error = process_watermark(root_path, client)  # 传入 client 参数
                    
                    if error:
                        st.error(f"处理失败: {error}")
                    else:
                        # 显示处理结果
                        success_count = sum(1 for r in results if r["status"] == "success")
                        error_count = sum(1 for r in results if r["status"] == "error")
                        
                        st.success(f"成功处理 {success_count} 个文件")
                        if error_count > 0:
                            st.warning(f"处理失败 {error_count} 个文件")
                        
                        # 显示详细结果
                        for result in results:
                            if result["status"] == "success":
                                st.success(f"""
                                处理成功: {result['file']}
                                水印识别结果: {result['watermark']}
                                """)
                            else:
                                st.error(f"""
                                处理失败: {result['file']}
                                错误信息: {result['error']}
                                """)
                                
            except Exception as e:
                st.error(f"处理失败: {str(e)}")
    
    elif add_type == "文件夹标签":
        st.subheader("添加文件夹标签")
        folder_tag = st.text_input("输入要添加的标签")
        
        if st.button("开始添加文件夹标签"):
            try:
                with st.spinner("处理中..."):
                    modified_files, error = add_folder_tag(root_path, folder_tag)
                    if error:
                        st.error(f"处理失败: {error}")
                    else:
                        st.success(f"成功处理 {len(modified_files)} 个文件")
                        st.write("处理的文件:", modified_files)
            except Exception as e:
                st.error(f"处理失败: {str(e)}")
    
    else:  # 自定义标签
        st.subheader("添加自定义标签")
        new_tags = st.text_area("输入要添加的标签（每行一个）")
        
        if st.button("开始添加自定义标签"):
            try:
                with st.spinner("处理中..."):
                    modified_files, error = add_new_dimension(root_path, new_tags)
                    if error:
                        st.error(f"处理失败: {error}")
                    else:
                        st.success(f"成功处理 {len(modified_files)} 个文件")
                        st.write("处理的文件:", modified_files)
            except Exception as e:
                st.error(f"处理失败: {str(e)}")

# ... 其他标签页的代码 ... 
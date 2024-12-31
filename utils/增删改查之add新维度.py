from pathlib import Path
from .file_utils import FileHandler, ProcessTracker
import base64
from openai import AzureOpenAI
import json

def deal_new_dimension(image_path, prompt_index, client):
    """处理新维度标签"""
    try:
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        file_extension = Path(image_path).suffix.lower()[1:]
        mime_type = 'image/png' if file_extension == 'png' else 'image/jpeg' if file_extension in ['jpg', 'jpeg'] else None

        if not mime_type:
            return None, "不支持的图片格式"

        # 获取对应的提示词
        prompt = generate_prompt(prompt_index)
        
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {
                    "url": f"data:{mime_type};base64,{image_base64}"
                }}
            ]}
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        result = response.choices[0].message.model_dump_json(indent=2)
        data = json.loads(result)
        return data['content'].replace('\n', ''), None
    except Exception as e:
        return None, str(e)

def generate_prompt(prompt_index):
    """根据索引生成提示词"""
    prompts = {
        1: """
        You are a room design analyzer.
        Please analyze the image and provide detailed tags for:
        1. Style (e.g., modern, traditional, minimalist)
        2. Color scheme
        3. Furniture arrangement
        4. Lighting
        5. Space utilization
        6. Decorative elements
        7. Mood/Atmosphere
        
        Format your response as comma-separated tags.
        Each tag should be specific and no more than 20 words.
        """,
        2: """
        You are a product detail analyzer.
        Please analyze the image and provide detailed tags for:
        1. Material details
        2. Design features
        3. Surface texture
        4. Color variations
        5. Functional elements
        6. Quality indicators
        7. Unique characteristics
        
        Format your response as comma-separated tags.
        Each tag should be specific and no more than 20 words.
        """,
        3: """
        You are a kettle interaction analyzer.
        Please analyze the image and provide detailed tags for:
        1. Handle design
        2. Grip comfort
        3. Pouring mechanism
        4. Safety features
        5. User interaction points
        6. Ergonomic elements
        7. Usage scenarios
        
        Format your response as comma-separated tags.
        Each tag should be specific and no more than 20 words.
        """
    }
    return prompts.get(prompt_index, prompts[1])  # 默认返回 prompt1

def process_new_dimension(folder_path, prompt_index, client):
    """处理文件夹中的所有图片，添加新维度标签
    
    Args:
        folder_path (str/Path): 图片文件夹路径
        prompt_index (int): 提示词索引，可选值：
            1: 房间设计分析（风格、配色、布局等）
            2: 产品细节分析（材质、设计、功能等）
            3: 水壶交互分析（手柄、倾倒、安全等）
        client (AzureOpenAI): Azure OpenAI客户端
    
    Returns:
        tuple: (results, error)
            - 成功时 results 包含处理结果列表，error 为 None
            - 失败时 results 为 None，error 包含错误信息
    """
    valid, path_or_error = FileHandler.validate_path(folder_path)
    if not valid:
        return None, path_or_error
    
    try:
        results = []
        image_files, error = FileHandler.get_image_files(folder_path)
        if error:
            return None, error
        
        tracker = ProcessTracker(len(image_files))
        
        for image_path in image_files:
            try:
                # 生成新维度标签
                new_dimension, error = deal_new_dimension(image_path, prompt_index, client)
                if error:
                    results.append({
                        "file": image_path.name,
                        "status": "error",
                        "error": error
                    })
                    continue
                
                # 保存结果
                new_text_path = image_path.parent / f"{image_path.stem}_new_dimension{prompt_index}.txt"
                success, error = FileHandler.write_text_file(new_text_path, new_dimension)
                
                if success:
                    results.append({
                        "file": image_path.name,
                        "status": "success",
                        "content": new_dimension
                    })
                else:
                    results.append({
                        "file": image_path.name,
                        "status": "error",
                        "error": error
                    })
                
            except Exception as e:
                results.append({
                    "file": image_path.name,
                    "status": "error",
                    "error": str(e)
                })
            
            tracker.update(image_path)
        
        tracker.complete()
        return results, None
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    # 测试配置
    test_folder = r".\dataset\水壶0"
    test_prompt_index = 1
    
    # 初始化客户端
    client = AzureOpenAI(
        api_key="your_key",
        azure_endpoint="your_endpoint",
        api_version="2024-02-01"
    )
    
    # 运行测试
    results, error = process_new_dimension(test_folder, test_prompt_index, client)
    if error:
        print(f"处理失败: {error}")
    else:
        for result in results:
            if result["status"] == "success":
                print(f"\n成功处理: {result['file']}")
                print(f"生成标签: {result['content']}")
            else:
                print(f"\n处理失败: {result['file']}")
                print(f"错误信息: {result['error']}")



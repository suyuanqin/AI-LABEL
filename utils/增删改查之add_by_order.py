from pathlib import Path
from .file_utils import FileHandler, ProcessTracker
import base64
from openai import AzureOpenAI
import json

def deal_new_dimension(image_path, prompt, client):
    """处理新维度标签"""
    try:
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        file_extension = Path(image_path).suffix.lower()[1:]
        mime_type = 'image/png' if file_extension == 'png' else 'image/jpeg' if file_extension in ['jpg', 'jpeg'] else None

        if not mime_type:
            return None, "不支持的图片格式"

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
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.model_dump_json(indent=2)
        data = json.loads(result)
        return data['content'].replace('\n', ''), None
    except Exception as e:
        return None, str(e)

def generate_add_prompt(origin_text, target_position):
    """生成添加标签的提示词"""
    prompt = f"""
    You are a product photography analyzer.
    Original tags: {origin_text}
    Target position: {target_position}
    Task: 
    Please analyze the image and add new detailed tags at the specified target position.
    The new tags should be related to the target position and should not repeat existing tags.
    Return the complete tag string with the new tags inserted at the target position.
    Format the response as a JSON object with a single key "content" containing the complete tag string.
    """
    return prompt

def process_add_by_order(folder_path, origin_suffix, target_position, client):
    """按顺序添加新标签"""
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
                # 读取原始标签
                origin_text_path = image_path.parent / f"{image_path.stem}{origin_suffix}.txt"
                origin_text, error = FileHandler.read_text_file(origin_text_path)
                if error:
                    results.append({
                        "file": image_path.name,
                        "status": "error",
                        "error": f"读取原始标签失败: {error}"
                    })
                    continue
                
                # 生成提示词并处理
                prompt = generate_add_prompt(origin_text, target_position)
                new_content, error = deal_new_dimension(image_path, prompt, client)
                
                if error:
                    results.append({
                        "file": image_path.name,
                        "status": "error",
                        "error": error
                    })
                    continue
                
                # 保存结果
                new_text_path = image_path.parent / f"{image_path.stem}_add_byorder.txt"
                success, error = FileHandler.write_text_file(new_text_path, new_content)
                
                if success:
                    results.append({
                        "file": image_path.name,
                        "status": "success",
                        "content": new_content
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


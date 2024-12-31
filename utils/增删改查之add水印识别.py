from pathlib import Path
from .file_utils import FileHandler, ProcessTracker
import base64
from openai import AzureOpenAI
import json

def add_watermark(image_path, prompt, client):
    """识别图片中的水印"""
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
        )
        result = response.choices[0].message.model_dump_json(indent=2)
        data = json.loads(result)
        return data['content'].replace('\n', ''), None
    except Exception as e:
        return None, str(e)

def process_watermark(folder_path, client):
    """处理文件夹中的所有图片，添加水印识别结果"""
    valid, path_or_error = FileHandler.validate_path(folder_path)
    if not valid:
        return None, path_or_error
    
    try:
        results = []
        image_files, error = FileHandler.get_image_files(folder_path)
        if error:
            return None, error
        
        tracker = ProcessTracker(len(image_files))
        prompt = """
        You are a watermark detection expert.
        Please identify if there is a watermark in the image.
        If there is a watermark or other text, please describe the watermark or text and the position of the watermark or text.
        If there is no watermark or other text, please respond with "No watermark or text detected".
        """
        
        for image_path in image_files:
            try:
                # 识别水印
                watermark, error = add_watermark(image_path, prompt, client)
                if error:
                    results.append({
                        "file": image_path.name,
                        "status": "error",
                        "error": error
                    })
                    continue
                
                # 读取原始标签（如果存在）
                txt_path = image_path.with_suffix('.txt')
                content, error = FileHandler.read_text_file(txt_path, "")
                if error:
                    content = ""
                
                # 保存结果
                new_content = content + "\n" + watermark if content else watermark
                success, error = FileHandler.write_text_file(
                    image_path.parent / f"{image_path.stem}_watermark.txt",
                    new_content
                )
                
                if success:
                    results.append({
                        "file": image_path.name,
                        "status": "success",
                        "watermark": watermark
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

# 如果直接运行此文件
if __name__ == "__main__":
    path = r"D:\lprojects\AI标签\打标\A多巴胺卧室"
    results = process_watermark(path)
    for result in results:
        if result["status"] == "success":
            print(f"已处理: {result['file']}")
        else:
            print(f"处理失败: {result['file']} - {result['error']}")

                                      


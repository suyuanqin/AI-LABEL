import os
path=r".\dataset\水壶"
folders=os.listdir(path)
# for folder in folders:
#     folder_path=os.path.join(path,folder)   
#     print(folder_path)

from PIL import Image
##这个函数可以不用了
def otherformat2jpg(image_path):
    # 支持的图片格式列表
    supported_formats = [ 'webp', 'bmp', 'gif', 'tiff','png']
    
    # 获取文件扩展名（不含点号，小写）
    file_extension = os.path.splitext(image_path)[1].lower()[1:]
    
    # 如果是jpg/jpeg格式，直接返回
    if file_extension in ['jpg', 'jpeg']:
        return image_path
    
    # 如果是支持的格式，转换为jpg
    if file_extension in supported_formats:
        try:
            # 打开图片
            img = Image.open(image_path)
            
            # 如果图片模式不是RGB，转换为RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 构建新的文件路径
            new_path = os.path.join(file_extension, os.path.splitext(os.path.basename(image_path))[0] + '.jpg')    
            
            # 保存为jpg格式
            img.save(new_path, 'JPEG', quality=95)
            
            # 关闭图片
            img.close()
            
            print(f"Converted {image_path} to {new_path}")
            return new_path
            
        except Exception as e:
            print(f"Error converting {image_path}: {str(e)}")
            return image_path
    
    return new_path#这个可以不用返回，img.save那一步就已经把转换后的图像保存了




def all_rename_image(root_path, status_placeholder):
    status_text = ""  # 初始化状态文本
    for folderpath, subfolders, files in os.walk(root_path):
        if files:
            for file in files:
                if file.endswith((".png", "gif", "webp", "jfif")):
                    try:
                        # 打开原图片
                        img_path = os.path.join(folderpath, file)
                        img = Image.open(img_path)
                        
                        # 转换为RGB模式
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                            
                        # 构建新文件路径
                        file_name = os.path.splitext(file)[0]
                        new_path = os.path.join(folderpath, f"{file_name}.jpg")
                        
                        # 保存为jpg格式
                        img.save(new_path, 'JPEG', quality=95)
                        
                        # 关闭并删除原图片
                        img.close()
                        os.remove(img_path)
                        
                        status_text += f"已转换 {file} 为jpg格式\n"
                        status_placeholder.text(status_text)
                        
                    except Exception as e:
                        status_text += f"转换 {file} 失败: {str(e)}\n"
                        status_placeholder.text(status_text)


# for folderpath,subfolders,files in os.walk(path):
#     if files:
#         for file in files:
#             if file.endswith((".jpg",".png")):
#                 image_path=os.path.join(folderpath,file)
#                 otherformat2jpg(image_path) 

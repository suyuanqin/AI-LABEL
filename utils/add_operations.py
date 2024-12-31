from pathlib import Path
from .file_utils import FileHandler, ProcessTracker

def add_new_dimension(folder_path, new_tags):
    """添加新维度标签"""
    valid, path_or_error = FileHandler.validate_path(folder_path)
    if not valid:
        return None, path_or_error
    
    try:
        modified_files = []
        tags_list = [tag.strip() for tag in new_tags.split('\n') if tag.strip()]
        
        # 获取所有txt文件
        txt_files = list(Path(folder_path).glob('*.txt'))
        tracker = ProcessTracker(len(txt_files))
        
        for file_path in txt_files:
            content, error = FileHandler.read_text_file(file_path)
            if error:
                continue
                
            # 添加新维度标签
            new_content = content + "," + ",".join(tags_list)
            success, error = FileHandler.write_text_file(file_path, new_content)
            
            if success:
                modified_files.append(file_path.name)
            
            tracker.update(file_path)
        
        tracker.complete()
        return modified_files, None
    except Exception as e:
        return None, str(e)

def add_folder_tag(folder_path, tag):
    """按文件夹添加标签"""
    valid, path_or_error = FileHandler.validate_path(folder_path)
    if not valid:
        return None, path_or_error
    
    try:
        modified_files = []
        txt_files = list(Path(folder_path).glob('*.txt'))
        tracker = ProcessTracker(len(txt_files))
        
        for file_path in txt_files:
            content, error = FileHandler.read_text_file(file_path)
            if error:
                continue
            
            # 添加新标签
            new_content = content + "," + tag if content else tag
            success, error = FileHandler.write_text_file(file_path, new_content)
            
            if success:
                modified_files.append(file_path.name)
            
            tracker.update(file_path)
        
        tracker.complete()
        return modified_files, None
    except Exception as e:
        return None, str(e) 
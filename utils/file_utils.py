import os
from pathlib import Path
import streamlit as st

class FileHandler:
    @staticmethod
    def validate_path(path):
        """验证路径是否有效"""
        try:
            path = Path(path)
            if not path.exists():
                return False, "路径不存在"
            return True, path
        except Exception as e:
            return False, f"路径无效: {str(e)}"
    
    @staticmethod
    def ensure_dir(path):
        """确保目录存在"""
        try:
            path = Path(path)
            path.mkdir(parents=True, exist_ok=True)
            return True, path
        except Exception as e:
            return False, f"创建目录失败: {str(e)}"
    
    @staticmethod
    def get_image_files(folder_path):
        """获取文件夹中的所有图片文件"""
        try:
            path = Path(folder_path)
            image_files = []
            for file in path.rglob("*"):
                if file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    image_files.append(file)
            return image_files, None
        except Exception as e:
            return None, f"获取图片文件失败: {str(e)}"
    
    @staticmethod
    def read_text_file(file_path, default=""):
        """读取文本文件，如果文件不存在返回默认值"""
        try:
            path = Path(file_path)
            if not path.exists():
                return default, None
            with open(path, 'r', encoding='utf-8') as f:
                return f.read().strip(), None
        except Exception as e:
            return None, f"读取文件失败: {str(e)}"
    
    @staticmethod
    def write_text_file(file_path, content):
        """写入文本文件"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, None
        except Exception as e:
            return False, f"写入文件失败: {str(e)}"

class ProcessTracker:
    def __init__(self, total_files):
        self.progress_bar = st.progress(0)
        self.status_text = st.empty()
        self.total_files = total_files
        self.processed = 0
    
    def update(self, current_file):
        """更新处理进度"""
        self.processed += 1
        progress = self.processed / self.total_files
        self.progress_bar.progress(progress)
        self.status_text.text(f"正在处理: {current_file.name} ({self.processed}/{self.total_files})")
    
    def complete(self):
        """完成处理"""
        self.status_text.text("处理完成！") 
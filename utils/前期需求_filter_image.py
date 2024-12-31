from PIL import Image
import os


#####因为太小的图片硬放大的话会模糊，不如直接在comfyui里面用原图放大
#####所以更改为小于400*400的图片放到“弃用”文件夹里面
path="D:\lprojects\AI_npc\场景"
dump_path=os.path.join(path,"弃用")
# Ensure the dump_path directory exists
os.makedirs(dump_path, exist_ok=True)

def judge_remove_image(image_path,dump_path):
    with Image.open(image_path) as img:
        width, height = img.size
        if width < 400 or height < 400:
            img.save(os.path.join(dump_path, os.path.basename(image_path)))
            print(f"已将{os.path.basename(image_path)}移至弃用文件夹")
            os.remove(image_path)
            print(f"已删除{os.path.basename(image_path)}")
            return True
        else:
            return False


for file in os.listdir(path):
    if file.endswith((".png","jpg","jpeg")):
        judge_remove_image(os.path.join(path, file))   

#把首次打标的prompt归类

#增删改的prompt分成3类。用类来调用generate_prompt函数

import os
import base64
from PIL import Image
from io import BytesIO

path_jpg=r"D:\lprojects\AI标签\试验\111.jpg"
path_png=r"D:\lprojects\AI标签\试验\1111.png"
###方法一用Image.open
# image_jpg = Image.open(path_jpg)
# image_png = Image.open(path_png)

# # Convert images to bytes
# buffer_jpg = BytesIO()
# buffer_png = BytesIO()

# # Convert RGBA to RGB if needed
# if image_jpg.mode == 'RGBA':
#     image_jpg = image_jpg.convert('RGB')
# image_jpg.save(buffer_jpg, format="JPEG")
# image_png.save(buffer_png, format="PNG")

# # Encode to base64
# image_jpg_base64 = base64.b64encode(buffer_jpg.getvalue()).decode("utf-8")
# image_png_base64 = base64.b64encode(buffer_png.getvalue()).decode("utf-8")

# print(image_jpg_base64)

###方法二，用with open
with open(path_jpg, "rb") as file:
    image_jpg_base64 = base64.b64encode(file.read()).decode("utf-8")

with open(path_png, "rb") as file:
    image_png_base64 = base64.b64encode(file.read()).decode("utf-8")

print(image_jpg_base64)
print(image_png_base64)
import os

files=['a.txt','b.txt','c.txt']
jpg_files=['a.jpg','b.jpg','ddddd.jpg']
for jpg in jpg_files:
    if jpg.split('.')[0] in [f.split('.')[0] for f in files]:
        print(jpg)

text_folder_path=r"D:\lprojects\AI标签\打标\水壶000"
new_tag="场景"
index=3
file="hu (1)0.txt"
with open(os.path.join(text_folder_path, file), "r", encoding="utf-8") as f:
    content = f.read().strip()

parts = content.split(',') 

parts.insert(index, new_tag)

new_content = ','.join(parts)
print(content,"\n",parts,"\n","---------------------------",new_content)

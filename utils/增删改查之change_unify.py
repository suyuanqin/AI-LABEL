from PIL import Image
import os
from openai import AzureOpenAI
import base64
import json

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# ***可运行的GPT4o***
# # Setting up the deployment name
deployment_name = "gpt-4"#os.environ['COMPLETIONS_MODEL']
model_name="gpt-4o"
# The API key for your Azure OpenAI resource.
api_key = "7a8b721edab840239d3c4b3eba5ffbf5"#os.environ["AZURE_OPENAI_API_KEY"]

# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
azure_endpoint ="https://bzt.openai.azure.com/"# os.environ['AZURE_OPENAI_ENDPOINT']

# Currently Chat Completion API have the following versions available: 2023-03-15-preview
api_version = "2024-02-01"#os.environ['OPENAI_API_VERSION']

client = AzureOpenAI(
  api_key=api_key,  
  azure_endpoint=azure_endpoint,
  api_version=api_version
)

def deal_new_dimension(image_path,prompt):
    image_base64=encode_image(image_path)
    file_extension = os.path.splitext(image_path)[1].lower()[1:]  # 去除点号并转换为小写

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
        print("不支持的图片格式")

    response = client.chat.completions.create(
        model=model_name, # model = "deployment_name"
        messages= messages,
    )
    result=response.choices[0].message.model_dump_json(indent=2)
    data = json.loads(result)
    new_dimension = data['content'].replace('\n', '')

    return new_dimension


def call_generate_change_function(prompt_index):
    function_name = f"generate_change_prompt{prompt_index}"  # 动态构建函数名
    if function_name in globals():  # 检查函数是否存在
        return globals()[function_name]
    else:
        return f"Function {function_name} not found!"



##将主产品视角的标签统一成指定的词汇
def generate_change_prompt4(origin_text):
    main_product = "Kettle"
    perspective_terms = ["eye-level view", "side view", "top-down view", "top view"]

    prompt = f"""
    You are a product photography analyzer.

    Original tags: {origin_text}
    Main product: {main_product}

    Task: 
    - Review the original tags and identify any tags related to the perspective or view of the main product (e.g., "front view", "side view", "bird's eye view").
    - Replace any perspective-related tags with one of the following standardized terms: 
      {', '.join(perspective_terms)}.
    - If no perspective-related tags are found, leave the original tags unchanged.
    
    Please provide the updated tags with the replacements made.
    """
    return prompt

def generate_change_prompt2(origin_text):
    main_product = "Kettle"
    perspective_terms = ["eye-level view", "side view", "top-down view", "top view"]

    prompt = f"""
    You are a product photography analyzer.

    Original tags: {origin_text}
    Main product: {main_product}

    Task: 
    - Review the original tags and identify any tags related to the perspective or view of the main product (e.g., "front view", "side view", "bird's eye view").
    - Replace any perspective-related tags with one of the following standardized terms: 
      {', '.join(perspective_terms)}.
    - If no perspective-related tags are found, leave the original tags unchanged.
    
    Please return only the updated tags, with no repetition of the original tags. 
    """
    return prompt


def insert_new_dimension(root_path,prompt_index):
    for folderpath,subfolders,files in os.walk(root_path):
        if files:
            for file in files:
                if file.endswith((".jpg",".png")):
                    file_name,file_ext=os.path.splitext(file)
                    image_path=os.path.join(folderpath,file)
                    origin_text_path=os.path.join(folderpath,file_name+"_new_dimension4.txt")
                    with open(origin_text_path,"r",encoding="utf-8") as f:
                        origin_text=f.read()
                    function_name=call_generate_change_function(prompt_index)
                    prompt=function_name(origin_text)
                    new_dimension=deal_new_dimension(image_path,prompt)
                    new_text=new_dimension
                    new_text_path=os.path.join(folderpath,file_name+f"_change_dimension{prompt_index}.txt")
                    with open(new_text_path,"w",encoding="utf-8") as f:
                        f.write(new_text)
                    print(f"已处理新维度: {file}")  


root_path=r".\dataset\水壶"
insert_new_dimension(root_path,4)



import os
import base64
from openai import AzureOpenAI
import streamlit as st

# print(os.environ["AZURE_OPENAI_API_KEY"])
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

@st.cache_resource
def get_client():
    try:
        deployment_name = "gpt-4"
        model_name = "gpt-4o"
        api_key = st.secrets["AZURE_OPENAI_API_KEY"] if "AZURE_OPENAI_API_KEY" in st.secrets else os.environ["AZURE_OPENAI_API_KEY"]
        
        azure_endpoint = "https://bzt.openai.azure.com/"
        api_version = "2024-02-01"
        
        return AzureOpenAI(
            api_key=api_key,  
            azure_endpoint=azure_endpoint,
            api_version=api_version
        )
    except (KeyError, FileNotFoundError):
        st.error("请在 .streamlit/secrets.toml 或 .env 文件中配置 AZURE_OPENAI_API_KEY")
        st.stop()
    except Exception as e:
        st.error(f"创建Azure OpenAI客户端时出错: {str(e)}")
        st.stop() 

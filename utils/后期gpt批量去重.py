#version 0627-2
from PIL import Image
import os
from openai import AzureOpenAI


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



def deduplicate_phrases(text):
    # Split the text by commas and strip whitespace
    phrases = [phrase.strip() for phrase in text.split(',')]
    # Use a set to remove duplicates while preserving order
    unique_phrases = list(dict.fromkeys(phrases))
    # Join the unique phrases back into a string
    return ', '.join(unique_phrases)

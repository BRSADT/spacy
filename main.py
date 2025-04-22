from promptParser.spacyParser import SpacyPromptParser
from promptParser.spacyParser_llm import SpacyLLMPromptParser
from renderer.matplot import MatplotlibChartRenderer


import torch
print("CUDA available:", torch.cuda.is_available())
print("CUDA version:", torch.version.cuda)
print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU")


#prompt_parser = SpacyPromptParser()
prompt_parser = SpacyLLMPromptParser()
renderer = MatplotlibChartRenderer()

prompt = """
Make a pie chart with 30 cats and 70 dogs.
"""
result = prompt_parser.parse(prompt)

renderer.render(result["chart_type"], result["data"])


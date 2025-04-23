from promptParser.spacyParser import SpacyPromptParser
from promptParser.spacyParser_llm import SpacyLLMPromptParser
from renderer.matplot import MatplotlibChartRenderer

def prompt_func(user_prompt: str, csv_columns=None, csv_sample=None):
    csv_info = ""
    if csv_columns and csv_sample:
        csv_info = f"""
You are given a dataset with the following columns:
{csv_columns}

Here are the rows:
{csv_sample}
"""

    return user_prompt.strip() + f"""

{csv_info}


"""




import torch
print("CUDA available:", torch.cuda.is_available())
print("CUDA version:", torch.version.cuda)
print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU")



import pandas as pd



#prompt_parser = SpacyPromptParser()
prompt_parser = SpacyLLMPromptParser()
renderer = MatplotlibChartRenderer()

"""
df = pd.read_csv("C:\\Users\\PC\\Desktop\\Nueva_carpeta\\spacy_test\\app_usage.csv")
llm_prompt = prompt_func(
    "Show me a pie chart of app usage.",
    csv_columns=df.columns.tolist(),
    csv_sample=df.values.tolist()
)
"""

"""
df = pd.read_csv("C:\\Users\\PC\\Desktop\\Nueva_carpeta\\spacy_test\\monthly_sales.csv")
llm_prompt = prompt_func(
    "Generate a line chart showing sales over each month of the year.",
    csv_columns=df.columns.tolist(),
    csv_sample=df.values.tolist()
)
"""

"""
df = pd.read_csv("C:\\Users\\PC\\Desktop\\Nueva_carpeta\\spacy_test\\movie_ratings.csv")
llm_prompt = prompt_func(
    "Show a bar chart comparing the IMDb ratings of Christopher Nolan’s movies..",
    csv_columns=df.columns.tolist(),
    csv_sample=df.values.tolist()
)"""


df = pd.read_csv("C:\\Users\\PC\\Desktop\\Nueva_carpeta\\spacy_test\\product_reviews.csv")
llm_prompt = prompt_func(
    "Create a scatter plot comparing the rating and the number of reviews for each product in the catalog.",
    csv_columns=df.columns.tolist(),
    csv_sample=df.values.tolist()
)


result = prompt_parser.parse(llm_prompt)

renderer.render(result)


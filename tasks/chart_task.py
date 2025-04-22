from spacy_llm.registry import registry
import json

@registry.llm_tasks("chart_task.parse_chart_prompt.v1")
def make_chart_prompt_parser():
    def prompt_func(text):
        return text + """\n\nReturn only a valid JSON object in the following format:
        {
          "chart_type": "pie",
          "data": {
            "Cats": 30,
            "Dogs": 70
          }
        }"""

    def parse_func(response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            raise ValueError("No se pudo parsear el JSON")

    return {"prompt": prompt_func, "parse": parse_func}

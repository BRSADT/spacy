from .base import PromptParser
import torch
from tasks import chart_task
from spacy_llm.util import assemble
from spacy.language import Language
import os


class SpacyLLMPromptParser(PromptParser):
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        config_path = os.path.join(base_dir, "..\\configs\\config.cfg")
        print("Usando config:", config_path)
        self.nlp = assemble(config_path)
        print("Pipeline:", self.nlp.pipe_names)

    def parse(self, prompt: str) -> dict:

        prompt += """Your task is to analyze the above prompt and return only a valid JSON object describing a chart.

The response must follow this exact format:
{{
  "chart_type": "type_of_chart",       // e.g., "bar", "line", "pie", "scatter", etc.
  "x_label": "label for x-axis",
  "y_label": "label for y-axis",
  "x": ["Label 1", "Label 2", ...],
  "y": [Value1, Value2, ...],
  "title": "Chart title"
}}

- Only return valid JSON.
- Do not include explanations or text outside the JSON.
- If the prompt does not provide explicit values, return an empty chart with label "Undefined".
- Use an appropriate chart type inferred from the prompt context."""

        doc = self.nlp(prompt)
        llm_response = doc._.llm_reply
        try:
            import json
            parsed_output = json.loads(llm_response)
        except json.JSONDecodeError:
            raise ValueError(f"Error al decodificar JSON desde LLM: {llm_response}")

        return parsed_output

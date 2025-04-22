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

        prompt+= """

        Return only a valid JSON object in the following format:
        {
          "chart_type": "pie",
          "data": {
            "Cats": 30,
            "Dogs": 70
          }
        }"""

        doc = self.nlp(prompt)
        llm_response = doc._.llm_reply
        try:
            import json
            parsed_output = json.loads(llm_response)
        except json.JSONDecodeError:
            raise ValueError(f"Error al decodificar JSON desde LLM: {llm_response}")

        return parsed_output

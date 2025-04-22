import spacy

from .base import PromptParser


class SpacyPromptParser(PromptParser):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")

    def parse(self, prompt: str) -> dict:
        doc = self.nlp(prompt)

        chart_type = None
        data = {}
        valid_chart_types = ["pie", "bar", "line"]
        valid_verbs = ["make", "create", "add", "graph", "generate", "plot", "show"]

        for token in doc:
            if token.lemma_.lower() in valid_chart_types:
                verb = token.head
                if verb.pos_ == "VERB" and verb.lemma_.lower() in valid_verbs:
                    chart_type = token.lemma_.lower()
                    break

        for i, token in enumerate(doc):
            if token.like_num and i + 1 < len(doc):
                next_token = doc[i + 1]
                if next_token.pos_ in {"NOUN", "PROPN"}:
                    label = next_token.text.capitalize()
                    value = int(token.text)
                    data[label] = value

        if chart_type is None:
            chart_type = "bar"

        return {
            "chart_type": chart_type,
            "data": data
        }

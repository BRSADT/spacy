import spacy
import ast
from .base import PromptParser

class SpacyPromptParser(PromptParser):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.valid_chart_types = ["pie", "bar", "line", "scatter"]
        self.valid_verbs = ["make", "create", "add", "graph", "generate", "plot", "show"]

    def find_best_matching_column(self, doc, columns):
        highest_score = 0
        best_column = None
        for col in columns:
            col_doc = self.nlp(col.lower())
            score = max(doc.similarity(col_doc), col_doc.similarity(doc))
            if score > highest_score:
                highest_score = score
                best_column = col
        return best_column

    def parse(self, prompt: str) -> dict:
        lines = prompt.strip().splitlines()
        main_prompt = lines[0].strip()

        try:
            col_line_idx = next(i for i, line in enumerate(lines) if "columns" in line.lower())
            row_line_idx = next(i for i, line in enumerate(lines) if "rows" in line.lower())

            columns = ast.literal_eval(lines[col_line_idx + 1].strip())
            rows = ast.literal_eval(lines[row_line_idx + 1].strip())
        except Exception as e:
            raise ValueError(f"Could not parse columns/rows: {e}")

        doc = self.nlp(prompt)

        chart_type = "bar"
        for token in doc:
            if token.lemma_.lower() in self.valid_chart_types:
                    chart_type = token.lemma_.lower()

        noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
        x_column, y_column = None, None
        for col in columns:
            col_lower = col.lower()
            if any(col_lower in chunk for chunk in noun_chunks):
                if not x_column:
                    x_column = col
                elif not y_column and col != x_column:
                    y_column = col

        if not x_column:
            x_column = self.find_best_matching_column(doc, columns)
        if not y_column:
            remaining = [col for col in columns if col != x_column]
            y_column = self.find_best_matching_column(doc, remaining)

        x_index = columns.index(x_column)
        y_index = columns.index(y_column)

        x = [row[x_index] for row in rows]
        y = [row[y_index] for row in rows]

        labels = None
        if any("product" in col.lower() for col in columns):
            label_index = next((i for i, col in enumerate(columns) if "product" in col.lower()), None)
            if label_index is not None:
                labels = [row[label_index] for row in rows]

        return {
            "chart_type": chart_type,
            "x_label": x_column,
            "y_label": y_column,
            "x": x,
            "y": y,
            "labels": labels,
            "title": main_prompt
        }

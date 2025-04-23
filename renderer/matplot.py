import matplotlib.pyplot as plt


class MatplotlibChartRenderer:
    """Renders structured data into charts using matplotlib."""

    def render(self, chart_data: dict):
        chart_type = chart_data.get("chart_type", "bar")
        x = chart_data.get("x", [])
        y = chart_data.get("y", [])
        x_label = chart_data.get("x_label", "")
        y_label = chart_data.get("y_label", "")
        title = chart_data.get("title", "Chart")

        if not x or not y:
            raise ValueError("Missing 'x' or 'y' data.")

        plt.figure(figsize=(8, 5))
        if chart_type == "pie":
            if len(x) != len(y):
                raise ValueError("Length of labels and values must match for pie chart.")
            plt.pie(y, labels=x, autopct='%1.1f%%')
        elif chart_type == "bar":
            plt.bar(x, y)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
        elif chart_type == "line":
            plt.plot(x, y, marker='o')
            plt.xlabel(x_label)
            plt.ylabel(y_label)
        elif chart_type == "scatter":
            plt.scatter(x, y)
            plt.xlabel(x_label)
            plt.ylabel(y_label)

        else:
            raise ValueError(f"Invalid chart type: {chart_type}")

        plt.title(title)
        plt.tight_layout()
        plt.show()

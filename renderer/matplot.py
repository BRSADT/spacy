import matplotlib.pyplot as plt
class MatplotlibChartRenderer:
    """Renders structured data into charts using matplotlib."""

    def render(self, chart_type: str, data: dict):

        labels = list(data.keys())
        values = list(data.values())

        if chart_type == "pie":
            plt.pie(values, labels=labels, autopct='%1.1f%%')
            plt.title("Pie Chart")
        elif chart_type == "bar":
            plt.bar(labels, values)
            plt.title("Bar Chart")
        elif chart_type == "line":
            plt.plot(labels, values, marker='o')
            plt.title("Line Chart")
        else:
            raise ValueError("Invalid chart type.")

        plt.tight_layout()
        plt.show()
import logfire
from render_sdk import Workflows

app = Workflows()


@app.task
async def calculate_sum(a: int, b: int) -> int:
    with logfire.span("calculate_sum"):
        logfire.info("Calculating sum", a=a, b=b)
        result = a + b
        logfire.info("Sum calculated", result=result)
        return result


@app.task
async def calculate_square(a: int) -> int:
    return a * a

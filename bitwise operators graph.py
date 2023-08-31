import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def func(x, y):
    operations = {
        "AND": x & y,
        "OR": x | y,
        "XOR": x ^ y,
        "NAND": ~(x & y),
        "NOR": ~(x | y),
        "XNOR": ~(x ^ y),
    }
    return operations["AND"]


def calc_coords(x: int, y: int):
    return np.fromfunction(func, (x, y), dtype=int)


def draw(max_power: int):
    fig = px.imshow(
        calc_coords(2 ** max_power + 1, 2 ** max_power + 1),
        text_auto=(max_power < 6))
    fig.show()


def draw_surface(max_power: int):
    fig = go.Figure(
        data=[go.Surface(z=calc_coords(2 ** max_power + 1, 2 ** max_power + 1))]
    )
    fig.show()


if __name__ == "__main__":
    n = 5
    draw(n)

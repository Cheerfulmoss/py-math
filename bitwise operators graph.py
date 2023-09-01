"""
Visualise logic functions
Alexander Burow - 2 September 2023

License: GPL3

There is no error checking.
"""

import plotly.express as px
import plotly.graph_objects as go
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
    return operations["XOR"]


def calc_coords(x: int, y: int):
    return np.fromfunction(func, (x, y), dtype=int)


def draw(max_power: int):
    fig = px.imshow(
        calc_coords(2 ** max_power, 2 ** max_power),
        text_auto=(max_power < 6))
    fig.show()


def draw_surface(max_power: int):
    fig = go.Figure(
        data=[go.Surface(z=calc_coords(2 ** max_power, 2 ** max_power))]
    )
    fig.show()


if __name__ == "__main__":
    n = 5
    draw(n)
    draw_surface(n)

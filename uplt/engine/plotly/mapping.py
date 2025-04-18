from uplt.interface import LineStyle, MarkerStyle
from typing import Literal


LINE_STYLE_MAPPING: dict[LineStyle | Literal[''] | None, str | None] = {
    '-' : 'solid',
    '--': 'dash',
    ':' : 'dot',
    '-.': 'dashdot',
    ''  : None,
    ' ' : ' ',
    None: None,
}

MARKER_STYLE_MAPPING: dict[MarkerStyle | None, str | None] = {
    '.': 'circle',
    ',': None,
    'o': 'circle-open',
    'v': 'triangle-down',
    '^': 'triangle-up',
    '<': 'triangle-left',
    '>': 'triangle-right',
    '1': 'y-down',
    '2': 'y-up',
    '3': 'y-left',
    '4': 'y-right',
    '8': 'octagon',
    's': 'square',
    'p': 'pentagon',
    '*': 'star',
    'h': 'hexagon',
    'H': 'hexagon2',
    '+': 'cross-thin',
    'x': 'x-thin',
    'X': 'x',
    'D': 'diamond',
    'd': 'diamond-tall',
    '|': 'line-ns',
    '_': 'line-ew',
    'P': 'cross',
    None: None,
}

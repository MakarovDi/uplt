import numpy as np
from typing import Literal, cast

from uplt.interface import AxisScale


def get_scale(figure, axis: Literal['x', 'y', 'z']) -> AxisScale:
    axis_key = { 'x': 'xaxis', 'y': 'yaxis' }[axis]
    axis_type = getattr(getattr(figure.layout, axis_key), 'type', 'linear')
    axis_type = cast(AxisScale, axis_type)
    return axis_type


def set_scale(figure, axis: Literal['x', 'y'], scale: AxisScale, base: float):
    if axis == 'x':
        update_axes = figure.update_xaxes
    elif axis == 'y':
        update_axes = figure.update_yaxes
    else:
        raise ValueError(f'unsupported axis: {axis}')

    update_axes(type=scale)
    if scale == 'log':
        update_axes(dtick=np.log10(base))
    elif scale == 'linear':
        update_axes(dtick=None)
    else:
        raise ValueError(f'unsupported scale: {scale}')

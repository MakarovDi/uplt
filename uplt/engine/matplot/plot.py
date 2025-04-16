import numpy as np
from numpy.typing import ArrayLike

import uplt.color as ucolor

from uplt.interface import LineStyle, MarkerStyle
from uplt.default import DEFAULT


def plot_line_marker(axis,
                     color       : str | list[str],
                     x           : ArrayLike,
                     y           : ArrayLike | None = None,
                     z           : ArrayLike | None = None,
                     name        : str | None = None,
                     line_style  : LineStyle | list[LineStyle] | None = None,
                     marker_style: MarkerStyle | list[MarkerStyle] | None = None,
                     marker_size : float | None = None,
                     opacity     : float = 1.0,
                     **kwargs):
    """
    General plot: line, line+markers, markers(scatter).
    """
    x = np.atleast_1d(np.asarray(x))

    if y is None:
        y = x
        x = np.arange(len(y))
    else:
        y = np.asarray(y)

    y = np.atleast_1d(y)

    assert x.ndim == y.ndim == 1, 'the input must be 1d arrays'
    assert len(x) == len(y), 'the length of the input arrays must be the same'

    if z is not None:
        z = np.atleast_1d(np.asarray(z))
        assert z.ndim == 1, 'the input must be 1d arrays'
        assert len(x) == len(z), 'the length of the input arrays must be the same'
        plot_data = x, y, z
    else:
        plot_data = x, y

    if marker_size is None:
        marker_size = DEFAULT.marker_size

    if isinstance(color, str):
        color = ucolor.name_to_hex(color)
    else:
        # color specified for each point (x, y)
        color = [ ucolor.name_to_hex(c) for c in color ]

    if line_style == ' ':  # only markers (scatter mode)
        axis.scatter(*plot_data,
                     color=color,
                     label=name,
                     marker=marker_style,
                     s=marker_size ** 2,
                     alpha=opacity,
                     **kwargs)
    else:
        axis.plot(*plot_data,
                  color=color,
                  label=name,
                  marker=marker_style,
                  markersize=marker_size,
                  linestyle=line_style,
                  alpha=opacity,
                  **kwargs)

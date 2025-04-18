from importlib.metadata import metadata

# engine managing
import uplt.engine as engine

# interface
from uplt.interface import IFigure, IPlotEngine

# main API function
from uplt.plot import figure

# common routines
import uplt.color as color

# common types
from uplt.utype import LineStyle, MarkerStyle, AspectMode, AxisScale, Colormap

# settings
from uplt.default import DEFAULT

# query the package metadata
meta = metadata('uplt-py')

__author__ = meta['Author-email']
__email__ = meta['Author-email']
__version__ = meta['Version']
__license__ = meta['License-Expression']


__all__ = [

    # package metadata

    "__version__",
    "__author__",
    "__email__",
    "__license__",

    # modules

    'engine',
    'color',

    # interface

    'IFigure',
    'IPlotEngine',

    # functions

    'figure',

    # types

    'LineStyle',
    'MarkerStyle',
    'AspectMode',
    'AxisScale',
    'Colormap',

    # variables / constants

    'DEFAULT'
]

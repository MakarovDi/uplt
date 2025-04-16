from uplt.engine.MatplotEngine import MatplotEngine
from uplt.engine.PlotlyEngine5 import PlotlyEngine5
from uplt.engine.manage import register, get, available


__all__ = [

    # classes

    'MatplotEngine',
    'PlotlyEngine5',

    # functions

    'register',
    'get',
    'available'
]


# register available engines


if MatplotEngine.is_available():
    # matplotlib GUI
    mpl_gui = MatplotEngine()
    register(engine=mpl_gui, name='matplotlib')
    register(engine=mpl_gui, name='mpl')

    # matplotlib without GUI (save to file only)
    mpl_no_gui = MatplotEngine(backend='agg')
    register(mpl_no_gui, name='matplotlib-nogui')
    register(mpl_no_gui, name='mpl-nogui')
    register(mpl_no_gui, name='mpl-ng')
    register(mpl_no_gui, name='mpl-io')
    register(mpl_no_gui, name='mpl-file')

if PlotlyEngine5.is_available():
    plotly5 = PlotlyEngine5()
    register(engine=plotly5, name='plotly')
    register(engine=plotly5, name='plotly5')
    register(engine=plotly5, name='pl')
    register(engine=plotly5, name='pl5')

import importlib.util
from uplt.interface import IPlotEngine, IFigure
from uplt.default import DEFAULT


class PlotlyEngine5(IPlotEngine):
    # engine specific default parameters
    FILE_RESOLUTION_SCALE = 2
    LINE_WIDTH = 2.5

    @property
    def name(self) -> str:
        return 'plotly'

    @classmethod
    def is_available(cls) -> bool:
        return importlib.util.find_spec("plotly") is not None

    @property
    def go(self):
        return self._go

    @property
    def pio(self):
        return self._pio


    def __init__(self):
        import plotly.graph_objs as go
        import plotly.io as pio

        self._pio = pio
        self._go = go

        # load style
        if DEFAULT.style.lower() == 'bmh':
            from uplt.engine.style.plotly import bmh
            self._layout_style = bmh
        else:
            raise NotImplementedError(f'style not supported for plotly: {DEFAULT.style}')

    def figure(self, width: int, aspect_ratio: float) -> IFigure:
        from uplt.engine.PlotlyFigure5 import PlotlyFigure5

        fig = PlotlyFigure5(self)

        # adjust style layout
        fig.internal.update_layout(template=self._layout_style,
                                   width=width,
                                   height=aspect_ratio*width)

        return fig

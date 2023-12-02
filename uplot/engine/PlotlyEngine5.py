from uplot.interface import IPlotEngine, IFigure


class PlotlyEngine5(IPlotEngine):
    FILE_RESOLUTION_SCALE = 2
    MARKER_SIZE = 8
    LINE_WIDTH = 2.5

    @property
    def name(self) -> str:
        return 'plotly5'

    @classmethod
    def is_available(cls) -> bool:
        try:
            import plotly
            return True
        except ImportError:
            return False

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
        from uplot.engine.style.plotly import bmh
        self._layout_style = bmh

    def figure(self, width: int, aspect_ratio: float) -> IFigure:
        from uplot.engine.PlotlyFigure5 import PlotlyFigure5

        fig = PlotlyFigure5(self)

        # adjust style layout
        fig.internal.update_layout(template=self._layout_style,
                                   width=width,
                                   height=aspect_ratio*width)

        return fig
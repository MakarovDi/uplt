import importlib.util
from uplt.interface import IPlotEngine, IFigure


class MatplotEngine(IPlotEngine):
    # automatically (default) chosen matplotlib backend
    AUTOMATIC_MPL_BACKEND: str | None = None

    @property
    def name(self) -> str:
        return f'matplotlib-{self._backend.title().lower()}'

    @classmethod
    def is_available(cls) -> bool:
        return importlib.util.find_spec("matplotlib") is not None

    @property
    def plt(self):
        return self._plt

    @property
    def mpl(self):
        return self._mpl

    @property
    def is_ipython_backend(self) -> bool:
       return ('inline' in self.mpl.get_backend() or
               'ipympl' in self.mpl.get_backend())

    @property
    def is_gui_backend(self) -> bool:
        return not self.is_ipython_backend and self.mpl.get_backend() != 'agg'


    # noinspection PyPackageRequirements
    def __init__(self, backend: str | None = None):
        import matplotlib as mpl
        from matplotlib import pyplot as plt

        self._mpl = mpl
        self._plt = plt

        if self.AUTOMATIC_MPL_BACKEND is None:
            # save default matplotlib backend for future use
            self.AUTOMATIC_MPL_BACKEND = mpl.get_backend()

        if backend is None:
            backend = self.AUTOMATIC_MPL_BACKEND

        self._backend = backend

    def figure(self, width: int, aspect_ratio: float) -> IFigure:
        from uplt.engine.MatplotFigure import MatplotFigure

        # use style and backend for our figure only
        # avoid to change global state of matplotlib
        current_backend = self._mpl.get_backend()
        self._mpl.use(backend=self._backend)
        fig = MatplotFigure(self, width=width, aspect_ratio=aspect_ratio) # type: ignore
        self._mpl.use(backend=current_backend)
        return fig

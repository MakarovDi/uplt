import uplt.engine as uengine
from uplt.interface import IFigure, IPlotEngine
from uplt.default import DEFAULT

# cache variable to store last used engine
CURRENT_ENGINE: IPlotEngine | None = None


def figure(engine      : str | IPlotEngine | None = None,
           width       : int = DEFAULT.figure_width,
           aspect_ratio: float = DEFAULT.figure_aspect_ratio) -> IFigure:
    """
    Create a new figure using the specified plotting engine or the default engine.

    Parameters
    ----------
    engine : str, IPlotEngine, or None, optional
        The plotting engine object, name, or None.
        If None, the function uses the previous or default engine.

    width : int or None, optional
        The width of the figure in pixels.

    aspect_ratio : float, optional
        The aspect ratio for the new figure. The value in the range (0, 4].

    Returns
    -------
    IFigure
        The created figure object.

    Examples
    --------
    >>> fig = figure(engine='plotly', width=800, aspect_ratio=0.6)
    >>> fig.plot(x, y, name='Data')
    >>> fig.show()

    >>> fig = figure(width=1200)
    >>> fig.scatter(x, y)
    >>> fig.show()
    """
    global CURRENT_ENGINE

    if not 0 < aspect_ratio <= 4:
        raise ValueError('Aspect ratio must be in the range (0, 4].')

    if engine is None:
        if CURRENT_ENGINE is not None:
            # use the previously used engine
            engine = CURRENT_ENGINE
        else:
            # use the first available engine
            engine = uengine.get()
            if engine is None:
                raise RuntimeError('No plotting engines are registered.')

    elif isinstance(engine, str):
        # get the engine object by name
        engine = uengine.get(engine)
        if engine is None:
            raise RuntimeError(f'Plotting engine "{engine}" is not registered.')

    return engine.figure(width=width, aspect_ratio=aspect_ratio)

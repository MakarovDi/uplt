from uplt.interface import IPlotEngine
from typing import OrderedDict


DEFAULT_ENGINES: dict[str, IPlotEngine] = OrderedDict[str, IPlotEngine]()


def available() -> dict[str, list[str]]:
    """
    Retrieve a dictionary mapping available plot engines to their registered shortcut names.

    Returns
    -------
    dict[str, list[str]]
        A mapping between plot engines and their corresponding registered names.
    """
    engine_name_mapping = {}

    for name, engine in DEFAULT_ENGINES.items():
        if engine.name not in engine_name_mapping:
            # create a list of names for the engine
            engine_name_mapping[engine.name] = []
        # add the registered name for the engine
        engine_name_mapping[engine.name].append(name)

    return engine_name_mapping


def register(engine: IPlotEngine, name: str) -> bool:
    """
    Register a plot engine object with a specified shortcut name for use in the **figure()** function.

    Parameters
    ----------
    engine : IPlotEngine
        The plot engine object to register.

    name : str
        The shortcut name for the engine.

    Returns
    -------
    bool
        Returns True if the registration is successful.
        Returns False if the engine is unavailable or the name is already occupied.
    """
    name = name.lower()

    if name in DEFAULT_ENGINES:
        return False

    if not engine.is_available():
        return False

    DEFAULT_ENGINES[name] = engine
    return True


def get(name: str | None = None) -> IPlotEngine | None:
    """
    Retrieve a registered plot engine object by its specified name.

    Parameters
    ----------
    name : str or None, optional
        The name of the plot engine. If None, the first registered engine will be returned.

    Returns
    -------
    IPlotEngine or None
        The plot engine object corresponding to the specified name, or None if not found.
    """
    if len(DEFAULT_ENGINES) == 0:
        raise RuntimeError('No plotting engines are registered.')

    if name is None:
        # return the first available engine
        return list(DEFAULT_ENGINES.values())[0]

    engine = DEFAULT_ENGINES.get(name.lower())
    return engine

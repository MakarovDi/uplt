from abc import abstractmethod as abstract
from typing import Any, NamedTuple, Sequence, Callable, Literal
from typing import cast, get_args
from types import GenericAlias
from numpy.typing import ArrayLike

import uplt.plugin as plugin


class PlotData(NamedTuple):
    """
    Structure to hold plotting data.
    """
    x: ArrayLike
    y: ArrayLike
    z: ArrayLike | None = None
    name: str | None = None
    group_name: str | None = None


PlotType = Literal['plot', 'scatter', 'surface3d']


class IPlotPlugin:
    """
    Plugin interface to support plotting of custom objects
    """

    @abstract
    def extract_data(self, obj: Any) -> list[PlotData]:
        """
        Extract plotting data (x,y,z) from the object.
        This function must be implemented for minimal object plotting support.
        To add more advanced support (style adjustment), implement `update_style` function.

        Parameters
        ----------
        obj:
            The object for data extraction.

        Returns
        -------
        list[PlotData]
            List of extracted data from the object.
        """
        pass


    def update_style(self, plot_type : PlotType,
                           data_index: int,
                           data_count: int,
                           data_name : str | None,
                           group_name: str | None,
                           **kwargs) -> dict:
        """
        Fine-tunes plotting of the custom object.

        Parameters
        ----------
        plot_type:
            Plotting type.

        data_index:
            Index of the data in list[PlotData], see extract_data.

        data_count:
            Size of list[PlotData], see extract_data.

        data_name:
            Name of the data.

        group_name:
            Name of the data group (interpretation depends on plugin).

        kwargs:
            Current plotting style.
            Style parameters depend on plot_type.

        Returns
        -------
        dict
            Updated style (kwargs).
        """
        if data_name is not None:
            kwargs['name'] = data_name

        return kwargs


def plot(plot_method: Callable,
         x          : ArrayLike | Any,
         y          : ArrayLike | None = None,
         z          : ArrayLike | None = None,
         **kwargs) -> bool:
    """
    Returns True if x is recognized as a custom type with an associated plugin.
    In this case, the data will be automatically extracted from the object and visualized.
    No further actions are needed.
    Otherwise, returns False, and x, y, z are regular arrays.
    """
    # check if x is a custom object or regular arrays
    x_type = get_type(x)
    if y is not None or z is not None:
        return False

    if not plugin.is_registered(x_type):
        return False

    # get registered plugin for x
    handler = plugin.get_handler(x_type)
    assert handler is not None, f'plugin for {x_type} is not registered'

    # extract x,y,z from the object
    data_list = handler.extract_data(x)

    # plot all extracted data
    for i, data in enumerate(data_list):
        plot_method_name = plot_method.__name__
        assert plot_method.__name__ in get_args(PlotType), f'unsupported plot method: {plot_method.__name__}'

        params = handler.update_style(plot_type=cast(PlotType, plot_method_name),
                                      data_index=i,
                                      data_count=len(data_list),
                                      data_name=data.name,
                                      group_name=data.group_name,
                                      **kwargs)
        plot_method(x=data.x, y=data.y, z=data.z, **params)

    return True


def get_type(obj: Any) -> type | GenericAlias:
    """
    Extended version of the type() function.

    This function detects and returns the type of the given object.
    It can also identify GenericAlias for homogeneous arrays, such as list[int] or tuple[float, ...].
    """
    obj_type = type(obj)

    if obj_type is str:
        return str

    if not issubclass(obj_type, Sequence) or len(obj) == 0:
        return obj_type

    item0_type = type(obj[0])
    is_homogeneous = all([type(i) is item0_type for i in obj])

    if not is_homogeneous:
        return obj_type

    if obj_type is list:
        # homogeneous list
        return GenericAlias(list, item0_type)
    elif obj_type is tuple:
        # homogeneous tuple
        return GenericAlias(tuple, (item0_type, ...))
    else:
        raise NotImplementedError(obj_type)

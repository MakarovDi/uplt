import numpy as np
from typing import Literal


Interpolator = Literal[
    'nearest',
    'linear',
    'cubic',
]


def array_to_grid(x: np.ndarray,
                  y: np.ndarray,
                  z: np.ndarray,
                  interpolation: Interpolator,
                  interpolation_range: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert an array of non-uniformly distributed points to a uniformly interpolated grid.

    parameters
    ----------
    x, y : np.ndarray
        1D arrays of coordinates.
    z : np.ndarray
        1D array of corresponding values for (x, y).
    interpolation : Interpolator
        Interpolation method to be used ('nearest', 'linear', or 'cubic').
    interpolation_range : int
        Number of points for creating the uniform grid.

    returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        x, y, z - 2D arrays representing uniform grid coordinates and a 2D array of corresponding values.
    """
    assert len(x) == len(y) == len(z), 'sizes of x, y, z must match'
    from scipy.interpolate import griddata

    # create a uniform grid based on the specified interpolation range
    x_range = np.linspace(x.min(), x.max(), num=interpolation_range)
    y_range = np.linspace(y.min(), y.max(), num=interpolation_range)

    # perform interpolation to obtain the uniformly distributed grid
    z = griddata((x, y), z, (x_range[None, :], y_range[:, None]), method=interpolation)
    x, y = np.meshgrid(x_range, y_range)

    return x, y, z
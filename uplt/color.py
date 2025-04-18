import numpy as np
from typing import overload
from typing import OrderedDict, Sequence


color_long_name = OrderedDict[str, str]([
    ('blue'   , '#1f77b4'),
    ('orange' , '#ff7f0e'),
    ('green'  , '#2ca02c'),
    ('red'    , '#d62728'),
    ('purple' , '#9467bd'),
    ('brown'  , '#8c564b'),
    ('magenta', '#e377c2'),
    ('gray'   , '#7f7f7f'),
    ('yellow' , '#bcbd22'),
    ('cyan'   , '#17becf'),
    ('black'  , '#000000'),
    ('white'  , '#ffffff'),
])

color_short_name = {
    'b': color_long_name['blue'],
    'g': color_long_name['green'],
    'r': color_long_name['red'],
    'c': color_long_name['cyan'],
    'm': color_long_name['magenta'],
    'y': color_long_name['yellow'],
    'k': color_long_name['black'],
    'w': color_long_name['white'],
    'o': color_long_name['orange'],
}


@overload
def name_to_hex(name: None) -> None:
    ...

@overload
def name_to_hex(name: str) -> str:
    ...

def name_to_hex(name: str | None) -> str | None:
    """
    Convert a color name to a hex string.

    Parameters
    ----------
    name : str or None
        The color name.

    Returns
    -------
    str or None
        The hex string corresponding to the color name.
    """
    if name is None:
        return None

    if len(name) == 1:
        if name not in color_short_name:
            raise LookupError(f'{name} is not a valid color name, use: {color_short_name.keys()}')
        return color_short_name[name]

    if name[0] == '#':
        return name

    if name not in color_long_name:
        raise LookupError(f'{name} is not a valid color name, use: {color_long_name.keys()}')

    return color_long_name[name]


def rgb_to_str(rgb: list | np.ndarray) -> str | list[str]:
    """
    Convert an RGB value (or array of RGB values) to a hex-string compatible with the uplot API.

    Parameters
    ----------
    rgb : list or np.ndarray
        RGB value in the [0, 1] range or an array of values (N x 3).

    Returns
    -------
    str or list[str]
        Hex color string or array of strings.
    """
    rgb = np.asarray(rgb)
    assert rgb.shape[-1] == 3, 'Input must be an Nx3 array or list'
    assert rgb.max() <= 1.0, 'RGB value range must be [0, 1]'

    rgb255 = (rgb*255).astype(np.uint8)
    rgb255 = np.atleast_2d(rgb255)
    rgb_str = [ f'#{r:02x}{g:02x}{b:02x}' for r, g, b in rgb255 ]

    if len(rgb) == 1:
        return rgb_str[0]  # single RGB value

    return rgb_str  # RGB array


class ColorScroller:
    """
    Class for maintaining automatic color switching for plotting.
    """
    DEFAULT_COLOR_LIST = (
        name_to_hex('orange'),
        name_to_hex('green'),
        name_to_hex('blue'),
        name_to_hex('red'),
        name_to_hex('purple'),
        name_to_hex('brown'),
        name_to_hex('magenta'),
        name_to_hex('gray'),
        name_to_hex('yellow'),
        name_to_hex('cyan'),
    )


    def __init__(self, color_list: Sequence[str] = DEFAULT_COLOR_LIST):
        """
        Parameters
        ----------
        color_list : list[str]
            List of color hex strings for scrolling.
        """
        self._color_list = color_list
        self._color_index = 0


    def scroll_color(self, count: int = 1) -> str:
        """
        Scroll through the color list.

        Parameters
        ----------
        count : int
            The number of colors to scroll.

        Returns
        -------
        str
            The current color before scrolling.
        """
        current = self.current_color()
        self._color_index += count
        self._color_index %= len(self._color_list)
        return current


    def current_color(self) -> str:
        """
        Return the current color.
        """
        return self._color_list[self._color_index]


    def reset(self):
        """
        Reset the scroller state to the first color in the list.
        """
        self._color_index = 0

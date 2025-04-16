from dataclasses import dataclass


@dataclass
class Default:
    figure_width       : int = 800
    figure_aspect_ratio: float = 0.6
    style              : str = 'bmh'
    marker_size        : int = 6


DEFAULT = Default()
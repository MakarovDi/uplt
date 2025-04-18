# Changelog

## `[v0.8.3]` - 18.04.2025

#### Changed
* `[interface]` update type for `IFigure.internal` to `Any | None`.


## `[v0.8.2]` - 18.04.2025

#### New
* `[engine]` add `matplot` alias for matplotlib engine.
* `uplot` and `uplt` are now aliases for the same package.

#### Changed
* change name `uplot` to available `uplt` for the package publishing.


## `[v0.8.1]` - 23.02.2025

#### Fixed
* `[engine]` extend range for `aspect_ratio` from `(0, 1]` to `(0, 4]`.



## `[v0.8.0]` - 26.01.2025

#### New
* `[interface]` add `xscale()` and `yscale()` methods.
* `[color]` add 'o' shortcut for orange color.

#### Changed
* `[interface]` change `marker_size` type from `int` to `float`.

#### Fixed
* `[engine.matplot]` replace deprecated `tostring_rgb()` with `buffer_rgba()`.



## `[v0.7.0]` - 15.12.2024

#### New
* `[interface]` bar() plot.

#### Changed
* `[engine.matplot]` imshow: disable normalization if vmin/vmax provided.
* `[ci]` update to non-vulnerable `pillow` version (>10.3).

#### Fixed
* `[engine.plotly5]` imshow: fixed issue with grayscale images.


## `[v0.6.2]` - 03.07.2024

#### Fixed
* `[engine.matplot]` update to v3.9: `get_cm -> colormaps`
* `[engine.plotly5]` range estimation with considering `xlim/ylim`

#### Changed
* numpy v2.0 support verified
* `[color]` color order updated, the first three colors are orange, green and blue now ~ RGB
* `[plugin]` new filed for PlotData: `group_name`


## `[v0.6.1]` - 09.06.2024

#### Fixed
* `[engine]` fixed returning `IFigure` for `reset_color()`
* `[engine.plotly5]` signature for `surface3d` fixed

#### Changed
* `[engine]` New extra aliases for non-GUI Matplotlib: `mpl-io`, `mpl-file`
* `[plugin]` New `force` parameter for `register()` to allow plugin replacement
* `[plugin]` plugin can be registered for homogeneous arrays like `list[T]` or `tuple[T, ...]`


## `[v0.6.0]` - 28.04.2024

#### New
* `[interface] & [engine]` functions `hline()`, `vline()`


## `[v0.5.0]` - 03.02.2024

#### New
* `[plugin]` plugin system to support custom objects plotting

#### Changed
* `[interface]` API documentation improved


## `[v0.4.0]` - 21.12.2023

#### New
* `[interface] & [engine]` parameter `legend_group` New

#### Changed
* `[interface]` return `IFigure` when possible to support chaining


## `[v0.3.1]` - 11.12.2023

#### Changed
* `[interface] & [engine]` marker size is fixed in the legend, by default
* `[interface]` API documentation

#### Fixed
* `[engine.matplot]` remove the empty legend space on `figure.legend(False)`


## `[v0.3.0]` - 06.12.2023

#### New
* `[interface]` singleton `DEFAULT` for storing and controlling default parameters.
* `[interface]` 3d surface plotting: `figure.surface3d(...)`
* `[color]` class `ColorScroller` for maintaining automatic color switching for plotting.

#### Changed
* `[engine]` the engine management system reworked: `engine.get()`, `engine.available()`, `engine.register()`.

#### Fixed
* `[engine.plotly5]` legend item width increased to show dashed line correctly.
* `[engine.matplot]` problem with `figure.close()` fixed.


## `[v0.2.1]` - 13.11.2023

#### Fixed
* `[engine.plotly5]` fixed problem with `line_style` setting.


## `[v0.2.0]` - 12.11.2023

#### New
* `[interface]` `[engine]` 3d plot & scatter.
* `[interface]` `[engine]` 3d plot support: `zlim()`, `zlabel()`.
* `[interface]` `[engine]` engine-specific parameters via `kwargs`: `plot()`, `scatter()`, `legend()`.
* `[engine]` "color per point" support for scatter.

#### Changed
* `[engine.matplot]` legend outside the plot (same as plotly legend).
* `[engine.matplot]` change from `tight_layout` to `constrained` for more predictable behavior.
* `[engine.matplot]` axis and frame disabled for `imshow()`.
* `[engine.plotly5]` fixed size of legend's markers.

#### Fixed
* `[engine.matplot]` problem with figure no-show / double-show in jupyter.
* `[engine.plotly5]` prevent name truncation (ellipsis) of a trace when hovering over.

## `[v0.1.0]` - 22.09.2023

Initial version

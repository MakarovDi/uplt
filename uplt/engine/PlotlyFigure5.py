from __future__ import annotations

import numpy as np
from numpy import ndarray
from numpy.typing import ArrayLike

import uplt.color as ucolor
import uplt.utool as utool
import uplt.plugin as plugin

from uplt.interface import IFigure
from uplt.interface import LineStyle, MarkerStyle, AspectMode, AxisScale, Colormap
from uplt.engine.PlotlyEngine5 import PlotlyEngine5
from uplt.utool import Interpolator


class PlotlyFigure5(IFigure):

    @property
    def engine(self) -> PlotlyEngine5:
        return self._engine

    @property
    def internal(self):
        return self._fig

    @property
    def is_3d(self) -> bool | None:
        return self._is_3d

    def __init__(self, engine: PlotlyEngine5):
        from plotly.graph_objs import Figure

        self._engine = engine
        self._color_scroller = ucolor.ColorScroller()

        self._fig: Figure = engine.go.Figure()
        self._is_3d = None
        self._colorbar_x_pos = 1.0
        self._show_grid = True

        self._group_counter: dict[str | None, int] = { None: 0 }


    def plot(self, x           : ArrayLike,
                   y           : ArrayLike | None = None,
                   z           : ArrayLike | None = None,
                   name        : str | None = None,
                   color       : str | None = None,
                   line_style  : LineStyle | None = None,
                   marker_style: MarkerStyle | None = None,
                   marker_size : float | None = None,
                   opacity     : float = 1.0,
                   legend_group: str | None = None,
                   **kwargs) -> IFigure:
        from uplt.engine.plotly.plot import plot_line_marker

        # check if x is a custom object and a plugin is available
        if plugin.plot(plot_method=self.plot,
                       x=x, y=y, z=z,
                       name=name,
                       color=color,
                       line_style=line_style,
                       marker_style=marker_style,
                       marker_size=marker_size,
                       opacity=opacity,
                       legend_group=legend_group,
                       **kwargs):
            return self

        self._is_3d = z is not None

        if color is None:
            color = self.scroll_color()

        self._update_group_counter(plot_name=name, legend_group=legend_group)

        plot_line_marker(figure=self._fig,
                         x=x, y=y, z=z,
                         color=color,
                         name=name,
                         line_style=line_style,
                         line_width=self.engine.LINE_WIDTH,
                         marker_style=marker_style,
                         marker_size=marker_size,
                         opacity=opacity,
                         legend_group=legend_group,
                         legend_group_title=legend_group if self._group_counter[legend_group] > 0 else None,
                         **kwargs)
        return self

    def scatter(self, x           : ArrayLike,
                      y           : ArrayLike | None = None,
                      z           : ArrayLike | None = None,
                      name        : str | None = None,
                      color       : str | list[str] | None = None,
                      marker_style: MarkerStyle | None = None,
                      marker_size : float | None = None,
                      opacity     : float = 1.0,
                      legend_group: str | None = None,
                      **kwargs) -> IFigure:
        from uplt.engine.plotly.plot import plot_line_marker

        # check if x is a custom object and a plugin is available
        if plugin.plot(plot_method=self.scatter,
                       x=x, y=y, z=z,
                       name=name,
                       color=color,
                       marker_style=marker_style,
                       marker_size=marker_size,
                       opacity=opacity,
                       legend_group=legend_group,
                       **kwargs):
            return self

        self._is_3d = z is not None

        if color is None:
            color = self.scroll_color()

        self._update_group_counter(plot_name=name, legend_group=legend_group)

        plot_line_marker(figure=self._fig,
                         x=x, y=y, z=z,
                         color=color,
                         name=name,
                         line_style=' ', # no line (scatter mode)
                         line_width=self.engine.LINE_WIDTH,
                         marker_style=marker_style,
                         marker_size=marker_size,
                         opacity=opacity,
                         legend_group=legend_group,
                         legend_group_title=legend_group if self._group_counter[legend_group] > 0 else None,
                         **kwargs)
        return self

    def hline(self, y           : float,
                    x_min       : float | None = None,
                    x_max       : float | None = None,
                    name        : str | None = None,
                    color       : str | None = None,
                    line_style  : LineStyle | None = None,
                    opacity     : float = 1.0,
                    legend_group: str | None = None,
                    **kwargs) -> IFigure:

        if self.is_3d:
            raise RuntimeError('3D figure is not supported')

        if x_min is None:
            from uplt.engine.plotly.axis_range import estimate_axis_range
            x_min = estimate_axis_range(self._fig, axis='x', mode='min')

        if x_max is None:
            from uplt.engine.plotly.axis_range import estimate_axis_range
            x_max = estimate_axis_range(self._fig, axis='x', mode='max')

        return self.plot([x_min, x_max], [y, y],
                         color=color,
                         name=name,
                         line_style=line_style,
                         opacity=opacity,
                         legend_group=legend_group,
                         **kwargs)

    def vline(self, x           : float,
                    y_min       : float | None = None,
                    y_max       : float | None = None,
                    name        : str | None = None,
                    color       : str | None = None,
                    line_style  : LineStyle | None = None,
                    opacity     : float = 1.0,
                    legend_group: str | None = None,
                    **kwargs) -> IFigure:
        if self.is_3d:
            raise RuntimeError('3D figure is not supported')

        if y_min is None:
            from uplt.engine.plotly.axis_range import estimate_axis_range
            y_min = estimate_axis_range(self._fig, axis='y', mode='min')

        if y_max is None:
            from uplt.engine.plotly.axis_range import estimate_axis_range
            y_max = estimate_axis_range(self._fig, axis='y', mode='max')

        return self.plot([x, x], [y_min, y_max],
                         color=color,
                         name=name,
                         line_style=line_style,
                         opacity=opacity,
                         legend_group=legend_group,
                         **kwargs)

    def surface3d(self, x            : ArrayLike,
                        y            : ArrayLike | None = None,
                        z            : ArrayLike | None = None,
                        name         : str | None = None,
                        show_colormap: bool = False,
                        colormap     : Colormap = 'viridis',
                        opacity      : float = 1.0,
                        interpolation: Interpolator = 'cubic',
                        interpolation_range: int = 100,
                        legend_group : str | None = None,
                        **kwargs) -> IFigure:
        # check if x is a custom object and a plugin is available
        if plugin.plot(plot_method=self.surface3d,
                       x=x, y=y, z=z,
                       name=name,
                       show_colormap=show_colormap,
                       colormap=colormap,
                       opacity=opacity,
                       interpolation=interpolation,
                       interpolation_range=interpolation_range,
                       legend_group=legend_group,
                       **kwargs):
            return self

        x = np.asarray(x)
        y = np.asarray(y)
        z = np.asarray(z)
        assert x.ndim == y.ndim == 1, 'x, y must be 1D arrays'
        assert z.ndim == 1 or z.ndim == 2, 'z must be 1D or 2D array'

        if z.ndim == 2:
            # uniform grid
            assert (len(y), len(x)) == z.shape, 'uniform grid: x and y range must match z'
            x, y = np.meshgrid(x, y)
        else:
            # non-uniform grid - array of points (x, y, z)
            x, y, z = utool.array_to_grid(x, y, z,
                                          interpolation=interpolation,
                                          interpolation_range=interpolation_range)

        self._is_3d = True

        if show_colormap:
            colorbar = dict(len=0.5, x=self._colorbar_x_pos)
            self._colorbar_x_pos += 0.12
        else:
            colorbar = None

        self._update_group_counter(plot_name=name, legend_group=legend_group)

        self._fig.add_surface(x=x, y=y, z=z,
                              name=name,
                              showlegend=(name != '') and (name is not None),
                              showscale=show_colormap,
                              colorscale=colormap,
                              colorbar=colorbar,
                              opacity=opacity,
                              legendgroup=legend_group,
                              legendgrouptitle_text=legend_group if self._group_counter[legend_group] > 0 else None,
                              **kwargs)
        return self

    def bar(self, x           : ArrayLike,
                  y           : ArrayLike | None = None,
                  name        : str | None = None,
                  color       : str | None = None,
                  opacity     : float = 1.0,
                  legend_group: str | None = None,
                  **kwargs) -> IFigure:

        self._is_3d = False

        x = np.asarray(x)
        if y is None:
            # y is provided via x
            y = x
            x = np.arange(len(y))
        else:
            y = np.asarray(y)
            assert len(x) == len(y), 'the length of the input arrays must be the same'

        if color is None:
            color = self.scroll_color()

        self._update_group_counter(plot_name=name, legend_group=legend_group)

        if name is None:
            name = ''
            show_legend = False
        else:
            show_legend = kwargs.pop('showlegend', True)

        self._fig.add_bar(x=x, y=y,
                          marker_color=ucolor.name_to_hex(color),
                          name=name,
                          showlegend=show_legend,
                          legendgroup=legend_group,
                          opacity=opacity,
                          legendgrouptitle_text=legend_group if self._group_counter[legend_group] > 0 else None,
                          **kwargs)
        return self

    def imshow(self, image: ArrayLike, **kwargs) -> IFigure:
        image = np.asarray(image)
        value_range = utool.image_range(image)

        if image.ndim == 2 or image.shape[2] == 1:
            # workaround for a grayscale image
            # https://github.com/plotly/plotly.py/issues/2885  # issuecomment-724679904
            image = np.stack([image, image, image], axis=2)

        self._is_3d = False

        self._fig.add_trace(self.engine.go.Image(
            z=image,
            zmax=kwargs.pop('zmax', [value_range]*4),
            zmin=kwargs.pop('zmin', [0]*4),
            **kwargs,
        ))

        # configure layout
        self._fig.update_layout(margin=self.engine.go.layout.Margin(b=30, t=30))
        self._fig.update_layout(hovermode='closest')
        self._fig.update_xaxes(visible=False)
        self._fig.update_yaxes(visible=False)

        return self

    def title(self, text: str) -> IFigure:
        self._fig.update_layout(title=text)
        return self

    def legend(self, show: bool = True,
                     equal_marker_size: bool = True,
                     **kwargs) -> IFigure:
        itemsizing = 'constant' if equal_marker_size else None

        self._fig.update_layout(legend=self.engine.go.layout.Legend(
            visible=show,
            bgcolor=kwargs.pop('bgcolor', 'rgba(255,255,255,0.8)'),
            itemsizing=kwargs.pop('itemsizing', itemsizing),
            itemwidth=kwargs.pop('itemwidth', 50),
            **kwargs,
        ))
        return self

    def grid(self, show: bool = True) -> IFigure:
        from uplt.engine.plotly.scale import get_scale

        show_minor_x = show and get_scale(self._fig, 'x') == 'log'
        show_minor_y = show and get_scale(self._fig, 'y') == 'log'
        if self.is_3d:
            Scene = self.engine.go.layout.Scene
            XAxis = self.engine.go.layout.scene.XAxis
            YAxis = self.engine.go.layout.scene.YAxis
            ZAxis = self.engine.go.layout.scene.ZAxis
            self._fig.update_layout(scene=Scene(xaxis=XAxis(showgrid=show),
                                                yaxis=YAxis(showgrid=show),
                                                zaxis=ZAxis(showgrid=show)))
        else:
            self._fig.update_xaxes(showgrid=show)
            self._fig.update_xaxes(minor=dict(ticks='inside' if show_minor_x else '',
                                              showgrid=show_minor_x))
            self._fig.update_yaxes(showgrid=show)
            self._fig.update_yaxes(minor=dict(ticks='inside' if show_minor_y else '',
                                              showgrid=show_minor_y))
        self._show_grid = show
        return self

    def xlabel(self, text: str) -> IFigure:
        if self.is_3d:
            self._fig.update_layout(scene=dict(xaxis_title=text))
        else:
            self._fig.update_xaxes(title=text)
        return self

    def ylabel(self, text: str) -> IFigure:
        if self.is_3d:
            self._fig.update_layout(scene=dict(yaxis_title=text))
        else:
            self._fig.update_yaxes(title=text)
        return self

    def zlabel(self, text: str) -> IFigure:
        if self.is_3d:
            self._fig.update_layout(scene=dict(zaxis_title=text))
        return self

    def xlim(self, min_value: float | None = None,
                   max_value: float | None = None) -> IFigure:
        from uplt.engine.plotly.axis_range import estimate_axis_range
        from uplt.engine.plotly.scale import get_scale

        if min_value is None:
            min_value = estimate_axis_range(self._fig, axis='x', mode='min')

        if get_scale(self._fig, 'x') == 'log':
            min_value = np.log10(min_value)

        if max_value is None:
            max_value = estimate_axis_range(self._fig, axis='x', mode='max')

        if get_scale(self._fig, 'x') == 'log':
            max_value = np.log10(max_value)

        if self.is_3d:
            self._fig.update_layout(scene=dict(xaxis=dict(range=[min_value, max_value])))
        else:
            self._fig.update_xaxes(range=[min_value, max_value])
        return self

    def ylim(self, min_value: float | None = None,
                   max_value: float | None = None) -> IFigure:
        from uplt.engine.plotly.axis_range import estimate_axis_range
        from uplt.engine.plotly.scale import get_scale

        if min_value is None:
            min_value = estimate_axis_range(self._fig, axis='y', mode='min')

        if get_scale(self._fig, 'y') == 'log':
            min_value = np.log10(min_value)

        if max_value is None:
            max_value = estimate_axis_range(self._fig, axis='y', mode='max')

        if get_scale(self._fig, 'y') == 'log':
            max_value = np.log10(max_value)

        if self.is_3d:
            self._fig.update_layout(scene=dict(yaxis=dict(range=[min_value, max_value])))
        else:
            self._fig.update_yaxes(range=[min_value, max_value])
        return self

    def zlim(self, min_value: float | None = None,
                   max_value: float | None = None) -> IFigure:
        if not self.is_3d:
            return self

        if min_value is None:
            from uplt.engine.plotly.axis_range import estimate_axis_range
            min_value = estimate_axis_range(self._fig, axis='z', mode='min')

        if max_value is None:
            from uplt.engine.plotly.axis_range import estimate_axis_range
            max_value = estimate_axis_range(self._fig, axis='z', mode='max')

        self._fig.update_layout(scene=dict(zaxis=dict(range=[min_value, max_value])))
        return self

    def xscale(self, scale: AxisScale, base: float = 10) -> IFigure:
        from uplt.engine.plotly.scale import set_scale

        set_scale(self._fig, 'x', scale=scale, base=base)
        self.grid(self._show_grid) # update grid if visible
        return self

    def yscale(self, scale: AxisScale, base: float = 10) -> IFigure:
        from uplt.engine.plotly.scale import set_scale

        set_scale(self._fig, 'y', scale=scale, base=base)
        self.grid(self._show_grid) # update grid if visible
        return self

    def current_color(self) -> str:
        return self._color_scroller.current_color()

    def scroll_color(self, count: int=1) -> str:
        return self._color_scroller.scroll_color(count)

    def reset_color(self) -> IFigure:
        self._color_scroller.reset()
        return self

    def axis_aspect(self, mode: AspectMode) -> IFigure:
        if self.is_3d:
            aspectmode = 'cube' if mode == 'equal' else 'auto'
            self._fig.update_scenes(aspectmode=aspectmode)
        else:
            scaleanchor = 'x' if mode == 'equal' else None
            self._fig.update_yaxes(scaleanchor=scaleanchor)
        return self

    def as_image(self) -> ndarray:
        import io
        from PIL import Image

        fig_bytes = io.BytesIO(
            self._fig.to_image(format='png', scale=self.engine.FILE_RESOLUTION_SCALE)
        )

        image = Image.open(fig_bytes)
        image = np.asarray(image)
        image = image[..., :3] # RGBA -> RGB
        return image

    def save(self, filename: str):
        if '.html' in filename:
            self._fig.write_html(filename)
        else:
            self._fig.write_image(filename)

    def close(self):
        self._fig.data = []
        self._fig.layout = {}

    def show(self, block: bool=True):
        self.engine.pio.show(self._fig)

    ## Protected ##

    def _update_group_counter(self, plot_name: str | None, legend_group: str | None):
        """
        Count visible legend's items for the same group
        """
        if legend_group is None or len(legend_group) == 0:
            return

        group_size = self._group_counter.get(legend_group, 0)

        if plot_name is not None and len(plot_name) > 0:
            group_size += 1

        self._group_counter[legend_group] = group_size

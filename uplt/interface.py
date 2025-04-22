from __future__ import annotations

from numpy import ndarray
from typing import Any, Protocol, runtime_checkable
from abc import abstractmethod as abstract
from numpy.typing import ArrayLike

from uplt.utype import LineStyle, MarkerStyle, AspectMode, AxisScale, Colormap
from uplt.utool import Interpolator


@runtime_checkable
class IFigure(Protocol):
    """
    Matplotlib-like interface for plotting.

    Note
    ----
    This interface follows a Matplotlib-like interface for plotting, providing a familiar
    environment for users, particularly those accustomed to MATLAB.
    It may not be the best choice, but it offers common conventions and practices.
    """

    @property
    @abstract
    def engine(self) -> IPlotEngine:
        """
        Get the underlying plotting engine associated with the figure.

        Returns
        -------
        IPlotEngine
            The plotting engine.
        """

    @property
    @abstract
    def internal(self) -> Any | None:
        """
        Access the underlying engine-specific figure object.
        Use it if you need richer functionality than uplot can provide.
        But manipulation with the internal figure may lead to undefined behavior of uplot.

        Returns
        -------
        Any
            An engine-specific figure object or None if figure is closed.
        """

    @property
    @abstract
    def is_3d(self) -> bool:
        """
        Check if the figure is set up for 3D plotting.

        Returns
        -------
        bool
            True if the figure is in 3D mode, False otherwise.
        """

    @abstract
    def plot(self, x           : ArrayLike | Any,
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
        """
        Plot 2D or 3D line.

        Parameters
        ----------
        x, y, z : ArrayLike
            1D data arrays of the same size.
            The x could be any object supported by a plugin.

        name : str or None, optional
            The plot name, which will appear as the legend item.

        color : str or None, optional
            The color of the line.

        line_style : LineStyle or None, optional
            The line style.

        marker_style : MarkerStyle or None, optional
            The marker style.

        marker_size : float or None, optional
            The size of the marker.

        opacity : float, optional
            Sets the opacity of the line(s).

        legend_group : str or None, optional
            Sets the legend group for this plot.
            Plots from the same group will be combined in the legend.

        kwargs : dict
            Other keyword arguments are forwarded to the underlying engine.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def scatter(self, x           : ArrayLike | Any,
                      y           : ArrayLike | None = None,
                      z           : ArrayLike | None = None,
                      name        : str | None = None,
                      color       : str | list[str] | None = None,
                      marker_style: MarkerStyle | None = None,
                      marker_size : float | None = None,
                      opacity     : float = 1.0,
                      legend_group: str | None = None,
                      **kwargs) -> IFigure:
        """
        Scatter plot for 2D or 3D data points.

        Parameters
        ----------
        x, y, z : ArrayLike
            1D data arrays of the same size. The x could be any object supported by a plugin.

        name : str or None, optional
            The plot name, which will appear as the legend item.

        color : str, list of str, or None, optional
            The color(s) of the markers.

        marker_style : MarkerStyle or None, optional
            The marker style.

        marker_size : float or None, optional
            The size of the markers.

        opacity : float, optional
            Sets the opacity of the markers.

        legend_group : str or None, optional
            Sets the legend group for this plot. Plots from the same group will be combined in the legend.

        kwargs : dict
            Other keyword arguments are forwarded to the underlying engine.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def hline(self, y           : float,
                    x_min       : float | None = None,
                    x_max       : float | None = None,
                    name        : str | None = None,
                    color       : str | None = None,
                    line_style  : LineStyle | None = None,
                    opacity     : float = 1.0,
                    legend_group: str | None = None,
                    **kwargs) -> IFigure:
        """
        Plot horizontal line at y.
        It supports 2d figures only.

        Parameters
        ----------
        y : float
            y coordinate where to plot the line.

        x_min, x_max : float or None, optional
            x range limit for the line, if None it will be estimated automatically.

        name : str or None, optional
            The plot name, which will appear as the legend item.

        color : str or None, optional
            The color of the line.

        line_style : LineStyle or None, optional
            The line style.

        opacity : float, optional
            Sets the opacity of the line(s).

        legend_group : str or None, optional
            Sets the legend group for this plot.
            Plots from the same group will be combined in the legend.

        kwargs : dict
            Other keyword arguments are forwarded to the underlying engine.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def vline(self, x           : float,
                    y_min       : float | None = None,
                    y_max       : float | None = None,
                    name        : str | None = None,
                    color       : str | None = None,
                    line_style  : LineStyle | None = None,
                    opacity     : float = 1.0,
                    legend_group: str | None = None,
                    **kwargs) -> IFigure:
        """
        Plot vertical line at x.
        It supports 2d figures only.

        Parameters
        ----------
        x : float
            x coordinate where to plot the line.

        y_min, y_max : float or None, optional
            y range limit for the line, if None it will be estimated automatically.

        name : str or None, optional
            The plot name, which will appear as the legend item.

        color : str or None, optional
            The color of the line.

        line_style : LineStyle or None, optional
            The line style.

        opacity : float, optional
            Sets the opacity of the line(s).

        legend_group : str or None, optional
            Sets the legend group for this plot.
            Plots from the same group will be combined in the legend.

        kwargs : dict
            Other keyword arguments are forwarded to the underlying engine.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def surface3d(self, x            : ArrayLike | Any,
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
        """
        Plot a surface in 3D space where the color scale corresponds to the z-values.
        Two coordinate formats are supported:
          - Uniform grid: x, y are 1D uniform ranges, z is a 2D array of corresponding values.
          - Non-uniform grid (set of points): x, y, z are 1D arrays of corresponding points' coordinates in 3D space.
            The non-uniform grid will be interpolated to a uniform grid using the specified **interpolator**.

        Parameters
        ----------
        x, y, z : ArrayLike
            Data values. The x could be any object supported by a plugin.

        name : str or None, optional
            The plot name, which will appear as the legend item.

        show_colormap : bool, optional
            Whether the colormap should be visualized as a bar alongside the plot.

        colormap : Colormap, optional
            A palette name string.

        opacity : float, optional
            Sets the opacity of the surface.

        interpolation : Interpolator, optional
            The interpolation method for the case when (x, y, z) is a non-uniform grid.

        interpolation_range : int, optional
            The number of points in the interpolated grid.

        legend_group : str or None, optional
            Sets the legend group for this plot. Plots from the same group will be combined in the legend.

        kwargs : dict
            Other keyword arguments are forwarded to the underlying engine.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def bar(self, x           : ArrayLike,
                  y           : ArrayLike | None = None,
                  name        : str | None = None,
                  color       : str | None = None,
                  opacity     : float = 1.0,
                  legend_group: str | None = None,
                  **kwargs) -> IFigure:
        """
        Create a bar plot using the provided data.

        Parameters
        ----------
        x : ArrayLike
            The x-coordinates of the bars. This can represent categories or numeric values.

        y : ArrayLike or None, optional
            The heights of the bars. If not provided, the values in `x` are assumed to be the heights,
            and the bars will be positioned sequentially on the x-axis.

        name : str or None, optional
            The name of the bar plot, which will appear as the legend item.

        color : str or None, optional
            The color of the bars.

        opacity : float, optional
            Sets the opacity of the bars. Default is 1.0 (fully opaque).

        legend_group : str or None, optional
            Sets the legend group for this plot. Plots from the same group will be combined in the legend.

        kwargs : dict
            Additional keyword arguments forwarded to the underlying plotting engine.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def imshow(self, image: ArrayLike, **kwargs) -> IFigure:
        """
        Display an image.

        Parameters
        ----------
        image : ArrayLike
            Image data. Supported ranges: double [0, 1], uint8, uint16.

        kwargs : dict
            Other keyword arguments are forwarded to the underlying engine.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def title(self, text: str) -> IFigure:
        """
        Set the title of the figure.

        Parameters
        ----------
        text : str
            The title text.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def legend(self, show: bool = True,
                     equal_marker_size: bool = True,
                     **kwargs) -> IFigure:
        """
        Show or hide the legend on the figure.

        Parameters
        ----------
        show : bool, optional
            Whether to show or hide the legend.

        equal_marker_size : bool, optional
            Whether markers in the legend are equal in size.

        kwargs : dict
            Other keyword arguments are forwarded to the underlying engine.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def grid(self, show: bool = True) -> IFigure:
        """
        Show or hide the grid on the figure.

        Parameters
        ----------
        show : bool, optional
            Whether to show or hide the grid.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def xlabel(self, text: str) -> IFigure:
        """
        Set the label for the x-axis.

        Parameters
        ----------
        text : str
            The label text.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def ylabel(self, text: str) -> IFigure:
        """
        Set the label for the y-axis.

        Parameters
        ----------
        text : str
            The label text.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def zlabel(self, text: str) -> IFigure:
        """
        Set the label for the z-axis.

        Parameters
        ----------
        text : str
            The label text.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def xlim(self, min_value: float | None = None,
                   max_value: float | None = None) -> IFigure:
        """
        Set limits for the x-axis.

        Parameters
        ----------
        min_value : float or None, optional
            The minimum value for the x-axis.

        max_value : float or None, optional
            The maximum value for the x-axis.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def ylim(self, min_value: float | None = None,
                   max_value: float | None = None) -> IFigure:
        """
        Set limits for the y-axis.

        Parameters
        ----------
        min_value : float or None, optional
            The minimum value for the y-axis.

        max_value : float or None, optional
            The maximum value for the y-axis.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def zlim(self, min_value: float | None = None,
                   max_value: float | None = None) -> IFigure:
        """
        Set limits for the z-axis.

        Parameters
        ----------
        min_value : float or None, optional
            The minimum value for the z-axis.

        max_value : float or None, optional
            The maximum value for the z-axis.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def xscale(self, scale: AxisScale, base: float = 10) -> IFigure:
        """
        Set the scale for the x-axis.

        Parameters
        ----------
        scale : AxisScale
            The scale for the x-axis: 'linear' or 'log'.

        base : float, optional
            The base for the logarithmic scale, default is 10.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def yscale(self, scale: AxisScale, base: float = 10) -> IFigure:
        """
        Set the scale for the y-axis.

        Parameters
        ----------
        scale : AxisScale
            The scale for the y-axis: 'linear' or 'log'.

        base : float, optional
            The base for the logarithmic scale, default is 10.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def current_color(self) -> str:
        """
        Get the color which will be used for the next plot.

        Returns
        -------
        str
            The current color.
        """

    @abstract
    def scroll_color(self, count: int = 1) -> str:
        """
        Scroll a list of predefined colors for plots.

        Parameters
        ----------
        count : int, optional
            The number of colors to scroll.

        Returns
        -------
        str
            The current color before scrolling.
        """

    @abstract
    def reset_color(self) -> IFigure:
        """
        Set the current color to the start of the list.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def axis_aspect(self, mode: AspectMode) -> IFigure:
        """
        Set the aspect ratio of the axis.

        Parameters
        ----------
        mode : AspectMode
            The aspect ratio mode.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def as_image(self) -> ndarray:
        """
        Get the figure as a numpy array.

        Returns
        -------
        ndarray
            The figure as an image.
        """

    @abstract
    def save(self, filename: str) -> IFigure:
        """
        Save the figure to a file.

        Parameters
        ----------
        filename : str
            The filename for saving the figure.

        Returns
        -------
        IFigure
            The figure object representing the plot.
        """

    @abstract
    def close(self):
        """
        Close the figure. Free allocated resources.
        """

    @abstract
    def show(self, block: bool = True):
        """
        Display the figure.

        Parameters
        ----------
        block : bool, optional
            Whether to block further execution until the figure window is closed.
        """


@runtime_checkable
class IPlotEngine(Protocol):
    """
    Interface for a plotting engine (lib) that provides functionality for creating IFigure.
    """

    @property
    @abstract
    def name(self) -> str:
        """
        Get the name of the plotting engine.

        Returns
        -------
        str
            The name of the plotting engine.
        """

    @classmethod
    @abstract
    def is_available(cls) -> bool:
        """
        Check if the plotting engine is available for use (a plotting lib installed).

        Returns
        -------
        bool
            True if the plotting engine is available, False otherwise.
        """

    @abstract
    def figure(self, width: int, aspect_ratio: float) -> IFigure:
        """
        Factory method for creating a new figure with the specified width and aspect ratio.

        Parameters
        ----------
        width : int
            The width of the figure in pixels.

        aspect_ratio : float
            The aspect ratio of the figure.

        Returns
        -------
        IFigure
            A new figure instance.
        """

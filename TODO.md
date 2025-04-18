# TODO

## Next Release

- [ ] **API**: plot_range(x, y_up, y_down, ...)
- [ ] update to `plotly 6`

## Backlog
- [ ] **API**: `line_width` parameter for `fig.plot(...)`
- [ ] **API**: `fig.legend`: param for the legend location
- [ ] `README` Add name, description and shortcuts for all engines
- [ ] `README` example for non-gui (file) plotting
- [ ] **API**: `opacity: float` -> `opacity: float | list[float]`
- [ ] **API**: `fig.click_event(...)`
- [ ] Unified styling
  - [x] Engine independent config: `uplot.DEFAULT`
- [ ] TeX support
- [ ] `DataFrame` basic support
- [ ] `Bokeh` engine

## Done

- [x] **API**: switching log vs normal scale: `xscale()`, `yscale()`
- [x] `README` API description: supported functions per engine
- [x] **API**: `fig.bar(...)`
- [x] **API**: `fig.hline()` and `fig.vline()`
- [x] **API**: plugin system for plotting of a custom object
- [x] **API**: `fig.legend_group(...)` or parameter `legend_group`
- [x] **API**: return **IFigure** if possible to allow chaining
- [x] Fixed size of the legend items for **matplotlib**
- [x] **README** refactoring
- [x] API documentation
- [x] **API**: `fig.surface3d(...)`
- [x] Gallery
- [x] Changelog
- [x] **API**: `kwargs` to directly access underlying engine
- [x] **API**: aspect ratio param: `uplot.figure(..., aspect_ratio: float)`
- [x] **API**: `fig.plot3d(...)` and `fig.scatter3d(...)`

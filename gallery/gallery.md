# Gallery

1. [plot](#plot)
1. [scatter](#scatter)
1. [surface3d](#surface3d)


> See also jupyter notebook: `gallery.ipynb`.

## plot

### 2d

```python
import numpy as np
import uplt

# data
x = np.linspace(0, np.pi*4, num=100)
y1 = np.sin(x)
y2 = np.sin(x + np.pi/4)
y3 = np.sin(x + 2*np.pi/4)
y4 = np.sin(x + 3*np.pi/4)

# plot
fig = uplt.figure(engine='plotly5')
fig.plot(x, y1, name='data #1')
fig.plot(x, y2, name='data #2')
fig.plot(x, y3, name='data #3')
fig.plot(x, y4, name='data #4')
fig.legend()
fig.show()
```

<img src='asset/plot.png' width='700'>

### 3d

```python
import numpy as np
import uplt

x = np.linspace(0, np.pi*4, num=100)
y1 = np.sin(x)
y2 = np.sin(x - np.pi/4)

fig = uplt.figure(engine='plotly5')
fig.plot(x=y1, y=y2, z=x, name='data #1')
fig.plot(x=y1, y=y2, z=x+2, name='data #2')
fig.plot(x=y1, y=y2, z=x+4, name='data #1')
fig.legend()
fig.show()
```

<img src='asset/plot-3d.png' width='700'>

## scatter

### 2d

```python
import numpy as np
import uplt

# data
x = np.random.uniform(size=100)
y = np.random.uniform(size=100)
# random color per point
rgb_colors = np.random.uniform(low=0.3, high=0.8, size=[100, 3])

# plot
fig = uplt.figure(engine='plotly5')
fig.scatter(x, y)
fig.show()
```

<img src='asset/scatter.png' width='700'>


### hline & vline

```python
import numpy as np
import uplt

fig = uplt.figure('mpl')
fig.plot(x, y, name='cos')

fig.hline(y=0.5, x_min=10, x_max=15, line_style='--')
fig.hline(y=-0.3, line_style='--')

fig.vline(x=np.pi+np.pi/2, y_min=-0.5, y_max=0.5, line_style='--')
fig.vline(x=4*np.pi, line_style='--')

fig.xlabel('X Axis')
fig.ylabel('Y Axis')
fig.show()
```

<img src='asset/hvline.png' width='700'>

### 3d

```python
import numpy as np
import uplt

z = np.linspace(0, np.pi*4, num=100)
x = np.sin(z)
y = np.sin(z - np.pi/4)

rgb_colors = np.random.uniform(low=0.1, high=0.9, size=[100, 3])

fig = uplt.figure(engine='plotly5')
fig.scatter(x, y, z, color=uplt.color.rgb_to_str(rgb_colors))
fig.show()
```

<img src='asset/scatter-3d.png' width='700'>


## bar

```python
y1 = np.arange(5) + 1
y2 = y1[::-1]
x = [ 'A', 'B', 'C', 'AABB', 'D' ]

fig = uplt.figure(engine)
fig.bar(x, y1, name='T1')
fig.bar(x, y2, name='T2')
fig.bar(x, [1, 1, 1, 1, 1], opacity=0.5, name='T3')
fig.ylim(0, 8)
fig.hline(3, color='r', line_style='--')
fig.legend()
fig.show()
```

<img src='asset/bar.png' width='700'>

## surface3d

```python
x = np.arange(0, 5, 0.25)
y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig = uplt.figure('plotly', aspect_ratio=0.8)
fig.surface3d(x, y, Z,   name='data #1', colormap='blues')
fig.surface3d(x, y, Z*6, name='data #2', show_colormap=True)
fig.xlabel('X Axis')
fig.ylabel('Y Axis')
fig.zlabel('Z Axis')
fig.legend()
fig.show()
```

<img src='asset/surface3d.png' width='700'>

# Log-scale

```python
x = np.linspace(0, 100000, num=1000)
y = np.sqrt(x)

fig = uplt.figure(engine)
fig.plot(x, y, name='sqrt(x)')
fig.xscale('log', base=10)
fig.yscale('log', base=10)
fig.hline(y=100, line_style='--', color='r')
fig.vline(x=10000, line_style='--', color='r')
fig.xlim(100)
fig.ylim(10)
fig.legend()
fig.show()
```

<img src='asset/log_scale.png' width='700'>


# Legend

```python
x = np.arange(8)
y = np.arange(8)

fig = uplt.figure('plotly')
fig.scatter(x, y, marker_style='.', marker_size=1, name='data #1', legend_group='Small')
fig.scatter(x, y+1, marker_style='s', marker_size=6, name='data #2', legend_group='Small')
fig.scatter(x, y-1, marker_style='v', marker_size=10, name='data #3', legend_group='Small')
fig.scatter(x, y+3, marker_style='x', marker_size=25, name='data #4', legend_group='Big')
fig.plot(x, y-3, marker_style='o', marker_size=25, name='data #5', legend_group='Big')
fig.legend(True, equal_marker_size=True)
fig.show()
```

<img src='asset/legend.png' width='700'>

# Plugin

`DataFrame` plugin:
```python
import pandas as pd
import uplt.plugin as plugin


class DataFramePlugin(plugin.IPlotPlugin):
    """
    DataFrame minimalistic plugin (only data extraction)
    """

    def extract_data(self, obj: pd.DataFrame) -> list[plugin.PlotData]:
        data = []
        for name in obj.columns:
            if not np.issubdtype(obj.dtypes[name], np.number): continue
            y = obj[name].values
            x = np.arange(len(y))
            name = name.replace('_', ' ').title()
            data.append(plugin.PlotData(x=x, y=y, name=name))
        return data


# register plugin
plugin.register(pd.DataFrame, handler=DataFramePlugin())
```

`DataFrame` visualization:
```python
car_crashes = pd.read_csv(
    'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/car_crashes.csv'
)

fig = uplt.figure()
fig.plot(car_crashes[['total', 'speeding', 'alcohol', 'no_previous']])
fig.show()
```

<img src='asset/plugin.png' width='700'>

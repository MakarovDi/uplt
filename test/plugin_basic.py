import uplt
import uplt.plugin as plugin

from dataclasses import dataclass


@dataclass
class CustomObj:
    x: list[float]
    y: list[float]
    name: str


class CustomObjPlugin(plugin.IPlotPlugin):

    def extract_data(self, obj: list[CustomObj]) -> list[plugin.PlotData]:
        data = []
        for o in obj:
            data.append(plugin.PlotData(x=o.x, y=o.y, name=o.name))
        return data


data_list = [
    CustomObj(x=[1, 2, 3], y=[5, 6, 7], name='obj1'),
    CustomObj(x=[7, 6, 5], y=[5, 6, 7], name='obj2'),
]

data_tuple = (
    CustomObj(x=[1, 2, 3], y=[5, 6, 7], name='obj1'),
    CustomObj(x=[7, 6, 5], y=[5, 6, 7], name='obj2'),
)

# plugin.register(pd.DataFrame, handler=DataFramePlugin())
plugin.register(list[CustomObj], handler=CustomObjPlugin())
plugin.register(tuple[CustomObj, ...], handler=CustomObjPlugin())

fig = uplt.figure('mpl')
# fig = uplot.figure('plotly')

# regular plot
fig.plot(data_list)
fig.plot(data_tuple)

fig.legend()
fig.show()

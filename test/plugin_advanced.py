import uplt

import numpy as np
import pandas as pd # type: ignore

import uplt.plugin as plugin


class DataFramePlugin(plugin.IPlotPlugin):
    """
    DataFrame minimalistic plugin (only data extraction)
    """

    def extract_data(self, obj: pd.DataFrame) -> list[plugin.PlotData]:
        data = []
        for name in obj.columns:
            if not np.issubdtype(obj.dtypes[name], np.number):
                continue
            y = np.asarray(obj[name].values)
            x = np.arange(len(y))
            name = name.replace('_', ' ').title()
            data.append(plugin.PlotData(x=x, y=y, name=name))
        return data


class DataFramePluginAdvanced(plugin.IPlotPlugin):
    """
    DataFrame plugin with advanced style processing
    """

    def __init__(self):
        # joint name for all data in DataFrame
        self._joined_name = None


    def extract_data(self, obj: pd.DataFrame) -> list[plugin.PlotData]:
        data = []
        joined_name = []
        for name in obj.columns:
            if not np.issubdtype(obj.dtypes[name], np.number):
                continue
            y = np.asarray(obj[name].values)
            x = np.arange(len(y))
            name = name.replace('_', ' ').title()
            joined_name.append(name)
            data.append(plugin.PlotData(x=x, y=y, name=name))
        self._joined_name = ' | '.join(joined_name)
        return data


    def update_style(self, plot_type : plugin.PlotType,
                           data_index: int,
                           data_count: int,
                           data_name : str | None,
                           group_name: str | None,
                           **kwargs) -> dict:
        name = kwargs.get('name', None)
        if name is not None:
            return kwargs

        kwargs['name'] = data_name

        if kwargs.get('color', None) is not None:
            # single color mode:
            #   - the one legend entry will be shown for all datasets.
            #    (no reason to have multiple entries with a single color)
            #   - all names for the data will be combined into one.
            if data_index == data_count - 1:
                # set the combined name for the last dataset only
                kwargs['name'] = self._joined_name
            else:
                kwargs['name'] = None
            # combine everything into the same legend group (plotly)
            kwargs['legend_group'] = self._joined_name

        return kwargs


# plugin.register(pd.DataFrame, handler=DataFramePlugin())
plugin.register(pd.DataFrame, handler=DataFramePluginAdvanced())


car_crashes = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/car_crashes.csv')


fig = uplt.figure('mpl')
# fig = uplot.figure('plotly')

# regular plot
fig.plot(car_crashes[['total', 'speeding', 'alcohol', 'no_previous']])

# single color mode
# fig.plot(car_crashes[['total', 'speeding', 'alcohol', 'no_previous']], color='green')

fig.legend()
fig.show()

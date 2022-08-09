""" Volume primitive """

import numpy as np
import pandas as pd

from ..model import Primitive


class Volume(Primitive):
    """
    Volume Primitive

    Used to plot the volume

    Parameters
    ----------
    sma: int, default = 20
        the period of the simple moving average
    """

    def __init__(self, sma=20):
        self.sma = sma

    def __str__(self):
        return self.__class__.__name__

    def calc(self, data):
        volume = data.volume
        change = data.close.pct_change()

        result = dict(volume=volume, change=change)

        if self.sma:
            result['average'] = volume.rolling(self.sma).mean()

        result = pd.DataFrame(result)

        return result

    def plot_handler(self, data, chart, ax=None):
        if ax is None:
            ax = chart.get_axes('twinx')

        data = self.calc(data)
        data = chart.extract_df(data)

        index = data.index
        volume = data.volume
        change = data.change
        color = np.where(change < 0, "red", "grey")

        if ax._label == 'twinx':
            vmax = data.volume.max()
            ax.set_ylim(0.0, vmax * 4.0)
            ax.yaxis.set_visible(False)

        ax.bar(index, volume, width=1.0, alpha=0.3, zorder=0, color=color)

        if self.sma:
            average = data.average
            ax.plot(index, average, linewidth=0.7, color='grey')

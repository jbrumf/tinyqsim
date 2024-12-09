"""
Functions for plotting histograms and density matrices.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from pathlib import Path

import matplotlib.pyplot as plt

# Constants for 1D Histogram
WIDTH_1D = 5.0  # Min plot width (inches)
HEIGHT_1D = 1.5  # Default plot height (inches)


def plot_histogram(data: dict, show=True, save: str = False, ylabel=None, height=1) -> None:
    """Plot 1D histogram of data labelled with basis state names.
        :param data: Dictionary of data to plot
        :param show: Show the plot
        :param save: File name to save image (or None)
        :param ylabel: Label for the Y-axis
        :param height: Scaling factor for plot height
    """
    n_bars = len(data)
    width = max(WIDTH_1D, n_bars * 0.5)
    height *= HEIGHT_1D
    fig, ax = plt.subplots(1)
    fig.set_size_inches(width, height)
    # This assumes the insertion order of 'data' was by increasing keys.
    # The 'list' wrapper is needed to satisfy PyCharm type checker.
    plt.bar(list(data.keys()), list(data.values()), width=0.95)
    for label in ax.get_xmajorticklabels():
        label.set_rotation(65)
    margin = ax.patches[0].get_x()
    plt.xlim(margin, n_bars - 1 - margin)
    plt.subplots_adjust(bottom=0.25)
    if ylabel:
        plt.ylabel(ylabel)
    if show:
        plt.show()
    if save:
        fname = Path.home() / save
        fig.savefig(fname, bbox_inches='tight')

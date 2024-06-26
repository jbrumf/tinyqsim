"""
Plotting routines.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from pathlib import Path

import matplotlib.pyplot as plt


def plot_histogram(data, show=True, save: str = False, ylabel=None, height=1) -> None:
    """Plot histogram of data.
        :param data: Dictionary of data to plot
        :param show: Show the plot
        :param save: File name to save image (or None)
        :param ylabel: Label for the Y-axis
        :param height: Scaling factor for plot height
    """
    n_bars = len(data)
    width = max(5.0, n_bars * 0.5)  # Min plot width = 5 inches
    height *= 2.5  # Default plot height = 2.5 inches
    fig, ax = plt.subplots(1)
    fig.set_size_inches(width, height)
    plt.bar(data.keys(), data.values(), width=0.95)
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

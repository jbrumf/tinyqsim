"""
Plotting routines.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from pathlib import Path

import matplotlib.pyplot as plt


def plot_histogram(data, save: str = False, ylabel=None, height=2.5) -> None:
    """Plot histogram of data.
        :param data: Dictionary of data to plot
        :param save: File name to save image (or None)
        :param ylabel: Label for the Y-axis
        :param height: Height of the plot in inches
    """
    n_bars = len(data)
    width = max(5.0, n_bars * 0.5)  # Min plot width = 5
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
    plt.show()
    if save:
        fname = Path.home() / save
        fig.savefig(fname)

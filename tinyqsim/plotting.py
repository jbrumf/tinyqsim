"""
Functions for plotting data.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PI = '\u03C0'  # Unicode pi

# Constants
WIDTH_1D = 5.0  # Min plot width (inches)
HEIGHT_1D = 1.5  # Default plot height (inches)
BAR_WIDTH = 0.92  # Width of bar / pitch
H_SPACE = 0.1  # Gap between plots
TICK_ANGLE = 65  # Angle of tick labels (degrees)
COLORS = ('#7bc8f6', '#ffa500', '#67a6eb', 'r', 'g', 'b')  # Colors for subplots


def plot_bars(keys, data, show=True, save: str = False, ylabels=None,
              ylims: list[list[float]] | None = None, height=1) -> None:
    """Plot bar chart with one or more data sets.
    :param keys: Labels for X ticks
    :param data: Array of data arrays
    :param show: Show the plot
    :param save: File name to save image (or None)
    :param ylabels: Array of Y axis labels for the subplots
    :param ylims: array of limits for the axes
    :param height: Scaling factor for plot height (default=1)
    """
    nplots = len(data)

    # Check that array lengths match
    for i in range(nplots):
        assert len(keys) == len(data[i]), f'Array length mismatch for dataset {i}'

    n_bars = len(keys)
    width = max(WIDTH_1D, n_bars * 0.5)
    height *= HEIGHT_1D * nplots
    fig, ax = plt.subplots(nplots, 1, sharex=True)
    if nplots == 1:
        ax = [ax]
    fig.set_size_inches(width, height)
    plt.subplots_adjust(bottom=0.25, hspace=H_SPACE)

    # Configure tick-marks for subplots
    if nplots > 1:
        for i in range(nplots - 1):
            ax[i].tick_params(
                axis='x',  # Apply changes to the x-axis
                top=False,  # Hide ticks on the top side
                bottom=False,  # Hide ticks on the bottom side
            )

    # Draw zero lines
    for i in range(nplots):
        ax[i].axhline(y=0, lw=0.5, color='gray')

    # Plot the data
    for i in range(nplots):
        values = np.array(list(data[i]))
        ax[i].bar(keys, values, width=BAR_WIDTH, color=COLORS[i])

    # Add the tick labels at an angle
    for label in ax[nplots - 1].get_xmajorticklabels():
        label.set_rotation(TICK_ANGLE)

    # Make plot width fit data
    margin = -BAR_WIDTH / 2
    plt.xlim(margin, n_bars - 1 - margin)

    if ylims:
        for i in range(len(ylims)):
            if ylims[i] is not None:
                ax[i].set_ylim(ylims[i])

    if ylabels:
        for i in range(nplots):
            ax[i].set_ylabel(ylabels[i])

    # Display the plot (always displayed in Jupyter notebook)
    if show:
        plt.show()

    # Save the plot to a file
    if save:
        fname = Path.home() / save
        fig.savefig(fname, bbox_inches='tight')

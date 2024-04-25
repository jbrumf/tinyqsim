""" Prototype Bloch sphere.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import atan2, sin, cos, pi, asin
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as random

from tinyqsim.arrow_fix import Arrow3D

SIZE = 0.7


def bloch_to_qubit(phi: float, theta: float) -> np.ndarray:
    """Convert Bloch sphere angles to a qubit.
        :param phi: Bloch sphere 'phi' angle in radians
        :param theta: Bloch sphere 'theta' angle in radians
        :return: A qubit
    """
    assert 0 <= phi < 2 * pi
    assert 0 <= theta <= pi
    return np.array([cos(theta / 2),
                     sin(theta / 2) * (cos(phi) + sin(phi) * 1j)])


def qubit_to_bloch(psi: np.ndarray) -> tuple[float, float]:
    """Convert qubit to Bloch sphere angles (phi, theta).
        :param psi: qubit state
        :return: Bloch sphere angles (phi, theta) in radians
    """
    alpha, beta = psi

    theta = 2 * atan2(abs(beta), abs(alpha))
    ab = alpha.conjugate() * beta  # Adjust for global phase
    phi = atan2(ab.imag, ab.real)
    if phi < 0:
        phi += 2 * pi
    return phi, theta


def random_bloch() -> tuple[float, float]:
    """ Return random point on Bloch sphere.
        0 <= theta <= pi,  0 <= phi < 2*pi
        :return: phi, theta (radians)
    """
    phi = random.random() * 2 * pi
    theta = asin(random.random() * 2 - 1) + pi / 2
    return phi, theta


def random_qubit() -> np.ndarray:
    """ Return random qubit (uniformly distributed on Bloch sphere.
        0 <= theta <= pi,  0 <= phi < 2*pi
        :return: A qubit (uniformly distributed on Bloch sphere.)
    """
    return bloch_to_qubit(*random_bloch())


def plot_bloch(phi: float, theta: float, scale=1, azimuth=35, elevation=10,
               save: str = None) -> None:
    """ Plot bloch sphere.
        :param phi: Bloch sphere 'phi' angle in radians
        :param theta: Bloch sphere 'theta' angle in radians
        :param scale: scaling factor
        :param azimuth: view-point azimuth (radians)
        :param elevation: view-point elevation (radians)
        :param save: File name to save image (or None)
    """
    size = SIZE / scale
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_xlim((-size, size))
    ax.set_ylim((-size, size))
    ax.set_zlim((-size, size))
    ax.view_init(elev=elevation, azim=azimuth)

    # Experimental: Draw the sphere
    u, v = np.mgrid[0:2 * np.pi:50j, 0:np.pi:50j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, color="g", alpha=0.1)

    # Vector coordinates
    vx = cos(phi) * sin(theta)
    vy = sin(phi) * sin(theta)
    vz = cos(theta)

    # Draw wire-frame
    u, v = np.mgrid[0:2 * np.pi:37j, 0:np.pi:37j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_wireframe(x, y, z, lw=0.5, color="#D0D0D0", rstride=3, cstride=6)  # 3, 6 or 3, 3
    ax.plot_wireframe(x, y, z, lw=0.7, color="#808080", rstride=9, cstride=18)  # 9, 18

    # Draw a point
    ax.scatter([0], [0], [0], color="g", s=10)

    # Text options for arrow labels
    text_options = {'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 14}

    # Draw arrow for state
    arrow_prop_dict = dict(mutation_scale=20, arrowstyle='-|>', color='r', lw=2,
                           shrinkA=0, shrinkB=0)
    arrow = Arrow3D([0, vx], [0, vy], [0, vz], **arrow_prop_dict)
    ax.add_artist(arrow)
    # ax.text(vx * 1.1, vy * 1.1, vz * 1.1, u'|\u03C8>', **text_options)

    # Draw arrows for X, Y, Z axes
    arrow_prop_dict = dict(mutation_scale=20, arrowstyle='-|>', color='b',
                           shrinkA=0, shrinkB=0)
    arrow = Arrow3D([0, 1], [0, 0], [0, 0], **arrow_prop_dict)
    ax.add_artist(arrow)
    ax.text(1.1, 0, 0, r'$X$', **text_options)

    arrow_prop_dict = dict(mutation_scale=20, arrowstyle='-|>', color='b',
                           shrinkA=0, shrinkB=0)
    arrow = Arrow3D([0, 0], [0, 1], [0, 0], **arrow_prop_dict)
    ax.add_artist(arrow)
    ax.text(0, 1.1, 0, r'$Y$', **text_options)

    arrow_prop_dict = dict(mutation_scale=20, arrowstyle='-|>', color='b',
                           shrinkA=0, shrinkB=0)
    arrow = Arrow3D([0, 0], [0, 0], [0, 1], **arrow_prop_dict)
    ax.add_artist(arrow)
    ax.text(0, 0, 1.1, r'$Z$', **text_options)

    # Annotate with parameter values
    text = f'\nphi={phi * 180 / pi:.2f}\u00b0\ntheta={theta * 180 / pi:.2f}\u00b0'
    ax.text2D(0.06, 0.06, text, fontsize=12, linespacing=2.0)

    if save:
        fname = Path.home() / save
        fig.savefig(fname)

    plt.show()

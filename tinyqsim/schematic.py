""" Graphics for QCircuit Schematic.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrow, Arc

# Geometry constants
UNITS_PER_CM = 10  # Base scale (drawing units per cm)
CM_PER_IN = 2.54  # Centimetres per inch
QUBIT_PITCH = 18  # Pitch of qubit lines
XSTEP = 18  # Pitch of gates along X axis
HBW = 5  # Half Width/height of gate symbols
BW = 2 * HBW  # Full width/height of gate symbols
LEFT_MARGIN = 6  # For qubit labels etc
TOP_MARGIN = 1  # Margin above diagram
BOTTOM_MARGIN = 4  # Margin below diagram (for text annotations)

FONT_SIZE = 13
TINY_FONT = 11

G_COLOR = 'b'  # Default gate color
H_COLOR = '#00A000'  # Hadamard gate color
BARRIER_COLOR = '#A0A0A0'
QUBIT_COLOR = 'k'


class Scheduler:
    """Simple time-slot scheduler for placing gates."""

    def __init__(self):
        self._slots = []
        self._slot = 0

    def schedule(self, qubits) -> int:
        """Pack qubits into a slot.
           :param qubits: Qubits of gate
           :return: Slot number for the gate
        """
        lo = min(qubits)
        hi = max(qubits)
        interval = set(range(lo, hi + 1))
        if all([interval.isdisjoint(z) for z in self._slots]):
            self._slots.append(interval)
            return self._slot
        else:
            self._slots = [interval]
            self._slot += 1
            return self._slot


class Schematic:
    """ QCircuit Schematic."""

    def __init__(self, nqubits: int) -> None:
        """Initialize Schematic.
           :param: nqubits: number of qubits
        """
        self.nqubits = nqubits
        self.qubit_pitch = QUBIT_PITCH
        self.xstep = XSTEP
        self.ax = None

    # ------------------- Draw the quantum circuit ------------------

    # This is all in one method so it can run in a single notebook cell.
    def draw(self, model, scale: float = 1, show: bool = True, save: str = None) -> None:
        """ Draw the quantum circuit.
            :param: model: QCircuit model
            :param: scale: scale factor
            :param: show: show quantum circuit
            :param: save: File name to save image
        """

        # Count  number of time slots needed
        slots = Scheduler()
        n_slots = 0
        for (_, cqubits, tqubits, _) in model.items:
            n_slots = slots.schedule(cqubits + tqubits)
        n_slots += 1

        # Calculate drawing parameters
        xlength = max(10, n_slots * self.xstep)  # Length of qubit lines

        ymin = -(self.nqubits - 1) * self.qubit_pitch - HBW - BOTTOM_MARGIN
        ymax = HBW + TOP_MARGIN
        xmin = -LEFT_MARGIN
        xmax = xlength
        plot_width = (xmax - xmin) / UNITS_PER_CM / scale  # Overall width in cm
        plot_height = (ymax - ymin) / UNITS_PER_CM / scale  # Overall height in cm

        # Initialize the plotting
        fig = plt.figure(figsize=(plot_width / CM_PER_IN, plot_height / CM_PER_IN))
        self.ax = fig.add_subplot(111)
        self.ax.set_aspect("equal")
        self.ax.set_axis_off()
        self.ax.set_xlim((xmin, xmax))
        self.ax.set_ylim((ymin, ymax))

        # Draw the qubit lines and gates
        slots = Scheduler()
        x0 = self.xstep / 2  # X position of first gate
        self.draw_qubit_lines(xlength)
        for (name, cqubits, tqubits, args) in model.items:
            slot = slots.schedule(cqubits + tqubits)
            x = self.xstep * slot + x0
            self.draw_gate(name, x, cqubits, tqubits, args)

        # Save figure to PNG file
        if save:
            fname = Path.home() / save
            fig.savefig(fname)

        # Display the circuit
        if show:
            plt.show()
        self.ax = None

    def draw_qubit_lines(self, xlength: int) -> None:
        """ Draw the qubit lines.
            :param: xlength: Length of qubit lines
        """
        for qubit in range(self.nqubits):
            y = -qubit * self.qubit_pitch
            _ = self.ax.plot([0, xlength], [y, y], '-', c=QUBIT_COLOR, lw=1, zorder=0)
            self.ax.annotate('q' + str(qubit), (-LEFT_MARGIN, y), color=G_COLOR,
                             fontsize=12, ha='center', va='center')

    def draw_gate(self, name: str, x: float, cqubits: list[int], tqubits: list[int], args=None) -> None:
        """Draw a gate.
            :param: name: name of gate
            :param: x: x position
            :param: cqubits: list of control qubits
            :param: tqubits: list of target qubits
            :param: args: arguments
        """
        qubits = cqubits + tqubits
        match name:
            # Simple one-qubit gates
            case 'H':
                self.draw_generic_gate(x, 'H', [], qubits[0:1], color=H_COLOR)
            case 'I' | 'S' | 'SX' | 'T' | 'X' | 'Y' | 'Z':
                self.draw_generic_gate(x, name, [], qubits[0:1])

            # Parameterized gates
            case 'P' | 'RX' | 'RY':
                self.draw_generic_gate(x, name, [], qubits[0:1], args[1])

            # Controlled gates
            case 'CS' | 'CT' | 'CY':
                self.draw_generic_gate(x, name[1:], qubits[0:1], qubits[1:2])

            # Controlled parameterized gates
            case 'CP':
                self.draw_generic_gate(x, name[1:], qubits[0:1], qubits[1:2], args[1])

            # Custom unitary gates
            case 'U':
                self.draw_generic_gate(x, args[0], cqubits, tqubits)
            case 'CU':
                self.draw_generic_gate(x, args[0], qubits[0:1], qubits[1:])

            # Gates with special symbols
            case 'CX':
                self.draw_cx_gate(x, *qubits)
            case 'CZ':
                self.draw_cz_gate(x, *qubits)
            case 'SWAP':
                self.draw_swap_gate(x, qubits)
            case 'CCX':
                self.draw_ccx_gate(x, *qubits)
            case 'CSWAP':
                self.draw_cswap_gate(x, *qubits)
            case 'measure':
                self.draw_meters(x, *qubits)
            case 'barrier':
                self.draw_barrier(x)
            case _:
                raise ValueError('Unknown gate:' + name)

    def draw_generic_gate(self, x: float, text: str, cqubits: list[int],
                          qubits: list[int], label: str = None, color='w') -> None:
        """ Draw a generic rectangular gate.
            The gate can have any number of qubits, controls and an annotation
            (e.g. for rotation angle).

        :param x: horizontal position
        :param text: name of gate
        :param cqubits: list of control qubits
        :param qubits: list of target qubits
        :param label: label to annotate the gate
        :param color: fill color of box
        """
        w = BW
        h = BW
        fontsize = FONT_SIZE

        all_qubits = cqubits + qubits
        assert len(all_qubits) == len(set(all_qubits)), 'Repeated qubits'

        # Draw vertical line joining controls to gate
        if len(all_qubits) > 1:
            qmin = min(all_qubits)
            qmax = max(all_qubits)
            self.draw_vline(x, qmin, qmax)

        # Draw the gate rectangle
        low_qubit = min(qubits)
        high_qubit = max(qubits)
        y = -self.qubit_pitch * low_qubit
        dy = (high_qubit - low_qubit) * self.qubit_pitch
        p = Rectangle((x - w / 2, y + h / 2), w, -dy - h, linewidth=1,
                      edgecolor=G_COLOR, facecolor=color)
        self.ax.add_patch(p)

        # Draw the control dots
        if len(cqubits) > 0:
            for q in cqubits:
                self.draw_dot(x, q, 1.5)

        # Draw dotted line for qubits that just pass through
        for qubit in range(low_qubit, high_qubit + 1):
            if qubit not in qubits:
                yn = -self.qubit_pitch * qubit
                line = '-' if qubit in cqubits else ':'
                _ = self.ax.plot([x - w / 2, x + w / 2], [yn, yn], line, c='k',
                                 lw=1, zorder=1)

        # Label connections with argument numbers
        if len(qubits) > 1:
            for i, q in enumerate(qubits):
                y1 = -self.qubit_pitch * q
                self.ax.annotate(str(i), (x, y1), color=G_COLOR,
                                 fontsize=10, ha='center', va='center')

        # Add text for name of the gate
        if text:
            font = fontsize if len(text) <= 2 else fontsize - 2
            ytext = y - 1
            if len(qubits) > 1:
                ytext -= self.qubit_pitch * 0.5 - 1
            text_color = G_COLOR if color == 'w' else 'w'
            self.ax.annotate(text, (x, ytext), color=text_color,
                             fontsize=font, ha='center', va='center')

        # Add annotation
        if label:
            y = -self.qubit_pitch * high_qubit
            self.ax.annotate(label, (x, y - 9), color=G_COLOR,
                             fontsize=TINY_FONT, ha='center', va='center')

    # ------------------ Gates with special symbols -----------------

    def draw_cx_gate(self, x: float, q1: int, q2: int) -> None:
        """ Draw CX gate.
            :param: x: x position
            :param: q1: qubit 1 (control)
            :param: q2: qubit 2 (target)
        """
        self.draw_vline(x, q1, q2)
        self.draw_dot(x, q1, 1.5)
        self.draw_circle(x, q2, r=4, text='+')

    def draw_cz_gate(self, x: float, q1: int, q2: int) -> None:
        """ Draw CZ gate.
            :param: x: x position
            :param: q1: qubit 1 (control)
            :param: q2: qubit 2 I(target)
        """
        self.draw_vline(x, q1, q2)
        self.draw_dot(x, q1, 1.5)
        self.draw_dot(x, q2, 1.5)

    def draw_swap_gate(self, x: float, qubits: list[int]) -> None:
        """ Draw SWAP gate.
            :param: x: x position
            :param: q1: qubit 1
            :param: q2: qubit 2
        """
        q1, q2 = qubits[0], qubits[1]
        self.draw_vline(x, q1, q2)
        self.draw_cross(x, q1)
        self.draw_cross(x, q2)

    def draw_ccx_gate(self, x: float, q1: int, q2: int, q3: int) -> None:
        """ Draw CCX gate.
            :param: x: x position
            :param: q1: qubit 1 (control 1)
            :param: q2: qubit 2 (control 2)
            :param: q3: qubit 3 (target)
        """
        qmin = min([q1, q2, q3])
        qmax = max([q1, q2, q3])
        self.draw_vline(x, qmin, qmax)
        self.draw_dot(x, q1, 1.5)
        self.draw_dot(x, q2, 1.5)
        self.draw_circle(x, q3, r=4, text='+')

    def draw_cswap_gate(self, x: float, q1: int, q2: int, q3: int) -> None:
        """ Draw CSWAP gate.
            :param: x: x position
            :param: q1: qubit 1 (control)
            :param: q2: qubit 2 (target 1)
            :param: q3: qubit 3 (target 2)
        """
        qmin = min([q1, q2, q3])
        qmax = max([q1, q2, q3])
        self.draw_vline(x, qmin, qmax)
        self.draw_dot(x, q1, 1.5)
        self.draw_cross(x, q2)
        self.draw_cross(x, q3)

    def draw_meters(self, x: float, *qubits: int) -> None:
        """ Draw measurement 'gate' as meter symbols.
            :param: x: x position
            :param: qubits: list of qubits
        """
        for qubit in qubits:
            y = -self.qubit_pitch * qubit
            self.draw_square(x, qubit)
            # FIXME: Derive constants from w & h
            p = Arc((x, y - 1), 6, 6, theta1=0, theta2=180, color=G_COLOR)
            self.ax.add_patch(p)
            p = FancyArrow(x, y - 1, 2, 3, lw=1, color=G_COLOR, head_width=0)
            self.ax.add_patch(p)

    def draw_barrier(self, x: float) -> None:
        """ Draw barrier.
            :param: x: x position
        """
        y1 = self.qubit_pitch * 0.5
        y2 = -self.qubit_pitch * (self.nqubits - 0.5)  # - 20
        _ = self.ax.plot([x, x], [y1, y2], ':', c=BARRIER_COLOR, lw=3, zorder=0)

    # ------------- Draw basic shapes needed for gates --------------

    def draw_square(self, x: float, qubit: int, text: str = None,
                    color='w', fontsize: int = FONT_SIZE) -> None:
        """ Draw square gate symbol.
            :param: x: x position
            :param: qubit: qubit index
            :param: text: Text to go in rectangle
            :param: color: color
            :param: fontsize: fontsize
        """
        w = BW
        h = BW
        y = -self.qubit_pitch * qubit
        p = Rectangle((x - w / 2, y - h / 2), w, h, linewidth=1, edgecolor=G_COLOR, facecolor=color)
        self.ax.add_patch(p)
        if text:
            text_color = G_COLOR if color == 'w' else 'w'
            self.ax.annotate(text, (x, y - 1), color=text_color,
                             fontsize=fontsize, ha='center', va='center')

    def draw_circle(self, x: float, qubit: int, r=HBW, text: str = None, color='w',
                    fontsize: int = FONT_SIZE) -> None:
        """ Draw circle.
            :param: x: x position
            :param: qubit: qubit index
            :param: r: radius
            :param: text: Text to go in circle
            :param: color: color
            :param: fontsize: fontsize
        """
        y = -self.qubit_pitch * qubit
        p = Circle((x, y), r, edgecolor=G_COLOR, facecolor='w')
        self.ax.add_patch(p)
        if text:
            text_color = G_COLOR if color == 'w' else 'w'
            self.ax.annotate(text, (x, y), color=text_color,
                             fontsize=fontsize, ha='center', va='center')

    def draw_dot(self, x: float, qubit: int, r: float) -> None:
        """ Draw dot.
            :param: x: x position
            :param: qubit: qubit index
            :param: r: radious
        """
        y = -self.qubit_pitch * qubit
        p = Circle((x, y), r, edgecolor=G_COLOR, facecolor=G_COLOR)
        self.ax.add_patch(p)

    def draw_cross(self, x: float, qubit: int) -> None:
        """ Draw cross.
            :param: x: x position
            :param: qubit: qubit index
        """
        y = -self.qubit_pitch * qubit
        r = 2
        p = FancyArrow(x - r, y - r, 2 * r, 2 * r, lw=1.5, color=G_COLOR, head_width=0)
        self.ax.add_patch(p)
        p = FancyArrow(x - r, y + r, 2 * r, -2 * r, lw=1.5, color=G_COLOR, head_width=0)
        self.ax.add_patch(p)

    def draw_vline(self, x: float, q1: int, q2: int) -> None:
        """ Draw vertical line between two qubit lines.
            :param: x: x position
            :param: q1: qubit 1
            :param: q2: qubit 2
        """
        y1 = -self.qubit_pitch * q1
        y2 = -self.qubit_pitch * q2
        _ = self.ax.plot([x, x], [y1, y2], '-', c='k', lw=1, zorder=0)

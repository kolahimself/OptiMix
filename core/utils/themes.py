"""themes.py

This module contains variables and constants for themes, colors and fonts used throughout the app.
"""

import numpy as np
from tkinter import ttk, Entry

# OptiMix colors
BG = '#1E1E1E'
ALT_BG = '#332E33'
white_color = "#FFFFFF"
optimix_variants = ['#D232CC', '#C906C1', '#70056C', '#61045D', '#D90A0A']
cement_select_color = '#CD0791'
cagg_select_color = '#CF0877'
fagg_select_color = '#D4093E'
slump_select_color = '#CD0791'
vebe_select_color = '#CF0877'
report_bg_color = '#251B24'
transparent = "rgba(0 ,0 ,0 , 0)"
graph_colors = ['cyan', '#CCCCCC', '#4A002E', '#888888', '#A6429E',
                '#007ACC', '#00A86B', '#FFA500', '#0047AB', '#008080', '#800000']
fig_vi_colors = ['#00689D', '#FF5773', '#A61B1B', '#009E48', '#9932CC', '#D69600']


def gradient_generator(n: int, start_color: np.ndarray, end_color: np.ndarray) -> list[str]:
    """
    Generates n colors in an angular gradient between a supplied start and end colors
    :param n: (int): number of colors needed
    :param start_color: (np.ndarray) array containing rgb values of the start color
    :param end_color: (np.ndarray) array containing rgb values of the end color
    :return: (hex_colors): a list containing the generated colors in hexadecimal format
    """

    # Generate an array of angles evenly spaced from 0 to 2*pi
    angles = np.linspace(0, 2 * np.pi, n)

    # Interpolate the RGB values between start color and end color based on the angles
    g_colors = start_color + (end_color - start_color) * angles[:, np.newaxis] / (2 * np.pi)

    # Convert the colors to integers in the range 0-255
    g_colors = np.round(g_colors).astype(int)

    # Convert the RGB values to hexadecimal strings
    hex_colors = ['#' + ''.join(f'{c:02X}' for c in color) for color in g_colors]

    return hex_colors


# Generate 100 colors in an angular gradient between `#C906C1` and `#D90A0A`
colors = gradient_generator(
    n=100,
    start_color=np.array([0xC9, 0x06, 0xC1]),
    end_color=np.array([0xD9, 0x0A, 0x0A])
)

# Report title colors
report_title_colors = gradient_generator(
    n=150,
    start_color=np.array([0xFF, 0xFF, 0xFF]),
    end_color=np.array([0x6A, 0x5A, 0xCD])
)

# OptiMix fonts
lato = 'Lato'
ubuntu = 'Ubuntu'
# inter = 'Helvetica'
cambria_math = 'Cambria Math'
courier = "Courier New, monospace"
arial = 'Arial'
helvetica = "Helvetica"
calibri = "Calibri"
verdana = "Verdana"


def color_entry(entry: Entry) -> None:
    """
    Handles active entry color changes
    To be used in scripts at the `pages` packages
    :param: (tk.Entry) entry: the entry widget
    """

    def on_entry_focus_in():
        """
        Changes the entry at random from 100 generated colors
        when the entry widget is active
        param event: the binding event of the entry
        """
        entry.config(highlightcolor=np.random.choice(colors))

    def on_entry_focus_out():
        """
        - Changes the highlight color when focus is out

        param event: the binding event of the entry
        """

        entry.config(highlightcolor=white_color)

    # Handle color transitions
    entry.bind("<FocusIn>", lambda event: on_entry_focus_in())

    # Handle numerical validation
    entry.bind("<FocusOut>", lambda event: on_entry_focus_out())

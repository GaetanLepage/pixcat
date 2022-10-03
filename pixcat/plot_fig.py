import os
from io import BytesIO

import matplotlib

from .display import display


def plot_fig(
    fig: matplotlib.figure.Figure,
    save_path: str = None
) -> None:
    """
    Display the given matplotlib figure in a kitty terminal.
    Learn more about the specification here:
    https://github.com/kovidgoyal/kitty/blob/master/docs/graphics-protocol.rst

    Optionnaly (if `save_path` is provided), save the plot in a png file.

    Args:
        fig (matplotlib.figure.Figure):     A matplotlib to plot.
        save_path (str) - optional:         The path where to save the image.
    """

    if save_path:
        fig.savefig(save_path)

    if os.getenv('TERM') == 'xterm-kitty':
        # image_bytes will contain the image PNG data needed by kitty.
        image_bytes: bytes

        if save_path:
            with open(save_path, 'rb') as image_file:
                image_bytes = image_file.read()

        else:
            with BytesIO() as buf:
                fig.savefig(buf, format='png', facecolor='#888888')
                image_bytes = buf.getbuffer().tobytes()

        display(image_bytes=image_bytes)

    else:
        matplotlib.pyplot.show()

    matplotlib.pyplot.close(fig=fig)

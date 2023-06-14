from typing import Union

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
from matplotlib.transforms import Bbox


def to_file(contents: str, filename: str):
    if filename is None:
        print(contents)
    else:
        with open(filename, 'w') as f:
            f.write(contents)


def prepare_colorbar(fig: Figure, ax: Union[GeoAxes, Axes] = None, vertical=False, pad=0.09, width=0.02,
                     position: Union[tuple[float, float, float, float], list[float, float, float, float]] = None)\
         -> Axes:
    """
    add cax to fig
    :param position: x0, y0, x1, y1. If ax is not None, use ax.get_position() instead
    :param width: colorbar width.
    :param pad: width between colorbar and axes
    :param vertical: if colorbar is vertical or horizontal
    :param fig: figure
    :param ax: Axes or GeoAxes
    :return: colorbar axes
    """
    if ax is not None:
        ax_position: Bbox = ax.get_position()
        x0, y0, x1, y1 = ax_position.x0, ax_position.y0, ax_position.x1, ax_position.y1
    elif position is not None:
        x0, y0, x1, y1 = position
    else:
        raise Exception('ax and position can\'t be None at the same time!')
    # y0 = ax_position.y0 - 0.01
    # y1 = ax_position.y1 - 0.03
    pad = pad
    width = width
    if not vertical:
        cax1_position = Bbox.from_extents(
            x0, y0 - pad - width,
            x1, y0 - pad
        )
    else:
        cax1_position = Bbox.from_extents(
            x1 + pad, y0,
            x1 + pad + width, y1
        )
    cax = fig.add_axes(cax1_position)
    return cax


__all__ = ['to_file', 'prepare_colorbar']

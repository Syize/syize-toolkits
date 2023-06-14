from typing import Union

from cartopy.mpl.geoaxes import GeoAxes
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox


class OnResize:
    """
    listen on figure resize event and change colorbar position and size dynamically
    """
    def __init__(self, ax: Union[GeoAxes, Axes], cax: Axes):
        self.ax = ax
        self.cax = cax
        # get position to calculate width and vertical
        ax_position = (ax.get_position().x0, ax.get_position().y0, ax.get_position().x1, ax.get_position().y1)
        cax_position = (cax.get_position().x0, cax.get_position().y0, cax.get_position().x1, cax.get_position().y1)
        # check if is vertical
        diff_x = cax_position[2] - cax_position[0]
        diff_y = cax_position[3] - cax_position[1]
        if diff_x > diff_y:
            self.vertical = False
            self.width = diff_y
        else:
            self.vertical = True
            self.width = diff_x
        # get padding
        if self.vertical:
            self.padding = cax_position[0] - ax_position[2]
        else:
            self.padding = ax_position[1] - cax_position[3]

    def __call__(self, event):
        ax_position = self.ax.get_position()
        x0, y0, x1, y1 = ax_position.x0, ax_position.y0, ax_position.x1, ax_position.y1
        if not self.vertical:
            cax1_position = Bbox.from_extents(
                x0, y0 - self.padding - self.width,
                x1, y0 - self.padding
            )
        else:
            cax1_position = Bbox.from_extents(
                x1 + self.padding, y0,
                x1 + self.padding + self.width, y1
            )

        self.cax.set_position(cax1_position)


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
    fig.canvas.mpl_connect("resize_event", OnResize(ax, cax))
    return cax


__all__ = ['prepare_colorbar']

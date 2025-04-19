from typing import Union

import numpy as np
from cartopy.mpl.geoaxes import GeoAxes
from haversine import inverse_haversine
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox


class OnResize:
    """
    Listen on the figure resize event and change colorbar position and size dynamically
    """
    def __init__(self, ax: Union[GeoAxes, Axes, tuple[GeoAxes, GeoAxes], tuple[Axes, Axes]], cax: Axes):
        self.ax = ax
        self.cax = cax

        # get position to calculate width and vertical
        if isinstance(ax, tuple):
            ax_position = (ax[0].get_position().x0, ax[0].get_position().y0, ax[1].get_position().x1, ax[1].get_position().y1)
        else:
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
        # get ax new position so we can change cax's position
        if isinstance(self.ax, tuple):
            x0, y0, x1, y1 = self.ax[0].get_position().x0, self.ax[0].get_position().y0, self.ax[1].get_position().x1, self.ax[1].get_position().y1
        else:
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


def prepare_colorbar(fig: Figure, ax: Union[GeoAxes, Axes, tuple[GeoAxes, GeoAxes], tuple[Axes, Axes]] = None,
                     vertical=True, pad=0.02, width=0.02, position: Union[tuple[float, float, float, float], list[float]] = None) -> Axes:
    """
    Add cax to fig.

    :param fig: Matplotlib Figure object.
    :param ax: A single or two Axes(GeoAxes).
               For single Axes(GeoAxes), will add cax to the ax.
               For two Axes(GeoAxes), which should be the left-bottom and right-top ax of an ax group, will add cax to the ax group.
    :param vertical: If the cax is vertical.
    :param pad: The distance length between cax and ax (group).
    :param width: The width of the cax.
    :param position: A tuple (x0, y0, x1, y1) to set ax (group) area. This param won't be used if `ax` isn't None.
    :return:
    """
    # get position to add cax
    if ax is not None:
        if isinstance(ax, tuple):
            x0, y0 = ax[0].get_position().x0, ax[0].get_position().y0
            x1, y1 = ax[1].get_position().x1, ax[1].get_position().y1
        else:
            x0, y0, x1, y1 = ax.get_position().x0, ax.get_position().y0, ax.get_position().x1, ax.get_position().y1
    elif isinstance(position, (tuple, list)):
        if len(position) != 4:
            raise ValueError(f"Expected 4 values in `position`, but got {len(position)}")
        x0, y0, x1, y1 = position
    else:
        raise ValueError('`ax` and `position` can\'t be None at the same time!')
    
    # add cax
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
        
    cax = fig.add_axes(cax1_position)   # type: ignore
    
    # add callback to make cax change size automatically
    if ax is not None:
        fig.canvas.mpl_connect("resize_event", OnResize(ax, cax))
    return cax


def get_lon_lat_range(central_lon: float, central_lat: float, distance: float) -> tuple[tuple, tuple]:
    """
    Calculate the range of longitude and latitude with specific center point and distance

    :param central_lon: central longitude
    :param central_lat: central latitude
    :param distance: distance from center point to boundary. unit: kilometers
    :return: (lon1, lon2), (lat1, lat2)
    """
    radar_position = (central_lat, central_lon)
    lon1 = inverse_haversine(radar_position, distance, np.pi * 1.5)[1]
    lon2 = inverse_haversine(radar_position, distance, np.pi * 0.5)[1]
    lat1 = inverse_haversine(radar_position, distance, np.pi * 1)[0]
    lat2 = inverse_haversine(radar_position, distance, np.pi * 0)[0]
    return (lon1, lon2), (lat1, lat2)


__all__ = ['prepare_colorbar', 'get_lon_lat_range']

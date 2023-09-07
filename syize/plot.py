from typing import Union

from cartopy.mpl.geoaxes import GeoAxes
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox
from haversine import inverse_haversine
import numpy as np
import cartopy.crs as ccrs
from cnmaps import get_adm_maps, draw_maps


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
    if ax is not None:
        fig.canvas.mpl_connect("resize_event", OnResize(ax, cax))
    return cax


def get_lon_lat_range(central_lon: float, central_lat: float, distance: float) -> tuple[tuple, tuple]:
    """
    calculate the range of longitude and latitude with specific center point and distance
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


def add_map_to_axes(fig: Figure, ax: Axes, lon: Union[tuple, list], lat: Union[tuple, list], zorder='top',
                    map_level: str = None, province: str = None, city: str = None) -> GeoAxes:
    """
    add map to radar plot
    :param city: City name to plot
    :param province: Province name to plot
    :param map_level: cnmaps' level
    :param lat: latitude range, [-90, 90]
    :param lon: longitude range, [-180, 180]
    :param zorder: where map line plot. `top` means map plot on the original axes. `bottom` means under the original axes.
    :param fig:
    :param ax: original axes
    :return:
    """
    # get original axes position
    x0 = ax.get_position().x0
    y0 = ax.get_position().y0
    x1 = ax.get_position().x1
    y1 = ax.get_position().y1
    proj = ccrs.PlateCarree()
    # add another axes
    ax2: GeoAxes = fig.add_axes((x0, y0, x1 - x0, y1 - y0), projection=proj)
    if zorder == 'top':
        ax.set_zorder(0)
        ax2.set_zorder(1)
        ax2.patch.set_alpha(0)
    elif zorder == 'bottom':
        ax2.set_zorder(0)
        ax.set_zorder(1)
        ax.patch.set_alpha(0)
    else:
        raise Exception('zorder should be `top` or `bottom`, but {}'.format(zorder))
    ax2.axis('off')
    # plot map
    draw_maps(get_adm_maps(level=map_level, province=province, city=city), color='black', ax=ax2)
    diff_lat = lat[1] - lat[0]
    diff_lon = lon[1] - lon[0]
    if diff_lat > diff_lon:
        diff_lon = (diff_lat - diff_lon) / 2
        lon1 = lon[0] - diff_lon
        lon2 = lon[1] + diff_lon
        lat1 = lat[0]
        lat2 = lat[1]
    else:
        diff_lat = - (diff_lat - diff_lon) / 2
        lat1 = lat[0] - diff_lat
        lat2 = lat[1] + diff_lat
        lon1 = lon[0]
        lon2 = lon[1]
    ax2.set_xlim(lon1, lon2)
    ax2.set_ylim(lat1, lat2)
    return ax2


__all__ = ['prepare_colorbar', 'get_lon_lat_range', 'add_map_to_axes']

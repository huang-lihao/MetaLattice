"""
===============
MetaLattice logo
===============

This example generates the current metalattice logo, derived from matplotlib logo2.py.
"""

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.font_manager
from matplotlib.patches import PathPatch
from matplotlib.text import TextPath
import matplotlib.transforms as mtrans

MPL_BLUE = '#11557c'


def get_font_properties():
    # The original font is Calibri, if that is not installed, we fall back
    # to Carlito, which is metrically equivalent.
    if 'Calibri'.lower() in matplotlib.font_manager.findfont('Calibri:bold').lower():
        return matplotlib.font_manager.FontProperties(family='Calibri',
                                                      weight='bold')
    if 'Carlito'.lower() in matplotlib.font_manager.findfont('Carlito:bold').lower():
        print('Original font not found. Falling back to Carlito. '
              'The logo text will not be in the correct font.')
        return matplotlib.font_manager.FontProperties(family='Carlito',
                                                      weight='bold')
    print('Original font not found. '
          'The logo text will not be in the correct font.')
    return None


def create_icon_axes(fig, ax_position, lw_bars, lw_grid, lw_border, rgrid):
    """
    Create a polar axes containing the metalattice RVE figure.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to draw into.
    ax_position : (float, float, float, float)
        The position of the created Axes in figure coordinates as
        (x, y, width, height).
    lw_bars : float
        The linewidth of the bars.
    lw_grid : float
        The linewidth of the grid.
    lw_border : float
        The linewidth of the Axes border.
    rgrid : array-like
        Positions of the radial grid.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The created Axes.
    """
    with plt.rc_context({'axes.edgecolor': MPL_BLUE,
                         'axes.linewidth': lw_border}):
        ax = fig.add_axes(ax_position, projection='polar')
        ax.set_axisbelow(True)
        
        dtheta = 12 / 360 * 2 * np.pi
        X, Y = np.meshgrid(np.linspace(-dtheta/2, dtheta/2, 256), np.linspace(1.25, 1.75, 256))
        Z =  -(-0.1*X+1)*(0.1*Y+2)
        ax.contour(X, Y, Z,1000, cmap='viridis')
        
        lw = 7
        
        r = [0.75, 1.25,1.75, 2.25]
        theta = [-dtheta/2*3, -dtheta/2, dtheta/2, dtheta/2*3]
        grid = np.meshgrid(theta, r)
        ax.plot(grid[0], grid[1],'gray',lw=lw,solid_capstyle='round', solid_joinstyle='round')
        ax.plot(grid[0].T, grid[1].T,'gray',lw=lw,solid_capstyle='round', solid_joinstyle='round')
        
        r = [1.25,1.75]
        theta = [-dtheta/2, dtheta/2]
        grid = np.meshgrid(theta, r)
        ax.plot(grid[0], grid[1],'g',lw=lw,solid_capstyle='round', solid_joinstyle='round')
        ax.plot(grid[0].T, grid[1].T,'g',lw=lw,solid_capstyle='round', solid_joinstyle='round')

        ax.set_rorigin(-1)
        ax.set_rlim(1, 2)
        ax.set_theta_zero_location('S')
        ax.set_thetalim(-dtheta, dtheta)
        ax.set_axis_off()

        ax.tick_params(labelbottom=False, labeltop=False,
                       labelleft=False, labelright=False)

        return ax


def create_text_axes(fig, height_px):
    """Create an Axes in *fig* that contains 'metalattice' as Text."""
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_aspect("equal")
    ax.set_axis_off()

    path = TextPath((0, 0), "MetaLa    ice", size=height_px * 0.8,
                    prop=get_font_properties())

    angle = 4.25  # degrees
    trans = mtrans.Affine2D().skew_deg(angle, 0)

    patch = PathPatch(path, transform=trans + ax.transData, color=MPL_BLUE,
                      lw=0)
    ax.add_patch(patch)
    ax.autoscale()


def make_logo(height_px, lw_bars, lw_grid, lw_border, rgrid, with_text=False):
    """
    Create a full figure with the MetaLattice logo.

    Parameters
    ----------
    height_px : int
        Height of the figure in pixel.
    lw_bars : float
        The linewidth of the bar border.
    lw_grid : float
        The linewidth of the grid.
    lw_border : float
        The linewidth of icon border.
    rgrid : sequence of float
        The radial grid positions.
    with_text : bool
        Whether to draw only the icon or to include 'MetaLattice' as text.
    """
    dpi = 100
    height = height_px / dpi
    figsize = (5 * height, height) if with_text else (height, height)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.patch.set_alpha(0)
    
    ax_pos = (0.59, 0.0, 0.16, 0.8) if with_text else (0.03, 0.03, .94, .94)
    ax = create_icon_axes(fig, ax_pos, lw_bars, lw_grid, lw_border, rgrid)
    
    if with_text:
        create_text_axes(fig, height_px)
    
    return fig, ax

if __name__ == '__main__':
    # A large logo:

    make_logo(height_px=110, lw_bars=0.7, lw_grid=0.5, lw_border=1,
            rgrid=[1, 3, 5, 7])
    plt.savefig(r"docs\source\_static\favicon.svg")


    # # A small 32px logo:

    make_logo(height_px=32, lw_bars=0.3, lw_grid=0.3, lw_border=0.3, rgrid=[5])


    # A large logo including text, as used on the metalattice website.

    make_logo(height_px=110, lw_bars=0.7, lw_grid=0.5, lw_border=1,
            rgrid=[1, 3, 5, 7], with_text=True)
    plt.savefig(r"docs\source\_static\logo.svg")

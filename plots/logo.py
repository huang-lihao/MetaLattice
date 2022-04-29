import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.patches import PathPatch
from matplotlib.textpath import TextPath
import matplotlib.transforms as mtrans
import os
from PIL import Image

MPL_BLUE = '#11557c'


def get_font_properties():
    # The original font is Calibri, if that is not installed, we fall back
    # to Carlito, which is metrically equivalent.
    if 'Calibri'.lower() in matplotlib.font_manager.findfont(
            'Calibri:bold').lower():
        return matplotlib.font_manager.FontProperties(family='Calibri',
                                                      weight='bold')
    if 'Carlito'.lower() in matplotlib.font_manager.findfont(
            'Carlito:bold').lower():
        print('Original font not found. Falling back to Carlito. '
              'The logo text will not be in the correct font.')
        return matplotlib.font_manager.FontProperties(family='Carlito',
                                                      weight='bold')
    print('Original font not found. '
          'The logo text will not be in the correct font.')
    return None


def create_icon_axes(fig, ax_position, lw_bars, lw_grid, lw_border, rgrid):
    """
    Create a polar axes containing the matplotlib radar plot.

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
    with plt.rc_context({
            'axes.edgecolor': MPL_BLUE,
            'axes.linewidth': lw_border
    }):
        ax = fig.add_axes(ax_position)
        ax.set_axisbelow(True)

        linewidth = 5

        N = 1000
        n_1 = 6
        n_2 = 32
        i = np.linspace(0, 1, n_1)
        j = np.linspace(0, 1, n_2 + 1, endpoint=True)
        II, JJ = np.meshgrid(i, j)
        R = 20 * (3)**II
        THETA = 2 * np.pi * (JJ + 0.5 / n_2)
        XX = R * np.cos(THETA)
        YY = R * np.sin(THETA)

        m = int(n_2 / 4 * 3 - 1)
        n = int(n_1 / 2)
        XXX = XX[m:m + 2, n:n + 2]
        YYY = YY[m:m + 2, n:n + 2]

        x_avg = (XXX.max() + XXX.min()) / 2
        a = (XXX.max() - XXX.min()) / 2 * 1.618
        y_avg = (YYY.max() + YYY.min()) / 2

        ax.set_aspect("equal")
        ax.axis("off")

        ax.plot(XX[m - 1:m + 3, n - 1:n + 3],
                YY[m - 1:m + 3, n - 1:n + 3],
                "gray",
                linewidth=linewidth,
                solid_capstyle="round")
        ax.plot(XX[m - 1:m + 3, n - 1:n + 3].T,
                YY[m - 1:m + 3, n - 1:n + 3].T,
                "gray",
                linewidth=linewidth,
                solid_capstyle="round")

        ax.set_xlim([x_avg - a, x_avg + a])
        ax.set_ylim([y_avg - a, y_avg + a])

        ax.plot(XXX, YYY, "green", linewidth=linewidth, solid_capstyle="round")
        ax.plot(XXX.T,
                YYY.T,
                "green",
                linewidth=linewidth,
                solid_capstyle="round")

        xi = np.linspace(-1.0, 1.0, N)
        eta = np.linspace(-1.0, 1.0, N)
        XI, ETA = np.meshgrid(xi, eta)
        shape_funcs = np.array([
            1 / 4 * (1 + XI) * (1 + ETA),
            1 / 4 * (1 - XI) * (1 + ETA),
            1 / 4 * (1 + XI) * (1 - ETA),
            1 / 4 * (1 - XI) * (1 - ETA),
        ])
        XXXX = np.einsum(shape_funcs, [0, 1, 2], XXX.reshape((-1, )), [0])
        YYYY = np.einsum(shape_funcs, [0, 1, 2], YYY.reshape((-1, )), [0])
        ZZZZ = (XXXX - XXXX.min()) * (YYYY - YYYY.min() + a * 0.5)

        ax.contourf(XXXX, YYYY, ZZZZ)

        return ax


def create_text_axes(fig, height_px):
    """Create an axes in *fig* that contains 'matplotlib' as Text."""
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_aspect("equal")
    ax.set_axis_off()

    path = TextPath((0, 0),
                    "`   MetaLattice",
                    size=height_px * 0.8,
                    prop=get_font_properties())

    angle = 4.25  # degrees
    trans = mtrans.Affine2D().skew_deg(angle, 0)

    patch = PathPatch(path,
                      transform=trans + ax.transData,
                      color=MPL_BLUE,
                      lw=0)
    ax.add_patch(patch)
    ax.autoscale()


def make_logo(height_px, lw_bars, lw_grid, lw_border, rgrid, with_text=False):
    """
    Create a full figure with the Matplotlib logo.

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
        Whether to draw only the icon or to include 'matplotlib' as text.
    """
    dpi = 100
    height = height_px / dpi
    figsize = (5 * height, height) if with_text else (height, height)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.patch.set_alpha(0)

    if with_text:
        create_text_axes(fig, height_px)
    ax_pos = (0, 0.12, .17, 0.75) if with_text else (0.03, 0.03, .94, .94)
    ax = create_icon_axes(fig, ax_pos, lw_bars, lw_grid, lw_border, rgrid)

    return fig, ax


if __name__ == "__main__":
    os.chdir("./temp")

    make_logo(height_px=110,
              lw_bars=0.7,
              lw_grid=0.5,
              lw_border=1,
              rgrid=[1, 3, 5, 7],
              with_text=True)

    plt.savefig("logo.svg", dpi=1200, transparent=True)
    plt.savefig("logo.png", dpi=1200, transparent=True)

    make_logo(height_px=110,
              lw_bars=0.7,
              lw_grid=0.5,
              lw_border=1,
              rgrid=[1, 3, 5, 7],
              with_text=False)

    plt.savefig("favicon.png", dpi=1200, transparent=True)

    img = Image.open('favicon.png')
    img.save('favicon.ico', size=[(256, 256)])

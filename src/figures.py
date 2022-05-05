import matplotlib.pyplot as plt
import string
import pandas as pd
from .tools import *

LOGGER = get_logger('figures')

N_CHIPS = 330
N_COLS = 41
N_ROWS = 10
SPACE = 0.1

WCS_CIELAB_FILE = 'cnum-vhcm-lab-new.txt'
WCS_CNUM_FILE = 'chip.txt'
ROWS = [string.ascii_uppercase[i] for i in range(10)]


# init module
ensure_dir('./data')
ensure_file('./data/%s' % WCS_CIELAB_FILE, 'http://www1.icsi.berkeley.edu/wcs/data/cnum-maps/cnum-vhcm-lab-new.txt')
ensure_file('./data/%s' % WCS_CNUM_FILE, 'http://www1.icsi.berkeley.edu/wcs/data/20021219/txt/chip.txt')

__CHIPS = pd.read_csv('./data/%s' % WCS_CIELAB_FILE, delimiter='\t').sort_values(by='#cnum')
WCS_CNUMS = pd.read_csv('./data/%s' % WCS_CNUM_FILE, delimiter='\t', header=None).values
WCS_CHIPS = __CHIPS[['L*', 'a*', 'b*']].values
WCS_CHIPS_RGB = lab2rgb(WCS_CHIPS)

CNUMS_WCS_COR = dict(zip(WCS_CNUMS[:, 0], [(ROWS.index(WCS_CNUMS[cnum - 1, 1]), WCS_CNUMS[cnum - 1, 2]) for cnum in WCS_CNUMS[:, 0]]))
_WCS_COR_CNUMS = dict(zip(WCS_CNUMS[:, 3], WCS_CNUMS[:, 0]))


def cnum2ind(cnum):
    """
    convert chip number to location in the WCS palette
    Example: cnum2ind(100) returns (2,22)
    """
    return CNUMS_WCS_COR[cnum]


def code2cnum(code):
    """
    convert WCS palette code to chip number
    Example: code2cnum('C22') returns 100
    :param c: string
    :return:
    """
    if code[0] == 'A':
        return _WCS_COR_CNUMS['A0']
    if code[0] == 'J':
        return _WCS_COR_CNUMS['J0']
    return _WCS_COR_CNUMS[code]


def grid2img(grid, small_grid=False, white_space=True):
    d = grid.shape[1]
    img = np.ones((N_ROWS, N_COLS + 1, d))
    if not white_space:
        img = img * np.nan
    for cnum in range(1, len(grid) + 1):
        i, j = cnum2ind(cnum)
        j = j + 1 if j > 0 else j
        img[i, j, :] = grid[cnum - 1, :]
        if img[i, j, 0] == 50:
            img[i, j, :] = img[i, j, :]
    if small_grid:
        img = img[1:-1, 2:]
    return img


def get_color_grid(pCW, chips=WCS_CHIPS):
    pC = pCW.sum(axis=1)[:, None]
    pW_C = np.where(pC > 0, pCW / pC, 1 / pCW.shape[1])
    y = pW_C.argmax(axis=1)
    pW = pCW.sum(axis=0)[:, None]
    pC_W = pCW.T / (pW + 1e-20)
    mu_w = lab2rgb(pC_W.dot(chips))
    grid = mu_w[y]
    grid[pC[:, 0] == 0] = np.nan * grid[pC[:, 0] == 0]
    return grid


def mode_map(qW_M, pM=None, small_grid=False):
    if pM is None:
        n = qW_M.shape[0]
        pM = np.ones((n, 1))/n
    qMW = qW_M * pM
    grid = get_color_grid(qMW)
    img = np.flipud(grid2img(grid, small_grid=small_grid))
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    clrs = np.array([r.flatten(), g.flatten(), b.flatten()]).T
    ax = plt.pcolor(r, color=clrs, linewidth=0.04, edgecolors='None')
    ax.set_array(None)
    plt.xlim([0, 42])
    plt.ylim([0, 10])
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')


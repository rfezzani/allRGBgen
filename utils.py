import numpy as np
from skimage import color


def sort_by_hue(rgb, hsv=None):
    if hsv is None:
        hsv = color.rgb2hsv(rgb)
    return rgb[hsv[..., 0].argsort()]


def sort_by_val(rgb, hsv=None):
    if hsv is None:
        hsv = color.rgb2hsv(rgb)
    return rgb[hsv[..., 2].argsort()]


def sort_by_lum(rgb, lab=None):
    if lab is None:
        lab = color.rgb2lab(rgb)
    return rgb[lab[..., 0].argsort()]


def rand_sort(rgb, *args, **kwargs):
    _rgb = rgb.copy()
    np.random.shuffle(_rgb)
    return _rgb


def create_map(src):
    _, inv, count = np.unique(src,
                              return_inverse=True,
                              return_counts=True)

    bins = np.prod(src.shape)
    bags_idx = [x.tolist() for x in np.split(np.arange(bins, dtype=int),
                                             np.cumsum(count)[:-1])]

    _map = np.array([bags_idx[val].pop() for val in inv]).reshape(src.shape)
    return _map


def apply_map(allrgb, _map, bloc_size):
    blocs = [b.reshape((bloc_size, bloc_size, 3))
             for b in np.split(allrgb, bins)]
    img = np.vstack([np.hstack([blocs[col] for col in row]) for row in idx])
    return img

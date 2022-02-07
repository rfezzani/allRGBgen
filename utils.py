import numpy as np
from skimage import color
from skimage.exposure import equalize_hist


def transform(rgb, func, channel):
    return func(rgb)[..., channel]


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


def create_map(src):
    _, inv, count = np.unique(src,
                              return_inverse=True,
                              return_counts=True)

    bins = np.prod(src.shape)
    bags_idx = [x.tolist() for x in np.split(np.arange(bins, dtype=int),
                                             np.cumsum(count)[:-1])]

    _map = np.array([bags_idx[val].pop() for val in inv]).reshape(src.shape)
    return _map


def apply_map(allrgb, _map, px_size):
    bins = np.prod(_map.shape)
    blocs = [b.reshape((px_size, px_size, 3))
             for b in np.split(allrgb, bins)]
    img = np.vstack([np.hstack([blocs[col] for col in row]) for row in _map])
    return img


def to_mozaic(img, px_size):
    _img = img.copy()
    nl, nc = img.shape[:2]
    res0, res1 = nl // px_size, nc // px_size
    for i in range(res0):
        for j in range(res1):
            _img[i::res0,
                 j::res1, :] = img[i * px_size: px_size * (i + 1),
                                   j * px_size: px_size * (j + 1), :]
    return _img


def crop_or_pad(img, res0, res1, tform_args):
    if img.ndim != 3:
        raise ValueError("Input image must be RGB")
    nl, nc, _ = img.shape

    i0 = abs(res0 - nl) // 2
    j0 = abs(res1 - nc) // 2
    if nl < res0 or nc < res1:
        out = np.zeros((res0, res1))
        out[i0: i0 + nl, j0: j0+nc] = transform(img, *tform_args)
    else:
        out = transform(img[i0: i0 + res0, j0: j0 + res1, :], *tform_args)
    return equalize_hist(out, np.prod(out.shape))

import numpy as np
from skimage import color
from skimage import exposure


def transform(rgb, func, channel):
    if channel is not None:
        return func(rgb)[..., channel]
    else:
        return func(rgb)


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

    for i in range(px_size):
        for j in range(px_size):
            _img[i * res0: (i+1) * res0,
                 j * res1: (j+1) * res1, :] = img[i::px_size, j::px_size, :]
    return _img


def crop_or_pad(img, res0, res1, tform_args):
    _img = img
    if img.ndim == 3:
        if img.shape[2] == 3:
            _img = transform(img, *tform_args)
        elif img.shape[2] == 4:
            _img = transform(color.rgba2rgb(img), *tform_args)
        else:
            raise ValueError("Input image must be gray scale, RGB or RGBA")

    nl, nc = _img.shape

    out = np.zeros((res0, res1))

    i0 = abs(res0 - nl) // 2
    j0 = abs(res1 - nc) // 2

    s0 = slice(None)
    s1 = slice(None)
    s2 = slice(None)
    s3 = slice(None)
    if nl < res0:
        s0 = slice(i0, i0 + nl)
    else:
        s2 = slice(i0, i0 + res0)
    if nc < res1:
        s1 = slice(j0, j0 + nc)
    else:
        s3 = slice(j0, j0 + res1)

    out[s0, s1] = _img[s2, s3]

    return exposure.rescale_intensity(out)

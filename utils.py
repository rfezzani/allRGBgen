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

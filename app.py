import io
from itertools import product
from PIL import Image, ImageColor

import streamlit as st
import numpy as np

import skimage
from skimage import color, data

from utils import (sort_by_hue, sort_by_val, sort_by_lum, create_map,
                   apply_map, to_mozaic, crop_or_pad)

sort_by = {
    "luminance": sort_by_lum,
    "hue": sort_by_hue,
    "val": sort_by_val,
    "Distance to ref color": None
}

tform = {
    "luminance": (color.rgb2lab, 0),
    "hue": (color.rgb2hsv, 0),
    "val": (color.rgb2hsv, 2),
    "Distance to ref color": None
}


@st.cache
def get_shape(px_size, sort_fun, ref_col, usr_img, nl=4096, nc=4096):
    res0, res1 = nl // px_size, nc // px_size
    x = np.linspace(-np.pi, np.pi, res0, True)
    y = np.linspace(-np.pi, np.pi, res1, True)
    x, y = np.meshgrid(x, y, indexing='ij')

    if ref_col is not None:
        tform["Distance to ref color"] = (dist_to_ref_color(ref_col), None)

    shapes = {"Vertical ramp": x,
              "Horizontal ramp": y,
              "Circle": np.cos(x ** 2 + y ** 2),
              "Cat": crop_or_pad(data.cat(), res0, res1, tform[sort_fun]),
              "Camera": crop_or_pad(data.camera(), res0, res1,
                                    tform[sort_fun]),
              "Coffee": crop_or_pad(data.coffee(), res0, res1,
                                    tform[sort_fun]),
              "Clock": crop_or_pad(data.clock(), res0, res1, tform[sort_fun]),
              "Moon": crop_or_pad(data.moon(), res0, res1, tform[sort_fun]),
              "Astronaut": crop_or_pad(data.astronaut(),
                                       res0, res1, tform[sort_fun])}

    if usr_img is not None:
        img = np.array(Image.open(usr_img))
        shapes["Your image"] = crop_or_pad(img, res0, res1, tform[sort_fun])

    return shapes


@st.cache
def gen_values():
    vals = np.arange(256, dtype=np.uint8)
    allrgb = np.array(list(product(vals, vals, vals)))
    _allrgbcie = color.rgb2rgbcie(skimage.img_as_float(allrgb))
    _allhsvcie = color.rgb2hsv(_allrgbcie)
    _alllabcie = color.rgb2lab(_allrgbcie)
    return allrgb, _allhsvcie, _alllabcie


@st.cache
def get_img(sort_fun, shape, px_size, ref_col, usr_img, nl=4096, nc=4096):

    allrgb, _allhsv, _alllab = gen_values()
    if ref_col is None:
        sort_val = _alllab if sort_fun == "luminance" else _allhsv
        allrgb = sort_by[sort_fun](allrgb, sort_val)
    else:
        dist_to_ref = dist_to_ref_color(ref_col)
        allrgb = allrgb[np.argsort(dist_to_ref(_alllab, True))]

    src = get_shape(px_size, sort_fun, ref_col, usr_img, nl, nc)[shape]
    _map = create_map(src)
    img = apply_map(allrgb, _map, px_size)

    return img


@st.cache(allow_output_mutation=True)
def get_png(img):
    image = Image.fromarray(img)
    out = io.BytesIO()
    image.save(out, format="PNG")
    return out


@st.cache
def dist_to_ref_color(col):
    def dist_to_ref(img, islab=False):
        ref_color = color.rgb2lab(np.array(ImageColor.getrgb(col)) / 255)
        lab = color.rgb2lab(img) if not islab else img
        return color.deltaE_cie76(ref_color, lab)
    return dist_to_ref


st.set_page_config(layout="wide")

with st.sidebar:
    usr_img = st.file_uploader("Your image", type=["jpg", "png", "jpeg"])
    px_size = st.selectbox("Super-pixel size", [32, 16, 8], index=1)
    sort_fun = st.selectbox("Sort strategy", sort_by.keys())
    container = st.empty()
    if sort_fun == "Distance to ref color":
        ref_col = container.color_picker("Reference color")
    else:
        ref_col = None
    shape = st.selectbox("Super-pixel map",
                         get_shape(px_size, sort_fun, ref_col, usr_img).keys())
    mozaic = st.checkbox("Make mozaic")

    img = get_img(sort_fun, shape, px_size, ref_col, usr_img)

    if mozaic:
        img = to_mozaic(img, px_size)

    img_dl = st.download_button("Load generated image", get_png(img),
                                file_name="allrgb.png", mime="image/png")

col0, col1 = st.columns(2)
with open("README.md") as f:
    col1.write(f.read())
col0.image(img)

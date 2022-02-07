import io
from itertools import product
from PIL import Image

import streamlit as st
import numpy as np

import skimage
from skimage import color, data

from utils import (sort_by_hue, sort_by_val, sort_by_lum, create_map,
                   apply_map, to_mozaic, crop_or_pad)

sort_by = {
    "hue": sort_by_hue,
    "val": sort_by_val,
    "lum": sort_by_lum,
}

tform = {
    "hue": (color.rgb2hsv, 0),
    "val": (color.rgb2hsv, 2),
    "lum": (color.rgb2lab, 0)
}


@st.cache
def get_shape(px_size, sort_fun, nl=4096, nc=4096):
    res0, res1 = nl // px_size, nc // px_size
    x = np.linspace(-np.pi, np.pi, res0, True)
    y = np.linspace(-np.pi, np.pi, res1, True)
    x, y = np.meshgrid(x, y, indexing='ij')

    return {"Vertical ramp": x,
            "Horizontal ramp": y,
            "Random": np.random.rand(res0, res1),
            "Circle": np.cos(x ** 2 + y ** 2),
            "Cat": crop_or_pad(data.cat(), res0, res1, tform[sort_fun])}


@st.cache
def gen_values():
    vals = np.arange(256, dtype=np.uint8)
    allrgb = np.array(list(product(vals, vals, vals)))
    _allrgbcie = color.rgb2rgbcie(skimage.img_as_float(allrgb))
    _allhsvcie = color.rgb2hsv(_allrgbcie)
    _alllabcie = color.rgb2lab(_allrgbcie)
    return allrgb, _allhsvcie, _alllabcie


@st.cache
def get_img(sort_fun, shape, px_size, nl=4096, nc=4096):

    allrgb, _allhsv, _alllab = gen_values()
    sort_val = _alllab if sort_fun == "lum" else _allhsv

    allrgb = sort_by[sort_fun](allrgb, sort_val)

    src = get_shape(px_size, sort_fun, nl, nc)[shape]
    _map = create_map(src)
    img = apply_map(allrgb, _map, px_size)

    return img


@st.cache(allow_output_mutation=True)
def get_png(img):
    image = Image.fromarray(img)
    out = io.BytesIO()
    image.save(out, format="PNG")

    return out


with st.sidebar:
    px_size = st.selectbox("Super pixel size", [32, 16, 8, 4, 2, 1], index=1)
    sort_fun = st.selectbox("Sort strategy", sort_by.keys())
    shape = st.selectbox("Shape", get_shape(px_size, sort_fun).keys())
    mozaic = st.checkbox("Make mozaic")

cat = get_shape(px_size, sort_fun)["Cat"]

img = get_img(sort_fun, shape, px_size)

if mozaic:
    img = to_mozaic(img, px_size)

st.image(img)

with st.sidebar:
    img_dl = st.download_button("Load generated image", get_png(img),
                                file_name="allrgb.png", mime="image/png")

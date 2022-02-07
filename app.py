import io
from itertools import product
from PIL import Image

import streamlit as st
import numpy as np
from matplotlib import pyplot as plt

import skimage
from skimage import color

from utils import (sort_by_hue, sort_by_val, sort_by_lum, rand_sort)

sort_by = {
    "rand": rand_sort,
    "hue": sort_by_hue,
    "val": sort_by_val,
    "lum": sort_by_lum,
}


@st.cache
def gen_values():
    vals = np.arange(256, dtype=np.uint8)

    allrgb = np.array(list(product(vals, vals, vals)))
    _allrgb = skimage.img_as_float(allrgb)
    _allhsv = color.rgb2hsv(_allrgb)
    _alllab = color.rgb2lab(_allrgb)
    _allrgbcie = color.rgb2rgbcie(_allrgb)
    _allhsvcie = color.rgb2hsv(_allrgbcie)
    _alllabcie = color.rgb2lab(_allrgbcie)
    return allrgb, _allhsv, _alllab, _allhsvcie, _alllabcie


@st.cache
def get_img(sort_fun, tocie, px_size, nl=4096, nc=4096):

    allrgb, _allhsv, _alllab, _allhsvcie, _alllabcie = gen_values()

    if tocie:
        sort_val = _alllabcie if sort_fun == "lum" else _allhsvcie
    else:
        sort_val = _alllab if sort_fun == "lum" else _allhsv

    allrgb = sort_by[sort_fun](allrgb, sort_val)
    img = allrgb.reshape(nl, nc, 3)

    return img


@st.cache(allow_output_mutation=True)
def get_png(img):
    image = Image.fromarray(img)
    out = io.BytesIO()
    image.save(out, format="PNG")

    return out


with st.sidebar:
    tocie = st.checkbox("Convert to RGB CIE color space")
    px_size = st.selectbox("Super pixel size", [16, 8, 4, 2, 1])
    sort_fun = st.selectbox("Sort strategy", sort_by.keys())

img = get_img(sort_fun, tocie, px_size)

fig, ax = plt.subplots(1, 1, figsize=(6, 6))

ax.imshow(img)
ax.set_axis_off()

fig.tight_layout()

st.pyplot(fig)

with st.sidebar:
    img_dl = st.download_button("Load generated image", get_png(img),
                                file_name="allrgb.png", mime="image/png")

from itertools import product

import streamlit as st
import numpy as np
from matplotlib import pyplot as plt

import skimage
from skimage import color, exposure

from utils import sort_by_hue, sort_by_val, sort_by_lum

sort_by = {
    "hue": sort_by_hue,
    "val": sort_by_val,
    "lum": sort_by_lum,
}


vals = np.arange(256, dtype=np.uint8)

_allrgb = skimage.img_as_float(np.array(list(product(vals, vals, vals))))
_allrgbcie = color.rgb2rgbcie(_allrgb)
_allhsv = color.rgb2hsv(_allrgb)
_allhsvcie = color.rgb2hsv(_allrgbcie)
_alllab = color.rgb2lab(_allrgb)
_alllabcie = color.rgb2lab(_allrgbcie)

with st.sidebar:
    tocie = st.checkbox("Convert to RGB CIE color space")
    px_size = st.selectbox("Super pixel size", [16, 8, 4, 2, 1])
    sort = st.selectbox("Sort strategy", sort_by.keys())

if tocie:
    allrgb = _allrgbcie
    sort_val = _alllabcie if sort == "lum" else _allhsvcie
else:
    allrgb = _allrgb
    sort_val = _alllab if sort == "lum" else _allhsv

nl, nc = 4096, 4096  # Output shape
res0, res1 = nl // px_size, nc // px_size  # Map shape

print(sort)
allrgb = sort_by[sort](allrgb, sort_val)

img = allrgb.reshape(4096, 4096, 3)

fig, ax = plt.subplots(1, 1, figsize=(6, 6))

ax.imshow(img)
ax.set_axis_off()

fig.tight_layout()

st.pyplot(fig)

## Super pixel allRGB

This application is inspired by the [allRGB challenge](https://allrgb.com/):

> The objective of allRGB is simple: To create images with one pixel
> for every RGB color (16,777,216); not one color missing, and not one
> color twice.

### Strategy

All RGB values are first sorted. Different options are provided (by
luminance, hue, value or distance to a reference color).

The sorted values are then split in blocs with the size of the super
pixels, and finally arranged according to a map of super pixels.

A mozaic can easily be obtained by dispatching the superpixels:

```
[0 0  1 1  2 2]        [0 1 2   0 1 2]
[0 0  1 1  2 2]        [3 4 5   3 4 5]
                       [6 7 8   6 7 8]
[3 3  4 4  5 5]   ->
[3 3  4 4  5 5]
                       [0 1 2   0 1 2]
[6 6  7 7  8 8]        [3 4 5   3 4 5]
[6 6  7 7  8 8]        [6 7 8   6 7 8]
```

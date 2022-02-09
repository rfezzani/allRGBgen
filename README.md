## Super pixel allRGB

This application is inspired by the [allRGB challenge](https://allrgb.com/):

> The objective of allRGB is simple: To create images with one pixel
> for every RGB color (16,777,216); not one color missing, and not one
> color twice.

### Strategy

1. All RGB values are first sorted. Different options are provided (by
   luminance, hue, value or distance to a reference color).
2. The sorted values are then split in blocs with the size of the
   super-pixels, and finally arranged according to a map of
   super-pixels.
3. A mozaic can easily be obtained by dispatching the super-pixels:

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

### Notes

- After having uploaded an image to be processed, you need to select
  **Your image** in the `Super-pixel map` selection box.
- The generated image is 4096×4096 pixels.
- The `Super-pixel size` parameter *px* defines the super-pixel-map
  size *S* = 4096 / *px*.
- The input image used to generate the super-pixel-map is cropped or
  padded to fit the *S*×*S* super-pixel-map.

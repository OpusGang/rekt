## rekt

Simple cropping and stacking to merge two clips as opposed to using a square mask.

## rekt_fast

Same as `rekt` with the exception that you can pass a function to be applied to the cropped clip.
This can be used to vastly speed up filters that don't require the entire image:

```py
clip = rekt_fast(clip, lambda c: c.std.Invert(), left=10, top=10, right=10, bottom=10)
```

## rektaa

Wrapper for `rekt_fast` with TAA.
Default `aamode` is nnedi3.

## rektlvl(s)

A faster version of havsfunc's FixBrightness(Protect2). It also features the option to process multiple rows or columns in one line.
```py
    '''
    More or less a wrapper around std.Levels with rekt_fast for darkening or brightening lines, usually on frame edges.
    :param clip: Clip to be processed.
    :param rownum: Row(s) to be processed.
    :param rowval: Row adjustment value. Negatives darken, positives brighten. Values can be between -100 and 100.
    :param colnum: Column(s) to be processed.
    :param colval: Column adjustment value. Negatives darken, positives brighten. Values can be between -100 and 100.
    :param prot_val: If None or False, this will work like FixBrightness. If an int, only a top protection is used.
                     Specify a list and the first value will be the bottom protect, while the second the top protect.
                     Values within 10 from the protect will be scaled linearly, while values past the protect aren't touched.
                     The AviSynth script this is from:
                     https://github.com/Asd-g/AviSynthPlus-Scripts/blob/master/FixBrightnessProtect3.avsi
    :return: Clip with first plane's values adjusted by adj_val.
    '''
```

### Contact
- **IRC Channel**: `#OpusGang` on `irc.libera.chat`

## rekt

Creates a rectangular "mask" for a fix to be applied to.

## rekt_fast

Creates a rectangular "mask" in which a fix is applied to only the masked area.  This vastly speeds up filters like anti-aliasing and scaling.
This wrapper works with a lambda function, which is applied to the "m" clip later on:
```python
rekt_fast(src, fun = lambda m: taa.TAAmbk(m, aatype=3, preaa=-1, strength=0.5, mtype=2), left=2, right=8, top=10, bottom=2)
```
Results in the following function being applied to only the masked rectangle:
```python
def f(m):
    return taa.TAAmbk(m, aatype=3, preaa=-1, strength=0.5, mtype=2)
```
## rektaa

Anti-aliasing alias that applies TAA to rekt_fast.  Default aatype is 3 with no mask, preaa, postaa, and strength 0.
Parameters are clip, location (left, top, right, bottom), and TAA parameters.

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

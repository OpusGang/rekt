# uvsfunc

Just some basic garbage to make VS scripts easier to write.

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

## rektdb

De-banding alias that applies f3kdb via rekt_fast.  Uses kageru's retinex_edgemask by default.

## black_detect

Tool to highlight black lines on borders and place them in the middle. Such lines should then create a straight line or even a cross if horizontal and vertical lines line up accordingly.
The threshold is set for very dark black lines, so it has to be adjusted for detecting dirty lines.  There are also only default values for one or two byte depths.

Optional "fix" included.  It's definitely recommended to do this manually, though.
The fix depends on FillBorders and applies it to the highlighted areas on every clip.  This can potentially damage unaffected areas.
I might write a protect for this eventually, but I only really care about the detection, not the fix.


## ds

Stupid downscaling that should automatically calculate the correct width and height.
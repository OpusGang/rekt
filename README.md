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

## rektlvl(s)

A faster version of havsfunc's FixBrightness(Protect2). It also features the option to process multiple rows or columns in one line.
The main function that does all the processing is rektlvl, while rektlvls is a simple wrapper to call rektlvl multiple times.
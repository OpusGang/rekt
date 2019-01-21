from vapoursynth import core
import vapoursynth as vs

'''    
Creates a rectangular "mask" for a fix to be applied to.
'''


def rekt(src, fix, left=0, top=0, right=0, bottom=0):
    if left > 0 or right > 0:
        m = core.std.Crop(fix, left=left, right=right)
        l = core.std.Crop(src, right=src.width - left) if left > 0 else 0
        r = core.std.Crop(src, left=src.width - right) if right > 0 else 0
        params = [x for x in [l, m, r] if x != 0]
        m = core.std.StackHorizontal(params)
    if top > 0 or bottom > 0:
        t = core.std.Crop(src, bottom=src.height - top) if top > 0 else 0
        m = core.std.Crop(m, bottom=bottom, top=top)
        b = core.std.Crop(src, top=src.height - bottom) if bottom > 0 else 0
        params = [x for x in [t, m, b] if x != 0]
        m = core.std.StackVertical(params)
    return m


'''
Creates a rectangular "mask" in which a fix is applied to only the masked area.
This vastly speeds up filters like anti-aliasing and scaling.
This wrapper works with a lambda function called m, which is applied to the "m" clip later on:

rekt_fast(src, fun=lambda m: taa.TAAmbk(m, aatype=3, preaa=-1, strength=-1, mtype=2), left=2, right=8, top=10, bottom=2)

Results in the following function being applied to only the masked rectangle:

def f(m):
    return taa.TAAmbk(m, aatype=3, preaa=-1, strength=-1, mtype=2)
'''


def rekt_fast(src, fun=lambda x: x, left=0, top=0, right=0, bottom=0):
    m = core.std.Crop(src, left=left, right=right, bottom=bottom, top=top)
    if left > 0 or right > 0:
        m = fun(m).std.AddBorders(top=top, bottom=bottom)
        l = core.std.Crop(src, right=src.width - left) if left > 0 else 0
        r = core.std.Crop(src, left=src.width - right) if right > 0 else 0
        params = [x for x in [l, m, r] if x != 0]
        m = core.std.StackHorizontal(params)
    else:
        m = fun(m).std.AddBorders(right=right, left=left)
    if top > 0 or bottom > 0:
        t = core.std.Crop(src, bottom=src.height - top) if top > 0 else 0
        m = core.std.Crop(m, bottom=bottom, top=top)
        b = core.std.Crop(src, top=src.height - bottom) if bottom > 0 else 0
        params = [x for x in [t, m, b] if x != 0]
        m = core.std.StackVertical(params)
    return m


'''
Anti-aliasing alias.
'''


def rektaa(clip, left=0, top=0, right=0, bottom=0, aatype=3, aatypeu=None, aatypev=None, preaa=0, strength=0, cycle=0,
           mtype=None, masktype=None, mclip=None,
           mthr=None, mthr2=None, mlthresh=None, mpand=(1, 0), txtmask=0, txtfade=0, thin=0, dark=0.0, sharp=0,
           aarepair=0, postaa=None, src=None, stabilize=0, down8=True, showmask=0, opencl=True, opencl_device=0):
    import vsTAAmbk as taa
    if masktype != None:
        return rekt_fast(clip, left=left, right=right, top=top, bottom=bottom,
                         fun=lambda x: taa.TAAmbk(x, aatype=aatype, aatypeu=aatypeu, aatypev=aatypev, preaa=preaa,
                                                  strength=strength, cycle=cycle, mtype=masktype, mclip=mclip,
                                                  mthr=mthr, mthr2=mthr2, mlthresh=mlthresh, mpand=mpand,
                                                  txtmask=txtmask, txtfade=txtfade, thin=thin, dark=dark, sharp=sharp,
                                                  aarepair=aarepair, postaa=postaa, src=src, stabilize=stabilize,
                                                  down8=down8, showmask=showmask, opencl=opencl,
                                                  opencl_device=opencl_device))
    elif mtype != None:
        return rekt_fast(clip, left=left, right=right, top=top, bottom=bottom,
                         fun=lambda x: taa.TAAmbk(x, aatype=aatype, aatypeu=aatypeu, aatypev=aatypev, preaa=preaa,
                                                  strength=strength, cycle=cycle, mtype=masktype, mclip=mclip,
                                                  mthr=mthr, mthr2=mthr2, mlthresh=mlthresh, mpand=mpand,
                                                  txtmask=txtmask, txtfade=txtfade, thin=thin, dark=dark, sharp=sharp,
                                                  aarepair=aarepair, postaa=postaa, src=src, stabilize=stabilize,
                                                  down8=down8, showmask=showmask, opencl=opencl,
                                                  opencl_device=opencl_device))
    else:
        return rekt_fast(clip, left=left, right=right, top=top, bottom=bottom,
                         fun=lambda x: taa.TAAmbk(x, aatype=aatype, aatypeu=aatypeu, aatypev=aatypev, preaa=preaa,
                                                  strength=strength, cycle=cycle, mtype=masktype, mclip=mclip,
                                                  mthr=mthr, mthr2=mthr2, mlthresh=mlthresh, mpand=mpand,
                                                  txtmask=txtmask, txtfade=txtfade, thin=thin, dark=dark, sharp=sharp,
                                                  aarepair=aarepair, postaa=postaa, src=src, stabilize=stabilize,
                                                  down8=down8, showmask=showmask, opencl=opencl,
                                                  opencl_device=opencl_device))


'''
De-banding alias.  Can use a lambda mask.  Default is retinex_edgemask from kagefunc.  Requires fvsfunc and kagefunc.
'''


def rektdb(clip, left=0, top=0, right=0, bottom=0,
           range=15, y=48, cb=0, cr=0,
           grainy=15, grainc=0, sample_mode=2, seed=None,
           blur_first=True, dynamic_grain=True,
           opt=-1, dither_algo=3, keep_tv_range=False,
           output_depth=16, random_algo_ref=1, random_param_ref=1, random_param_grain=1,
           preset=None, mask=retinex):
    if mask == retinex:
        import fvsfunc as fvf
        import kagefunc as kgf
        clip = fvf.Depth(16)
        m = rekt_fast(clip.std.ShufflePlanes(0, vs.GRAY), lambda x: kgf.retinex_edgemask(x), left=left, right=right,
                      top=top, bottom=bottom)
        deband = rekt_fast(clip, left=left, right=right, top=top, bottom=bottom,
                           fun=lambda x: core.f3kdb.Deband(x, range=range, y=y, cb=cb, cr=cr,
                                                           grainy=grainy, grainc=grainc, sample_mode=sample_mode,
                                                           seed=seed,
                                                           blur_first=blur_first, dynamic_grain=dynamic_grain,
                                                           opt=opt, dither_algo=dither_algo,
                                                           keep_tv_range=keep_tv_range,
                                                           output_depth=output_depth, random_algo_ref=random_algo_ref,
                                                           random_param_ref=random_param_ref,
                                                           random_param_grain=random_param_grain,
                                                           preset=preset))
        return core.std.MaskedMerge(deband, clip, m)

    elif mask != None:
        m = rekt_fast(clip, left=left, right=right, top=top, bottom=bottom,
                      fun=mask)
        deband = rekt_fast(clip, left=left, right=right, top=top, bottom=bottom,
                           fun=lambda x: core.f3kdb.Deband(x, range=range, y=y, cb=cb, cr=cr,
                                                           grainy=grainy, grainc=grainc, sample_mode=sample_mode,
                                                           seed=seed,
                                                           blur_first=blur_first, dynamic_grain=dynamic_grain,
                                                           opt=opt, dither_algo=dither_algo,
                                                           keep_tv_range=keep_tv_range,
                                                           output_depth=output_depth, random_algo_ref=random_algo_ref,
                                                           random_param_ref=random_param_ref,
                                                           random_param_grain=random_param_grain,
                                                           preset=preset))
        return core.std.MaskedMerge(deband, clip, m)
    else:
        return rekt_fast(clip, left=left, right=right, top=top, bottom=bottom,
                         fun=lambda x: core.f3kdb.Deband(x, range=range, y=y, cb=cb, cr=cr,
                                                         grainy=grainy, grainc=grainc, sample_mode=sample_mode,
                                                         seed=seed,
                                                         blur_first=blur_first, dynamic_grain=dynamic_grain,
                                                         opt=opt, dither_algo=dither_algo, keep_tv_range=keep_tv_range,
                                                         output_depth=output_depth, random_algo_ref=random_algo_ref,
                                                         random_param_ref=random_param_ref,
                                                         random_param_grain=random_param_grain,
                                                         preset=preset))


'''
Tool to highlight black lines on borders and place them in the middle.
Such lines should then create a straight line or even a cross if horizontal and vertical lines line up accordingly.
The threshold is set for very dark black lines, so it has to be adjusted for detecting dirty lines.
There are also only default values for one or two byte depths.

Optional "fix" included.  It's definitely recommended to do this manually, though.
The fix depends on FillBorders and applies it to the highlighted areas on every clip.
This can potentially damage unaffected areas.
I might write a protect for this eventually, but I only really care about the detection, not the fix.
'''


def black_detect(clip, thresh=None, fix=False, left=0, right=0, top=0, bottom=0):
    if thresh == None:
        if clip.format.bits_per_sample == 8:
            thresh = 25
        elif clip.format.bits_per_sample == 16:
            thresh = 5000
        else:
            raise TypeError("black_detect: thresh argument required for bit depths outside 8 and 16.")
    if fix == False:
        mask = core.std.ShufflePlanes(clip, 0, vs.GRAY).std.Binarize(
            "{0}".format(thresh)).std.Invert().std.Maximum().std.Inflate().std.Maximum().std.Inflate()
        l = core.std.Crop(mask, right=clip.width / 2)
        r = core.std.Crop(mask, left=clip.width / 2)
        mask_test = core.std.StackHorizontal([r, l])
        t = core.std.Crop(mask_test, top=clip.height / 2)
        b = core.std.Crop(mask_test, bottom=clip.height / 2)
        mask_test = core.std.StackVertical([t, b])
        return mask_test
    else:
        mask = core.std.ShufflePlanes(clip, 0, vs.GRAY).std.Binarize("{0}".format(thresh)).std.Invert()
        fb = core.fb.FillBorders(clip, left=left, right=right, top=top, bottom=bottom)
        return core.std.MaskedMerge(clip, fb, mask)


'''
Stupid downscaling that should automatically calculate the correct width and height.
'''


def ds(clip, size=720, sar=16 / 9):
    ar = clip.width / clip.height
    if ar > (sar):
        width = size * ar
        height = size
        w = round((width * ar) / 2) * 2
        h = round((height * (1 / ar)) / 2) * 2
    if ar < (sar):
        width = size * (sar ** (-1))
        height = size * ar
        w = round((width * ar) / 2) * 2
        h = round((height * (1 / ar)) / 2) * 2
    return core.resize.Spline36(clip, w, h)

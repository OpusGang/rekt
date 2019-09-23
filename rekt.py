from vapoursynth import core
import vapoursynth as vs


def rekt(src, fix, left=0, top=0, right=0, bottom=0):
    '''Creates a rectangular "mask" for a fix to be applied to.'''

    if left > 0 or right > 0:
        m = core.std.Crop(fix, left=left, right=right)
        l = core.std.Crop(src, right=src.width - left) if left > 0 else 0
        r = core.std.Crop(src, left=src.width - right) if right > 0 else 0
        params = [x for x in [l, m, r] if x != 0]
        m = core.std.StackHorizontal(params)
    else:
        m = fix
    if top > 0 or bottom > 0:
        t = core.std.Crop(src, bottom=src.height - top) if top > 0 else 0
        m = core.std.Crop(m, bottom=bottom, top=top)
        b = core.std.Crop(src, top=src.height - bottom) if bottom > 0 else 0
        params = [x for x in [t, m, b] if x != 0]
        m = core.std.StackVertical(params)
    return m


def rekt_fast(src, fun=lambda x: x, left=0, top=0, right=0, bottom=0):
    '''Creates a rectangular "mask" in which a fix is applied to only the masked area.
    This vastly speeds up filters like anti-aliasing and scaling.
    This wrapper works with a lambda function called m, which is applied to the "m" clip later on:
    
    rekt_fast(src, fun=lambda m: taa.TAAmbk(m, aatype=3, preaa=-1, strength=-1, mtype=2), left=2, right=8, top=10, bottom=2)
    
    Results in the following function being applied to only the masked rectangle:
    
    def f(m):
        return taa.TAAmbk(m, aatype=3, preaa=-1, strength=-1, mtype=2)'''
    m = core.std.Crop(src, left=left, right=right)
    if left > 0 or right > 0:
        m = fun(m.std.Crop(top=top, bottom=bottom)).std.AddBorders(top=top, bottom=bottom)
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


def rektaa(clip, left=0, top=0, right=0, bottom=0, aatype=3, aatypeu=None, aatypev=None, preaa=0, strength=0, cycle=0,
           mtype=None, masktype=None, mclip=None,
           mthr=None, mthr2=None, mlthresh=None, mpand=(1, 0), txtmask=0, txtfade=0, thin=0, dark=0.0, sharp=0,
           aarepair=0, postaa=None, src=None, stabilize=0, down8=True, showmask=0, opencl=False, opencl_device=0):
    '''Anti-aliasing alias for fast_rekt with vsTAAmbk.'''
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


def rektdb(clip, left=0, top=0, right=0, bottom=0,
           range=15, y=48, cb=0, cr=0,
           grainy=15, grainc=0, sample_mode=2, seed=None,
           blur_first=True, dynamic_grain=True,
           opt=-1, dither_algo=3, keep_tv_range=False,
           output_depth=16, random_algo_ref=1, random_param_ref=1, random_param_grain=1,
           preset=None, mask='retinex', thry=40, thrc=None, radiusy=12, radiusc=8, mask_thr=2, mask_radius=2):
    '''De-banding alias.  Can use a lambda mask.  Default is retinex_edgemask from kagefunc.  Requires fvsfunc, fag3kdb, and kagefunc.'''
    if mask == 'retinex':
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

    elif mask == 'gradfun3' or mask == 'fag':
        from fag3kdb import fag3kdb 
        return rekt_fast(clip=clip,
                         fun=lambda x: fag3kdb(x, thry=thry, thrc=thrc, radiusy=radiusy, radiusc=radiusc, grainy=grainy,
                                               grainc=grainc, dynamic_grainy=dynamic_grain,
                                               dynamic_grainc=dynamic_grain, mask_thr=mask_thr, mask_radius=mask_radius,
                                               keep_tv_range=keep_tv_range))

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


def rektlvl(c, num, adj_val, type='row', prot_val=20, min=16, max=235):
    '''
    A rekt_fast version of havsfunc's FixBrightnessProtect2/FixBrightness.
    :param c: Clip to be processed.
    :param num: Row or column number.
    :param adj_val: Adjustment value; negative numbers darken, while positive numbers brighten. Between -100 and 100.
    :param type: Whether a row or a column is to be processed
    :param prot_val: Values above 255 - prot_val will not be processed. If 0, this will work like FixBrightness.
    :return: Clip with first plane's values adjusted by adj_val.
    '''
    from vsutil import get_y, plane
    from havsfunc import scale, cround
    core = vs.get_core()
    if (adj_val > 100 or adj_val < -100) and prot_val != 0:
        raise ValueError("adj_val must be between -100 and 100!")
    if c.format.color_family == vs.RGB:
        raise TypeError("RGB color family is not supported by rektlvls.")
    peak = (1 << c.format.bits_per_sample) - 1

    if c.format.color_family != vs.GRAY:
        c_orig = c
        c = get_y(c)
    else:
        c_orig = None
    if prot_val != 0:
        expr = f'x {scale(16, peak)} - {100 - adj_val} / 100 * {scale(16, peak)} + x {scale(255 - prot_val, peak)} - -10 / 0 max 1 min * x x {scale(245 - prot_val, peak)} - 10 / 0 max 1 min * +'
        last = lambda x: core.std.Expr(x, expr=expr)
    else:
        if adj_val < 0:
            last = lambda x: core.std.Levels(x, min_in=scale(min, peak), max_in=scale(max, peak),
                                             min_out=scale(min, peak), max_out=scale(max + adj_val, peak))
        elif adj_val > 0:
            last = lambda x: core.std.Levels(x, min_in=scale(min, peak), max_in=scale(max - adj_val, peak),
                                             min_out=scale(min, peak), max_out=scale(max, peak))
        else:
            last = lambda x: x
    if type is 'row':
        last = rekt_fast(c, last, bottom=c.height - num - 1, top=num)
    elif type is 'column':
        last = rekt_fast(c, last, right=c.width - num - 1, left=num)
    else:
        raise ValueError("Type must be 'row' or 'column'.")

    if c_orig is not None:
        last = core.std.ShufflePlanes([last, c_orig], planes=[0, 1, 2], colorfamily=c_orig.format.color_family)

    return last


def rektlvls(clip, rownum=None, rowval=None, colnum=None, colval=None, prot_val=20, min=16, max=235):
    '''
    Wrapper around rektlvl: a rekt_fast version of havsfunc's FixBrightnessProtect2.
    :param clip: Clip to be processed.
    :param rownum: Row(s) to be processed.
    :param rowval: Row adjustment value. Negatives darken, positives brighten. Values can be between -100 and 100.
    :param colnum: Column(s) to be processed.
    :param colval: Column adjustment value. Negatives darken, positives brighten. Values can be between -100 and 100.
    :param prot_val: Values above 255 - prot_val will not be processed. If 0, this will work like FixBrightness.
    :return: Clip with first plane's values adjusted by adj_val.
    '''
    if rownum is not None:
        if isinstance(rownum, int):
            rownum = [rownum]
        if isinstance(rowval, int):
            rowval = [rowval]
        for _ in range(len(rownum)):
            clip = rektlvl(clip, rownum[_], rowval[_], type='row', prot_val=prot_val, min=min, max=max)
    if colnum is not None:
        if isinstance(colnum, int):
            colnum = [colnum]
        if isinstance(colval, int):
            colval = [colval]
        for _ in range(len(colnum)):
            clip = rektlvl(clip, colnum[_], colval[_], type='column', prot_val=prot_val, min=min, max=max)
    return clip

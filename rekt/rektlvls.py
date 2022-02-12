import vapoursynth as vs
from vapoursynth import core
from rekt import rekt_fast


def _rektlvl(c, num, adj_val, alignment='row', prot_val=[16, 235], min_val=16, max_val=235):
    if adj_val == 0:
        return c
    from vsutil import get_y, scale_value
    core = vs.core

    if (adj_val > 100 or adj_val < -100) and prot_val:
        raise ValueError("adj_val must be between -100 and 100!")
    if c.format.color_family == vs.RGB:
        raise TypeError("RGB color family is not supported by rektlvls.")
    bits = c.format.bits_per_sample

    min_val = scale_value(min_val, 8, bits)
    max_val = scale_value(max_val, 8, bits)
    diff_val = max_val - min_val
    ten = scale_value(10, 8, bits)

    if c.format.color_family != vs.GRAY:
        c_orig = c
        c = get_y(c)
    else:
        c_orig = None

    if prot_val:
        adj_val = scale_value(adj_val * 2.19, 8, bits)
        if adj_val > 0:
            expr = f'x {min_val} - 0 <= {min_val} {max_val} {adj_val} - {min_val} - 0 <= 0.01 {max_val} {adj_val} - {min_val} - ? / {diff_val} * x {min_val} - {max_val} {adj_val} - {min_val} - 0 <= 0.01 {max_val} {adj_val} - {min_val} - ? / {diff_val} * {min_val} + ?'
        elif adj_val < 0:
            expr = f'x {min_val} - 0 <= {min_val} {diff_val} / {max_val} {adj_val} + {min_val} - * x {min_val} - {diff_val} / {max_val} {adj_val} + {min_val} - * {min_val} + ?'

        if isinstance(prot_val, int):
            prot_top = [scale_value(255 - prot_val, 8, bits), scale_value(245 - prot_val, 8, bits)]
            expr += f' x {prot_top[0]} - -{ten} / 0 max 1 min * x x {prot_top[1]} - {ten} / 0 max 1 min * +'
        else:
            prot_val = [scale_value(prot_val[0], 8, bits), scale_value(prot_val[1], 8, bits)]
            expr += f' x {prot_val[1]} - -{ten} / 0 max 1 min * x x {prot_val[1]} {ten} - - {ten} / 0 max 1 min * + {prot_val[0]} x - -{ten} / 0 max 1 min * x {prot_val[0]} {ten} + x - {ten} / 0 max 1 min * +'

        last = lambda x: core.std.Expr(x, expr=expr)
    else:
        adj_val = adj_val * (max_val - min_val) / 100
        if adj_val < 0:
            last = lambda x: core.std.Levels(x, min_in=min_val, max_in=max_val, min_out=min_val, max_out=max_val + adj_val)
        elif adj_val > 0:
            last = lambda x: core.std.Levels(x, min_in=min_val, max_in=max_val - adj_val, min_out=min_val, max_out=max_val)

    if alignment == 'row':
        last = rekt_fast(c, last, bottom=c.height - num - 1, top=num)
    elif alignment == 'column':
        last = rekt_fast(c, last, right=c.width - num - 1, left=num)
    else:
        raise ValueError("Alignment must be 'row' or 'column'.")

    if c_orig:
        last = core.std.ShufflePlanes([last, c_orig], planes=[0, 1, 2], colorfamily=c_orig.format.color_family)

    return last


def rektlvls(clip, rownum=None, rowval=None, colnum=None, colval=None, prot_val=[16, 235], min_val=16, max_val=235):
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
    if rownum:
        if isinstance(rownum, int):
            rownum = [rownum]
        if isinstance(rowval, int):
            rowval = [rowval]
        for _ in range(len(rownum)):
            if rownum[_] < 0:
                rownum[_] = clip.height + rownum[_]
            clip = _rektlvl(clip, rownum[_], rowval[_], alignment='row', prot_val=prot_val, min_val=min_val, max_val=max_val)
    if colnum:
        if isinstance(colnum, int):
            colnum = [colnum]
        if isinstance(colval, int):
            colval = [colval]
        for _ in range(len(colnum)):
            if colnum[_] < 0:
                colnum[_] = clip.width + colnum[_]
            clip = _rektlvl(clip, colnum[_], colval[_], alignment='column', prot_val=prot_val, min_val=min_val, max_val=max_val)
    return clip

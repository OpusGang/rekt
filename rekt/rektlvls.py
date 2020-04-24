import vapoursynth as vs
from vapoursynth import core

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

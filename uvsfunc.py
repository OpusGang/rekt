from vapoursynth import core
import vapoursynth as vs
  
'''    
Creates a rectangular "mask" for a fix to be applied to.  Cropped area must be mod 4 for YUV420 or mod 2 for YUV422.
'''
def rekt(src, fix, left=0, right=0, top=0, bottom=0):
	if src.format == vs.YUV420P8 or vs.YUV420P10 or vs.YUV420P12 or vs.YUV420P16 or vs.YUV420P32:
	    if src.width-left-right % 4 != 0 or src.height-top-bottom % 4 != 0:
			raise TypeError("rekt: fix height and width must be mod 4 if source clip's color space is YUV420.")
	if src.format == vs.YUV422P8 or vs.YUV422P10 or vs.YUV422P12 or vs.YUV422P16 or vs.YUV422P32:
	    if src.width-left-right % 4 != 0 or src.height-top-bottom % 2 != 0:
			raise TypeError("rekt: fix height and width must be mod 2 if source clip's color space is YUV422.")
	else:
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
Creates a rectangular "mask" in which a fix is applied to only the masked area.  This vastly speeds up filters like anti-aliasing and scaling.
Cropped area must be mod 4 for YUV420 or mod 2 for YUV422
This wrapper works with a lambda function called m, which is applied to the "m" clip later on:

rekt_fast(src, fun = lambda m: taa.TAAmbk(m, aatype=3, preaa=-1, strength=-1, masktype=2), left=2, right=8, top=10, bottom=2)

Results in the following function being applied to only the masked rectangle:

def f(m):
    return taa.TAAmbk(m, aatype=3, preaa=-1, strength=-1, masktype=2)
'''
def rekt_fast(src, fun=lambda x: x, left=0, right=0, top=0, bottom=0):
	if src.format == vs.YUV420P8 or vs.YUV420P10 or vs.YUV420P12 or vs.YUV420P16 or vs.YUV420P32:
	    if src.width-left-right % 4 != 0 or src.height-top-bottom % 4 != 0:
			raise TypeError("rekt_fast: fix height and width must be mod 4 if source clip's color space is YUV420.")
	if src.format == vs.YUV422P8 or vs.YUV422P10 or vs.YUV422P12 or vs.YUV422P16 or vs.YUV422P32:
	    if src.width-left-right % 4 != 0 or src.height-top-bottom % 2 != 0:
			raise TypeError("rekt_fast: fix height and width must be mod 2 if source clip's color space is YUV422.")
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
def rektaa(clip, left=0, right=0, top=0, bottom=0, aatype=3, aatypeu=None, aatypev=None, preaa=0, strength=-1, cycle=0, mtype=None, mclip=None,
           mthr=None, mthr2=None, mlthresh=None, mpand=(1, 0), txtmask=0, txtfade=0, thin=0, dark=0.0, sharp=0,
           aarepair=0, postaa=None, src=None, stabilize=0, down8=True, showmask=0, opencl=False, opencl_device=0):
	import vsTAAmbk as taa
	return rekt_fast(clip, left=left, right=right, top=top, bottom=bottom, fun=lambda x: taa.TAAmbk(x, aatype=aatype, aatypeu=aatypeu, aatypev=aatypev, preaa=preaa, strength=strength, cycle=cycle, mtype=mtype, mclip=mclip,
           mthr=mthr, mthr2=mthr2, mlthresh=mlthresh, mpand=mpand, txtmask=txtmask, txtfade=txtfade, thin=thin, dark=dark, sharp=sharp,
           aarepair=aarepar, postaa=postaa, src=src, stabilize=stabilize, down8=down8, showmask=showmask, opencl=opencl, opencl_device=opencl_device))

'''
Tool to highlight black lines on borders and place them in the middle. Such lines should then create a straight line or even a cross if horizontal and vertical lines line up accordingly.
The threshold is set for very dark black lines, so it has to be adjusted for detecting dirty lines.  There are also only default values for one or two byte depths.

Optional "fix" included.  It's definitely recommended to do this manually, though.
The fix depends on FillBorders and applies it to the highlighted areas on every clip.  This can potentially damage unaffected areas.
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
		mask = core.std.ShufflePlanes(clip, 0, vs.GRAY).std.Binarize("{0}".format(thresh)).std.Invert().std.Maximum().std.Inflate().std.Maximum().std.Inflate()
		l = core.std.Crop(mask, right=clip.width/2)
		r = core.std.Crop(mask, left=clip.width/2)
		mask_test = core.std.StackHorizontal([r, l])
		t = core.std.Crop(mask_test, top=clip.height/2)
		b = core.std.Crop(mask_test, bottom=clip.height/2)
		mask_test = core.std.StackVertical([t, b])
		return mask_test
	else:
		mask = core.std.ShufflePlanes(clip, 0, vs.GRAY).std.Binarize("{0}".format(thresh)).std.Invert()
		fb = core.fb.FillBorders(clip, left=left, right=right, top=top, bottom=bottom)
		return core.std.MaskedMerge(clip, fb, mask)

'''
Stupid downscaling that should automatically calculate the correct width and height.
'''
def ds(clip, size=720, sar=16/9):
    ar = clip.width / clip.height
    if ar > (sar):
    	width = size * ar
        height = size
    	w = round((width * ar) / 2) * 2
    	h = round((height * (1 / ar)) / 2) * 2
    if ar < (sar):
    	width = size * (sar**(-1))
        height = size * ar
    	w = round((width * ar) / 2) * 2
    	h = round((height * (1 / ar)) / 2) * 2
    return core.resize.Spline36(clip, w, h)
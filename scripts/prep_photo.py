"""Prep a portrait for ASCII conversion: bg removal + CLAHE + white composite."""
import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

SRC = sys.argv[1] if len(sys.argv) > 1 else r'E:\Varun B P Image.jpeg'
DST = 'data/source-prepped.png'

img = np.array(Image.open(SRC).convert('RGB'))
# head-and-shoulders crop (face reads better at README sizes)
h, w = img.shape[:2]
img = img[int(h * 0.03):int(h * 0.74), :]
fg = remove(img)  # RGBA, subject isolated
alpha = np.array(Image.fromarray(fg).split()[-1])
# tight crop to the subject bbox so the portrait fills the frame
ys, xs = np.where(alpha > 12)
if len(xs):
    m = 24
    fg = fg[max(0, ys.min() - m):ys.max() + m, max(0, xs.min() - m):xs.max() + m]
    alpha = np.array(Image.fromarray(fg).split()[-1]) / 255.0
else:
    alpha = alpha / 255.0
gray = cv2.cvtColor(np.array(Image.fromarray(fg).convert('RGB')), cv2.COLOR_RGB2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
boosted = clahe.apply(gray)
# percentile stretch: force real blacks and whites (flat-lit photos wash out)
p2, p98 = np.percentile(boosted, (2, 98))
stretched = np.clip((boosted.astype(np.float32) - p2) * 255.0 / max(1, p98 - p2), 0, 255).astype(np.uint8)
comp = (stretched * alpha + 255 * (1 - alpha)).astype(np.uint8)  # white backdrop
Image.fromarray(comp).save(DST)
print('wrote', DST)

# khung thân của mascot trong ảnh raw: (x0, y0, x1, y1) - phần cam lớn nhất, kéo xuống tới hết chân
import numpy as np
from scipy import ndimage

def body_box(rgb):
    a = np.asarray(rgb).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    orange = (r > 170) & (g > 80) & (g < 160) & (b > 40) & (b < 130) & (r - g > 50) & (g - b > 15)
    lab, _ = ndimage.label(ndimage.binary_opening(orange, iterations=2))
    main = lab == np.argmax(np.bincount(lab.ravel())[1:]) + 1
    ys, xs = np.nonzero(main)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    # chân bị viền đen tách khỏi thân: lấy pixel cùng màu thân, dò xuống cho tới khi hết (cho phép hở 25px viền)
    mean = a[main].mean(0)
    skin = (np.abs(a - mean).sum(-1) < 60)[:, x0:x1].sum(1) > (x1 - x0) * 0.01
    gap, y = 0, y1
    while y < len(skin) and gap < 25:
        gap = 0 if skin[y] else gap + 1
        y += 1
    return int(x0), int(y0), int(x1), int(y - gap)

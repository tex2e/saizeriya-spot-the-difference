
# サイゼリアの間違い探しを見つけるプログラム

import sys
import cv2
import numpy as np

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print('Usage: python main.py <filename.png>', file=sys.stderr)
    sys.exit(1)

img_src = cv2.imread('./%s' % filename, cv2.IMREAD_COLOR)

# 余白を取り除いたときに2つの画像が最も一致するような適切な余白（padding）の幅を見つける

img_diffs = []
for padding in range(10, 50):
    # 画像の余白を削除
    img = img_src[:, padding:-padding]

    # 画像を左右で分割する
    height, width, channels = img.shape[:3]
    img1 = img[:, :width//2]
    img2 = img[:, width//2:]

    # 2つの画像の差分を算出
    img_diff = cv2.absdiff(img2, img1)
    img_diff_sum = np.sum(img_diff)

    img_diffs.append((img_diff, img_diff_sum))

# 差分が最も少ないものを選ぶ
img_diff, _ = min(img_diffs, key=lambda x: x[1])


tmp = filename.split('.')
filename = '.'.join([tmp[0] + '-diff', *tmp[1:]])
cv2.imwrite('./%s' % filename, img_diff)

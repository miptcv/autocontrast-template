import sys, os.path, cv2, numpy as np
import math

class point(object):
    def __init__(self, I, J, color):
        self.H = I
        self.W = J
        self.col = color


def byCol_key(point):
    return point.col

def autocontrast(img: np.ndarray, white_percent: float, black_percent: float) -> np.ndarray:
    height = len(img)
    width = len(img[0])
    KEKmass = []
    KEKout = np.ones((height, width), dtype = int)
    for i in range(height):
        for j in range(width):
            KEKout[i][j] = -KEKout[i][j]
            KEKmass.append(point(i, j, img[i][j]))
    KEKsorted = sorted(KEKmass, key=byCol_key)

    passblack = math.ceil(height * width * black_percent)
    passwhite = height * width - math.ceil(height * width * white_percent)
    c = 0

    while (KEKsorted[c].col <= KEKsorted[passblack - 1].col):
        KEKout[KEKsorted[c].H][KEKsorted[c].W] = 0
        c = c + 1

    c1 = height * width - 1
    while (KEKsorted[c1].col >= KEKsorted[passwhite].col and c1 >= c):
        KEKout[KEKsorted[c1].H][KEKsorted[c1].W] = 255
        c1 = c1 - 1

    upperBound = img[KEKsorted[c1 + 1].H][KEKsorted[c1 + 1].W]
    lowerBound = img[KEKsorted[c - 1].H][KEKsorted[c - 1].W]
    kekMul =  255.0/(upperBound - lowerBound)

    for i in range(height):
        for j in range(width):
            if (KEKout[i][j] == -1):
                KEKout[i][j] = round((int(img[i][j]) - lowerBound) * kekMul)

    return KEKout
    pass


def main():
    assert len(sys.argv) == 5
    src_path, dst_path = sys.argv[1], sys.argv[2]
    white_percent, black_percent = float(sys.argv[3]), float(sys.argv[4])
    assert 0 <= white_percent < 1
    assert 0 <= black_percent < 1

    assert os.path.exists(src_path)
    img = cv2.imread(src_path, cv2.IMREAD_GRAYSCALE)
    assert img is not None

    result = autocontrast(img, white_percent, black_percent)
    cv2.imwrite(dst_path, result)


if __name__ == '__main__':
    main()
import numpy as np

def init(rows = 100, cols = 100):
    return np.arange(rows * cols).reshape(rows, cols)

def rules(out_img, in_img, time_step):
    print (type(in_img), len(in_img))
    for rr in range(in_img.shape[0]):
        for cc in range(in_img.shape[1]):
            out_img[rr,cc] += 1



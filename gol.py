import numpy as np
import automata_lib as al

def init(rows = 100, cols = 100):
    return np.zeros([rows,cols])


ALIVE = 1
DEAD = 0
def rules(out_img, in_img, time_step):
    # print (type(in_img), len(in_img))
    for rr in range(in_img.shape[0]):
        for cc in range(in_img.shape[1]):
            N = al.neighbors(in_img,[rr,cc])
            cur = N[1,1]
            N[1,1] = 5
            alive_count = len(N[N==1].flatten())

            # if alive_count == 3 or (rr == 4 and cc == 6):
            #     print(rr,cc, alive_count)
            #     print(N)

            # if cur == ALIVE and alive_count in (2, 3):

            if alive_count < 2:
                out_img[rr,cc] = DEAD
            elif ALIVE == cur and alive_count in (2,3):
                out_img[rr,cc] = ALIVE
            elif cur == DEAD and alive_count == 3:
                out_img[rr,cc] = ALIVE
            else:
                out_img[rr,cc] = DEAD
            N[1,1] = cur






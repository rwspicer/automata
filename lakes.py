import numpy as np
import automata_lib as al


AIR = 2
WATER = 0
SOIL = 3
ICE = 1


def init(rows = 100, cols = 100):
    grid = np.zeros([rows,cols])  + AIR
    grid[:60] = SOIL
    w = 25 + np.random.randint(0,20)
    center = 50
    # c_shift = np.random.randint(-1,2)
    for i in range(10,60)[::-1]:
        # print(i)
       
        if i > 55: 
            grid [i,center-w:center+w] = AIR
        else:
            grid [i,center-w:center+w] = WATER
        if np.random.random() > np.random.random():
            w -= 1
            # center += c_shift
    return grid



##http://cripe.ca/docs/proceedings/17/Comfort-Abdelnour-2013.pdf
def rules(out_img, in_img, time_step, **kwargs):

    FDD = 500
    if "FDD" in kwargs:
        FDD = kwargs["FDD"]
    alpha=2.7
    if "alpha" in kwargs:
        alpha = kwargs["alpha"]
    # print (type(in_img), len(in_img))
    cell_res = 1/10 #m or decimetes
    # alpha =  2.7 #windy lake no snow
    # FDD = 5000

    max_cm_thickness = alpha * np.sqrt(FDD)
    max_dm_thickness = max_cm_thickness * .1 #also cell thickness
    # print(max_dm_thickness)

    for rr in range(in_img.shape[0])[::-1]:
        for cc in range(in_img.shape[1]):
            N = al.neighbors(in_img,[rr,cc])
            cur = in_img[rr,cc]

            column = in_img[:,cc]
            thickness = len(column[column == ICE])
            # if cc == 50:
            #     print(column)

            #freeze cells
            if cur == WATER and ( (N[0] == AIR).any()  or (N[0] == ICE).any()) and thickness < max_dm_thickness and np.random.random() > .75:
                out_img[rr,cc] = ICE

            ## freeze surface water
            if cur == WATER and (N[2] == ICE).any() and np.random.random() > .05:
                out_img[rr,cc] = ICE

            # FREEZE surrounded cells
            if cur == WATER and len(N[N == ICE].flatten()) > 6:
                # print("ACT")
                out_img[rr,cc] = ICE

            # # base thaw # bubbly?
            # if cur == ICE and (N[2] == WATER).any() and thickness >= max_dm_thickness and np.random.random() > .75:
            #     out_img[rr,cc] = WATER

            if cur == ICE and N[2,1] == WATER and thickness > max_dm_thickness and np.random.random() > .75:
                out_img[rr,cc] = WATER
           

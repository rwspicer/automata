import numpy as np
import automata_lib as al


AIR = 0
WATER = 2
SOIL = 6 ## frozen soil
FROZEN_SOIL = 6 ## frozen soil
ICE = 1 #surface ICE



THAWED_SOIL = 5

GROUND_ICE = 3
SLUSH = 4

OTHER = 10


# WATER_LEVEL = 55
INIT_SOIL_LEVEL = 60

def init(rows = 100, cols = 100, water_level=55):
    grid = np.zeros([rows,cols])  + AIR
    grid[:INIT_SOIL_LEVEL] = SOIL
    w = 25 + np.random.randint(0,20)
    center = 50
    # c_shift = np.random.randint(-1,2)
    for i in range(10,60)[::-1]:
        # print(i)
        continue
       
        if i > water_level: 
            grid [i,center-w:center+w] = AIR
        else:
            grid [i,center-w:center+w] = WATER
        if np.random.random() > np.random.random():
            w -= 1
            # center += c_shift
    return grid

def in_water_gravity (rr, cc, N, out_img, WATER_LEVEL = 55):
    # in water gravity
    cur = N[1,1]
    if cur == THAWED_SOIL and N[2,1] ==  WATER and rr <= WATER_LEVEL:
        out_img[rr,cc] = WATER
        out_img[rr-1,cc] = THAWED_SOIL
    
    if cur == THAWED_SOIL and N[2,1] == WATER and rr > WATER_LEVEL:
        out_img[rr,cc] = AIR
        out_img[rr-1,cc] = THAWED_SOIL

    if cur == FROZEN_SOIL and (N[1] == np.array([WATER, FROZEN_SOIL, WATER])).all():
        out_img[rr,cc] = THAWED_SOIL

    if cur == WATER and rr > WATER_LEVEL:
        out_img[rr,cc] = AIR
    
    if cur == AIR and rr <= WATER_LEVEL:
        out_img[rr,cc] = WATER

    if cur == ICE and N[2,1] == AIR:
        out_img[rr,cc] = AIR

def freezing_rules (rr, cc, in_img, out_img, params = {}):

    max_dm_thickness = params["max_dm_it"]
    # print("max", max_dm_thickness)
    N = al.neighbors(in_img,[rr,cc])
    cur = in_img[rr,cc]
    column = in_img[:,cc]
    thickness = len(column[column == ICE])
    # if cc == 50:
    #     print(column)

    # ICE WEDGES
    if cur == GROUND_ICE and np.random.random() > .8 and (in_img[:rr,cc] != WATER).any():
        out_img[rr-1,cc] = GROUND_ICE
    
    if cur == GROUND_ICE and N[0,1] in (THAWED_SOIL, FROZEN_SOIL) and np.random.random() > .99 and (in_img[:rr,cc] != WATER).any():
        # print("uplift")
        out_img[rr+1,cc] = GROUND_ICE

        rix = min(np.where(in_img[:,cc] == AIR)[0])
        out_img[rix, cc] = THAWED_SOIL
        rix = min(np.where(in_img[:,cc+1] == AIR)[0])
        out_img[rix, cc+1] = THAWED_SOIL
        rix = min(np.where(in_img[:,cc-1] == AIR)[0])
        out_img[rix, cc-1] = THAWED_SOIL
    
    if cur == GROUND_ICE and N[0,1] in (THAWED_SOIL, FROZEN_SOIL) and np.random.random() > .95 and (in_img[:rr,cc] != WATER).any():
        s = cc
        e = cc
        while in_img[rr, s] == GROUND_ICE:
            s -=1
        while in_img[rr, e] == GROUND_ICE:
            e +=1
        dist = e - s

        if dist < 10:   
            out_img[rr,cc + 1 ] = GROUND_ICE
            out_img[rr,cc - 1 ] = GROUND_ICE

    # if cur == THAWED_SOIL and  N[0,0] == AIR and N[0,2] == AIR:
    #     out_img[rr, cc] = 

    # if cur == GROUND_ICE and N[0,1] in (THAWED_SOIL, FROZEN_SOIL) and np.random.random() > .9 :
    #     out_img[rr+1,cc] = GROUND_ICE
    #     out_img[rr+2,cc] = DISPLACED
    #     out_img[rr+2,cc - 1] = DISPLACED
    #     out_img[rr+2,cc + 1] = DISPLACED

    # if cur == FROZEN_SOIL and N[2,1] == DISPLACED:
    #     out_img[rr,cc] = DISPLACED
    #     out_img[rr-1,cc] = FROZEN_SOIL

    # if cur == THAWED_SOIL and N[2,1] == DISPLACED:
    #     out_img[rr,cc] = DISPLACED
    #     out_img[rr-1,cc] = THAWED_SOIL

    # if cur == DISPLACED and N[0,1] == AIR:
    #     out_img[rr+1,cc] = THAWED_SOIL





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


    ### soil
    if cur == THAWED_SOIL and N[0,1] in (AIR,FROZEN_SOIL, ICE, GROUND_ICE) and not (in_img[rr:,cc] == WATER).any() and np.random.random() > (1 - .75):
        out_img[rr,cc] = FROZEN_SOIL
    # if cur == OTHER:
    #     out_img[rr,cc] = FROZEN_SOIL

    if cur == SLUSH:
        out_img[rr,cc] = GROUND_ICE

    in_water_gravity (rr, cc, N, out_img, params['water_level'])

    if thickness >= max_dm_thickness or (len(np.where(in_img == WATER)[0]) < 25 and len(np.where(in_img == THAWED_SOIL)[0]) < 25 ):
        return 1
    else:
        return 0

def thawing_rules (rr, cc, in_img, out_img, params = {}):
    """
    """
    ul_depth = 20
    max_dm_depth = params["max_dm_td"]
    N = al.neighbors(in_img,[rr,cc])
    cur = in_img[rr,cc]
    column = in_img[:,cc]
    thickness = len(column[column == THAWED_SOIL])
    # print('t', thickness, max_dm_depth, thickness > max_dm_depth)
    if cur == ICE:
        out_img[rr,cc] = OTHER
    if cur == OTHER:
        out_img[rr,cc] = WATER

    # if cur == FROZEN_SOIL and len(N[N == THAWED_SOIL]):
    #     out_img[rr,cc] = THAWED_SOIL

    if cur == SOIL and (N[0] == AIR).any():
        out_img[rr,cc] = THAWED_SOIL
    
    if cur == SOIL and (N[0] == THAWED_SOIL).any() and thickness < max_dm_depth and np.random.random() > .75:
        out_img[rr,cc] = THAWED_SOIL

    if cur == SOIL and (in_img[rr:,cc] == WATER).any() and ((N[0] == THAWED_SOIL).any() or (N[0] == WATER).any()) and np.random.random() > .75 and thickness < ul_depth:
        out_img[rr,cc] = THAWED_SOIL

    if cur == SOIL and ((N[:,0] == WATER).any() or (N[:,2] == WATER).any()) and np.random.random() > .75 and thickness < ul_depth:
        out_img[rr,cc] = THAWED_SOIL

    ## in water EROSION

    ## Soil thaws under water
    if cur == FROZEN_SOIL and N[1,0] == WATER:
        out_img[rr,cc] = THAWED_SOIL

    
    # right side Erosion
    if cur == THAWED_SOIL and N[1,0] == WATER and np.random.random() > .75:
        out_img[rr,cc] = WATER
        out_img[rr,cc-1] = THAWED_SOIL

    # left side Erosion
    if cur == THAWED_SOIL and N[1,2] == WATER and np.random.random() > .75:
        out_img[rr,cc] = WATER
        out_img[rr,cc+1] = THAWED_SOIL

    in_water_gravity (rr, cc, N, out_img, params['water_level'])

    #above water erosion
    # right side Erosion
    right_erosion = False

    if cur == THAWED_SOIL and N[1,0] == AIR and np.random.random() > .75:# and rr < INIT_SOIL_LEVEL:
        out_img[rr,cc] = AIR
        out_img[rr,cc-1] = THAWED_SOIL
        right_erosion = True

    # left side Erosion
    if cur == THAWED_SOIL and N[1,2] == AIR and np.random.random() > .75:# and rr < INIT_SOIL_LEVEL:
        out_img[rr,cc] = AIR
        out_img[rr,cc+1] = THAWED_SOIL


    if cur == AIR and N[0,1] in (FROZEN_SOIL, THAWED_SOIL):
        out_img[rr,cc] = THAWED_SOIL
        out_img[rr+1,cc] = AIR


    if cur == GROUND_ICE and len(N[N==THAWED_SOIL]) >= 3:
        out_img[rr,cc] = SLUSH

    if cur == GROUND_ICE and len(N[N==SLUSH]) >= 3:
        out_img[rr,cc] = SLUSH

    if cur in (SLUSH, GROUND_ICE) and (len(N[N==SLUSH]) + len(N[N==THAWED_SOIL]) + len(N[N==AIR]) + len(N[N==WATER])) == 8:
        out_img[rr,cc] = WATER

    if cur == SLUSH and len(N[N==WATER]) > 1:
        out_img[rr,cc] = WATER

    
    

    if thickness >= max_dm_depth:
        return 0
    else:
        return 1

##http://cripe.ca/docs/proceedings/17/Comfort-Abdelnour-2013.pdf
def rules(out_img, in_img, time_step, **kwargs):

    FDD = 500
    if "FDD" in kwargs:
        FDD = kwargs["FDD"]

    TDD = 500
    if "TDD" in kwargs:
        TDD = kwargs["TDD"]

    alpha=2.7
    if "alpha" in kwargs:
        alpha = kwargs["alpha"]
    # print (type(in_img), len(in_img))
    cell_res = 1/10 #m or decimetes
    # alpha =  2.7 #windy lake no snow
    # FDD = 5000

    stage = 0
    if "stage" in kwargs:
        stage = kwargs["stage"]



    max_cm_thickness = alpha * np.sqrt(FDD)
    max_dm_thickness = max_cm_thickness * .1 #also cell thickness
    # print(max_dm_thickness)

    max_cm_depth = alpha * np.sqrt(TDD)
    max_dm_depth = max_cm_depth * .1 #also cell thickness
    # print(max_dm_thickness)

    rv_grid = np.zeros(in_img.shape)
    for rr in range(in_img.shape[0])[::-1]:
        for cc in range(in_img.shape[1]):
            N = al.neighbors(in_img,[rr,cc])
            if N[0,0] == N[0,1] == N[0,2] == \
               N[1,0] == N[1,1] == N[1,2] == \
               N[2,0] == N[2,1] == N[2,2]:  
                continue
            if stage == 0:
                rv_grid[rr,cc] = freezing_rules(
                    rr, cc, in_img, out_img, params={
                        "max_dm_it": max_dm_thickness,
                        "water_level": kwargs['water_level']
                })
            else: 
                rv_grid[rr,cc] = thawing_rules(
                    rr, cc, in_img, out_img, params= {
                        "max_dm_td": max_dm_depth,
                        "water_level": kwargs['water_level']
                })
            
    # print( len(out_img.flatten()[out_img.flatten() == WATER]) )
    if (rv_grid == 1).any():
        stage = 1
    else:
        stage = 0

    return {"stage":stage}

            

            
           

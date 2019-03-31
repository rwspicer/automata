import numpy as np
from numba import njit
import scipy.misc

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, ColorBar, LinearColorMapper,Ticker, FreehandDrawTool
from bokeh.palettes import gray,viridis
from bokeh.plotting import figure



import numpy as np
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh import events
from bokeh.models import CustomJS, Div, Button
from bokeh.layouts import column, row

# print(Slider)


ROW, COL = 0, 1

PERMAFROST = 2
ICE = 3
WATER = 4
AIR = 0
SOIL = 1
FROST_HEAVE = 5

def setup():
    a = np.zeros([100,100])
    a[50:] = SOIL

    a[60:] = PERMAFROST
    # a[49:75, 25:26] = ICE

    # a[46:60, 80] = ICE
    a[59, 80] = ICE

    
    return a
# image = scipy.misc.ascent().astype(np.int32)[::-1, :]
image = setup()[::-1]
h, w = image.shape

source = ColumnDataSource(data=dict(image=[image.reshape([100,100])]))
# source.add([[]], "xs")
# source.add([[]], "ys")
# print(type(source), source.data['image'][0])

# TOOLTIPS = [
#     ('index', "$index"),
#     ('pattern', '@pattern'),
#     ("x", "$x"),
#     ("y", "$y"),
#     ("value", "@image"),
#     ('squared', '@squared')
# ]


p = figure(x_range=(0, w), y_range=(0, h), plot_width=w*5 +75, plot_height=h*5)#, tooltips=TOOLTIPS)#, tools=[tool,])

print(source.data)
# r = p.image('image', 'xs','ys', w + 10, h + 10, source=source)
# tool = FreehandDrawTool(renderers=[r])
# p.add_tools(tool)

# renderer = p.multi_line([[1, 9]], [[5, 5]])

# draw_tool = FreehandDrawTool(renderers=[renderer], num_objects=3)
# p.add_tools(draw_tool)

color_mapper = LinearColorMapper(palette="Viridis256", high=5, low=0)



p.image('image', x=0, y=0, dw=w, dh=h, source=source, color_mapper=color_mapper)


color_bar = ColorBar( color_mapper=color_mapper, label_standoff=12, border_line_color=None, location=(0,1) )
# curdoc().add_root(column(p, color_bar))

p.add_layout(color_bar, 'right')


point_attributes = ['x','y','sx','sy']                     # Point events
pan_attributes = point_attributes + ['delta_x', 'delta_y'] # Pan event


style = 'float:left;clear:left;font_size=10pt'
jscb = CustomJS(args=dict(source=source), code="""


        var attrs = %s; var args = [];
        if (source != "null") {

            var data = source.data;
            var img = data['image'][0]
            console.log(img.length)
            x =  Math.floor(Number(cb_obj[attrs[0]]))
            y =  Math.floor(Number(cb_obj[attrs[1]]))

            if (x < 100 && x >= 0 && x < 100 && x >= 0){
                if (img.length == 100) {
                    img[y][x] = 3
                } else {
                    img[x  +y* 100] = 3
                }
            }
    
            
            source.change.emit();
            source.data = data;
        
        }
        
        
    """% (pan_attributes,))
p.js_on_event(events.Pan,jscb)


# @njit
def neighbors(grid, idx):
    if 0 < idx[ROW] < grid.shape[ROW]-1 and  0 < idx[COL] < grid.shape[COL]-1:
#         print('totaly in bounds')
        return grid[idx[ROW]-1:idx[ROW]+2,idx[COL]-1:idx[COL]+2]
    # special cases
    hood = np.zeros([3,3]) - 1
    if idx == [0,0]:
#         print ("top left corner")
        hood[1:,1:] = grid[:idx[ROW]+2,:idx[COL]+2]
    elif idx == [0,grid.shape[COL]-1]:
#         print("top right corner")
        hood[1:,:-1] = grid[:idx[ROW]+2,idx[COL]-1:idx[COL]+2]
    elif idx == [grid.shape[ROW]-1,0]:
#         print ("bottom left corner")
        hood[:-1,1:] = grid[idx[ROW]-1:,:idx[COL] +2]
    elif idx == [grid.shape[ROW]-1,grid.shape[COL]-1]:
#         print ("bottop right corner")
        hood[:-1,:-1] = grid[idx[ROW]-1:,idx[COL]-1:]
    elif idx[ROW] == 0:
#         print('top')
        hood[1:,:] = grid[idx[ROW]:idx[ROW]+2,idx[COL]-1:idx[COL]+2]
    elif idx[COL] == 0:
#         print('left')
        hood[:,1:] = grid[idx[ROW]-1:idx[ROW]+2,0:idx[COL]+2]
    elif idx[COL] == grid.shape[COL] - 1:
#         print('right')
        hood[:,:-1] = grid[idx[ROW]-1:idx[ROW]+2,idx[COL]-1:]
    elif idx[ROW] == grid.shape[ROW] - 1:
#         print('bottom')
        hood[:-1,:] = grid[idx[ROW]-1:,idx[COL]-1:idx[COL]+2]
    else:
#         print ("out of bounds")
        hood[:] = np.nan
    return hood



T = 2
M = 1
B = 0

L = 2
R = 0
 
# @njit
def blur(out, image):
    for rr in range(image.shape[0]):
        for cc in range(image.shape[1]):
            if cc >= 99 or rr >= 99:
                continue
            n = neighbors(image,[rr,cc])
           
            # if n[1,1] == 0 and (n == 3).any():
            #     out[rr,cc] = SOIL


            # if n[M,M] == ICE and n[T,M] == SOIL:
            #     out[rr,cc] = ICE
            if n[M,M] == SOIL and n[B,M] == AIR:
                out[rr,cc] = AIR
                out[rr-1,cc] = SOIL

            if n[M,M] == SOIL and n[B,L] == AIR:
                out[rr,cc] = AIR
                out[rr-1,cc-1] = SOIL
            


            if n[M,M] == SOIL and (n[B,:] == ICE).all(): #and np.random.rand() > .99:
                out[rr,cc] = ICE
                if out[rr+1,cc] == SOIL:
                    out[rr+1,cc] = FROST_HEAVE

            if n[M,M] in (PERMAFROST,) and n[M,L] == ICE:# and np.random.rand() > .99:
                c = 1
                while out[rr,cc-c] == ICE:
                    c += 1
                if c < 10:
                    out[rr,cc] = ICE
                if out[rr+1,cc] == SOIL:
                    out[rr+1,cc] = FROST_HEAVE
            if n[M,M] in ( PERMAFROST,) and n[M,R] == ICE:# and np.random.rand() > .99:
                c = 1
                while out[rr,cc+c] == ICE:
                    c += 1
                if c < 10:
                    out[rr,cc] = ICE
                if out[rr+1,cc] == SOIL:
                    out[rr+1,cc] = FROST_HEAVE
            # if ((n[1,0] == 3).any() or (n[1,-1] == 3).any()) and (neighbors(image,[rr-1,cc]) == 0).any() and np.random.rand() > .9:
            #     out[rr,cc] = 3
            #     if out[rr+1,cc] == SOIL:
            #         out[rr+1,cc] = FROST_HEAVE

            if n[M,M] in (PERMAFROST, SOIL) and n[T,M] == ICE and np.random.rand() > .95:
                out[rr,cc] = ICE
                # if out[rr+1,cc] == SOIL:
                #     out[rr+1,cc] = FROST_HEAVE
            
            if n[M,M] == AIR and n[B,M] == SOIL and  (image[:rr,cc] == FROST_HEAVE).any()  :
                out[rr,cc] = SOIL
            if n[M,M] == FROST_HEAVE:
                out[rr,cc] = SOIL

IMAGE = image
import copy
#def update(attr, old, new):
def update(event):

    if type(source.data['image'][0]) is dict:
        fixed = np.array(list(source.data['image'][0].values())).reshape([100,100])
        # print(fixed)
        #
        source.data.update(image=[fixed])

    # if type(source.data['image'][0]) is list:
    #     fixed = []
    #     for l in source.data['image'][0][:100]:
    #         # for s in l:
    #         #     print(s, '\n')
    #         fixed.append(list(l))
    #     print(len(fixed))
    #     fixed = np.array(fixed)#.reshape([100,100])

    #     print(fixed)
    #     # fixed = np.array(source.data['image'][0][:100]).reshape([100,100])
    # #     fixed = np.array(source.data['image'][0][:100]).reshape([100,100])
    # #     # fixed = np.array(list(source.data['image'][0].values())).reshape([100,100])
    # #     # print(fixed)
    # #     # #
    #     source.data.update(image=[fixed])
    
    # if type(source.data['image'][0]) is tuple:
    #     print(np.array(source.data['image'][0]).shape)
    

    out = source.data['image'][0].copy()
    # print(source.data['image'])
  
    blur(out, source.data['image'][0])
    source.data.update(image=[out])



curdoc().title = "Image Blur"


div = Div(width=1000)
button = Button(label="Button", button_type="success")
layout = column(button, row(p, div))#, slider)


## Events with no attributes
button.on_event(events.ButtonClick, update) # Button click





# ## Events with attributes



curdoc().add_root(layout)

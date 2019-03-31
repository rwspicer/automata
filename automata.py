import numpy as np
from numba import njit
import scipy.misc

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, ColorBar, LinearColorMapper,Ticker, SaveTool,CategoricalColorMapper
from bokeh.palettes import gray,viridis, Spectral5
from bokeh.plotting import figure



import numpy as np
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh import events
from bokeh.models import CustomJS, Div, Button
from bokeh.layouts import column, row


import importlib

TIME_STEP = 0

def setup(rows, cols, rules):
    
    init_img = rules.init()
    source = ColumnDataSource(data=dict(image=[np.array(init_img)]))
    

    h, w = init_img.shape
    p = figure(
        x_range=(0, w), y_range=(0, h),
        plot_width=w*5 +75, plot_height=h*5,
        tools = [SaveTool()]
    )#, tooltips=TOOLTIPS)#, tools=[tool,])

    color_mapper = LinearColorMapper(palette="Spectral5", high=5, low=0)
    # color_mapper = CategoricalColorMapper(palette=["white", "brown", "blue", "green"], factors=[0, 1,2,3])
    p.image('image', x=0, y=0, dw=w, dh=h, source=source, color_mapper=color_mapper)
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12, border_line_color=None, location=(0,1) )
    p.add_layout(color_bar, 'right')

    p.toolbar.logo = None
    # p.toolbar_location = None
    return p, source



def add_drawing(p, ink=1):
    point_attributes = ['x','y','sx','sy']                     # Point events
    pan_attributes = point_attributes + ['delta_x', 'delta_y'] # Pan event
    jscb = CustomJS(args=dict(source=source), code="""


            var attrs = %s; var args = [];
            if (source != "null") {

                var data = source.data;
                var img = data['image'][0]
                // console.log(img.length)
                x =  Math.floor(Number(cb_obj[attrs[0]]))
                y =  Math.floor(Number(cb_obj[attrs[1]]))

                if (x < 100 && x >= 0 && x < 100 && x >= 0){
                    if (img.length == 100) {
                        img[y][x] = %r
                    } else {
                        img[x  +y* 100] = %r
                    }
                }
        
                
                source.change.emit();
                source.data = data;
            
            }
            
        """% (pan_attributes, ink, ink))
    p.js_on_event(events.Pan,jscb)

#def update(attr, old, new):
def time_step(event):

    if type(source.data['image'][0]) is dict:
        fixed = np.array(list(source.data['image'][0].values())).reshape([100,100])
        # print(fixed)
        #
        source.data.update(image=[fixed])

    out = np.array(source.data['image'][0].copy())
    
    # print(type(out), len(out))
    # print(type(source.data['image'][0]), len(source.data['image'][0]))
  

    FDD= mutable_values.data['FDD'][0]
    alpha = mutable_values.data['alpha'][0]
    rules.rules(out, np.array(source.data['image'][0]), time_step = 1, alpha=alpha, FDD=FDD  )
    source.data.update(image=[out])


def update_fdd(attr, old, new):
    mutable_values.data.update(FDD=[new])


def update_alpha(attr, old, new):
    mutable_values.data.update(alpha=[new])



def s_reset(event):
    source.data.update(image=[rules.init()])


def automata (p, rules):


    curdoc().title = "Image Blur"
    div = Div(width=1000)
    step = Button(label="Step", button_type="success")
    reset = Button(label="Reset", button_type="success")

    fslider = Slider(title="FDD", start=0, end=10000, value=500)
    fslider.on_change('value', update_fdd)
    aslider = Slider(title="alpha", start=0, end=5, value=2.5)
    aslider.on_change('value', update_alpha)

    layout = column(row(step, reset), row(p, div), fslider, aslider)



    ## Events with no attributes
    step.on_event(events.ButtonClick, time_step) # Button click
    reset.on_event(events.ButtonClick, s_reset) # Button click
    curdoc().add_root(layout)


# import sys
# args = sys.argv

rules_mod = 'lakes'
rules = importlib.__import__(rules_mod)
p, source = setup(100,100,rules)

mutable_values = ColumnDataSource(data=dict(FDD=[500],alpha=[2.5]))



add_drawing(p)
automata(p,rules)





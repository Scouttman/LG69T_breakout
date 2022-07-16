# cd /home/scouttman/my_stuff/old/GPS/LG69T/LG69T_breakout
""" Script to generate a kicad pcb heater block of a given size """
"""
cd my_stuff/old/GPS/LG69T
import LG69T_footprint
import importlib
def gen():
    importlib.reload(LG69T_footprint)
"""

import sys
sys.path
sys.path.append('/home/scouttman/my_stuff/old/GPS/kicad-footprint-generator')
from KicadModTree import *
import numpy as np

footprint_name = "LG69T"
width = 18.1
hight = 22

# init kicad footprint
kicad_mod = Footprint(footprint_name)
kicad_mod.setDescription("LG69T CPS")
kicad_mod.setTags("LG69T")

# set general values
kicad_mod.append(Text(type='reference', text='REF**', at=[0, -hight/2-2], layer='F.SilkS'))
kicad_mod.append(Text(type='value', text=footprint_name, at=[1.5, hight/2+2], layer='F.Fab'))


# create silkscreen
kicad_mod.append(RectLine(start=[-width/2, -hight/2], end=[width/2, hight/2], layer='F.SilkS'))

# create courtyard
kicad_mod.append(RectLine(start=[-width/2-0.25, -hight/2-0.25], end=[width/2+0.25, hight/2+0.25], layer='F.CrtYd'))

global current_count
current_count = 1
def pad_array(locs, pin_num_in = None, **pad_params):
    global current_count
    for i in range(locs.shape[0]):
        # create pads
        if(pin_num_in is None):
            pin_num = current_count+i
        else:
            pin_num = pin_num_in
        kicad_mod.append(Pad(number=pin_num, at=[locs[i,0], locs[i,1]], **pad_params))
    current_count += i+1
# kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
#                      at=[3, 0], size=[2, 2], drill=1.2, layers=Pad.LAYERS_THT))

# # add model
# kicad_mod.append(Model(filename="example.3dshapes/example_footprint.wrl",
#                        at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

# ground pads
pad_params_side = {"type":Pad.TYPE_SMT, "shape":Pad.SHAPE_RECT,
                             "size":[1.5, 0.8], "layers":Pad.LAYERS_SMT}
pad_params_vert = {"type":Pad.TYPE_SMT, "shape":Pad.SHAPE_RECT,
                             "size":[0.8, 1.5], "layers":Pad.LAYERS_SMT}

#left 
x = -width/2+1.05
locs = np.zeros((14,2))
locs[:,0] = x
locs[:,1] = (np.arange(-7,7)+0.5)*1.1
pad_array(locs, **pad_params_side)

# bottom
y = hight/2-1.05
locs = np.zeros((13,2))
locs[:,0] = (np.arange(-6,7))*1.1
locs[:,1] = y
pad_array(locs, **pad_params_vert)

# right
x = width/2-1.05
locs = np.zeros((14,2))
locs[:,0] = x
locs[:,1] = (np.flip(np.arange(-7,7))+0.5)*1.1
pad_array(locs, **pad_params_side)

#top
y = -hight/2+1.05
locs = np.zeros((13,2))
locs[:,0] = (np.flip(np.arange(-6,7)))*1.1
locs[:,1] = y
pad_array(locs, **pad_params_vert)

# ground pads
pad_params = {"type":Pad.TYPE_SMT, "shape":Pad.SHAPE_RECT,
                             "size":[1.1, 1.1], "layers":Pad.LAYERS_SMT}
x = np.arange(-3, 3)*2.1+2.1/2
y = np.arange(-4, 4,)*2.1+2.1/2
x, y = np.meshgrid(x, y)
locs = np.vstack((x.flatten(),y.flatten())).T
print(locs.shape)
pad_array(locs, pin_num_in=55, **pad_params)
    


# output kicad model
file_handler = KicadFileHandler(kicad_mod)
file_handler.writeFile('LG69T.kicad_mod')

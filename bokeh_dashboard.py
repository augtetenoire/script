#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import vaspfric as vfric
# from joblib import Parallel, delayed
# import multiprocessing
import pandas as pd

from bokeh.plotting import figure, show
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, ColumnDataSource, CustomJS, Select, RangeSlider, Switch, Range1d, LinearAxis, Legend
# from bokeh.models import Div, , Spinner
from bokeh.layouts import layout, row
from bokeh.io import curdoc

gaussian_width = 5


sheets = pd.read_excel('/Users/atetenoire/Documents/Post_doc/experimental_data_Au111_calix_acid/dataRamanNR.xlsx', sheet_name=None)

keys = list(sheets.keys())
# y2_max = 0
for key in keys:
    # if max(sheets[key].loc[:, 'y']) > y2_max:
    #     y2_max = max(sheets[key].loc[:, 'y'])
    sheets[key].loc[:, 'y'] = sheets[key].loc[:, 'y'] / max(sheets[key].loc[:, 'y'])
y2_max = 1


lfiles = [
    '/Users/atetenoire/server/Au/calix_acid/anyline_forms/mono_anyline_var1/job_132607_calculation/polarizability/job_132613_polarizability_calculation/modes_dftb_polarizability_calculation_132613.out',
    '/Users/atetenoire/server/Au/calix_acid/anyline_forms/mono_anyline_var2/job_132608_calculation/polarizability/job_132615_polarizability_calculation/modes_dftb_polarizability_calculation_132615.out',
    '/Users/atetenoire/server/Au/calix_acid/anyline_forms/tetra_anyline/job_132609_calculation/polarizability/job_132612_polarizability_calculation/modes_dftb_polarizability_calculation_132612.out',
    '/Users/atetenoire/server/Au/methyl/dftb-D3/grafted/job_128051_calculation/polarizability_test/born_derive/frozen_but_one/removed_2_layers/job_132876_frequency_calculation/modes_dftb_frequency_calculation_132876.out',
    '/Users/atetenoire/server/Au/phenyl/grafted/job_133615_calculation/born_deriv/job_133636_polarizability_calculation/modes_dftb_polarizability_calculation_133636.out',
    '/Users/atetenoire/server/Au/gold_surface_calix_acid/Au_111_calix_acid/dftb/calix_adsorbed/different_anchors/anchr0/job_127175_calculation/born_deriv/remove_2_layers/job_133153_polarizability_calculation/modes_dftb_polarizability_calculation_133153.out',
    '/Users/atetenoire/server/Au/gold_surface_calix_acid/Au_111_calix_acid/dftb/calix_adsorbed/different_anchors/anchr1_var1/job_127119_calculation/born_deriv/remove_2_layers/job_132742_polarizability_calculation/modes_dftb_polarizability_calculation_132742.out',
    '/Users/atetenoire/server/Au/gold_surface_calix_acid/Au_111_calix_acid/dftb/calix_adsorbed/different_anchors/anchr1_var2/job_127120_calculation/born_deriv/remove_2_layers/job_133152_polarizability_calculation/modes_dftb_polarizability_calculation_133152.out',
    '/Users/atetenoire/server/Au/gold_surface_calix_acid/Au_111_calix_acid/dftb/calix_adsorbed/different_anchors/anchr2_var1/job_127121_calculation/born_deriv/remove_2_layers/job_133155_polarizability_calculation/modes_dftb_polarizability_calculation_133155.out',
    '/Users/atetenoire/server/Au/gold_surface_calix_acid/Au_111_calix_acid/dftb/calix_adsorbed/different_anchors/anchr2_var2/job_127122_calculation/born_deriv/remove_2_layers/job_133156_polarizability_calculation/modes_dftb_polarizability_calculation_133156.out',
    '/Users/atetenoire/server/Au/gold_surface_calix_acid/Au_111_calix_acid/dftb/calix_adsorbed/different_anchors/anchr2_var3/job_127123_calculation/born_deriv/remove_2_layers/job_133154_polarizability_calculation/modes_dftb_polarizability_calculation_133154.out',
    '/Users/atetenoire/server/Au/gold_surface_calix_acid/Au_111_calix_acid/dftb/calix_adsorbed/different_anchors/anchr3_var1/job_127124_calculation/born_deriv/remove_2_layers/job_133157_polarizability_calculation/modes_dftb_polarizability_calculation_133157.out',
    '/Users/atetenoire/server/Au/gold_surface_calix_acid/Au_111_calix_acid/dftb/calix_adsorbed/different_anchors/anchr3_var2/job_127125_calculation/born_deriv/remove_2_layers/job_133151_polarizability_calculation/modes_dftb_polarizability_calculation_133151.out',
    '/Users/atetenoire/server/Au/gold_surface_calix_acid/Au_111_calix_acid/dftb/calix_adsorbed/different_anchors/anchr4/job_127126_calculation/born_deriv/remove_2_layers/job_133451_polarizability_calculation/modes_dftb_polarizability_calculation_133451.out',
]
llabel = [
    'Mono_anyline_var1',
    'Mono_anyline_var2',
    'Tetra_anyline',
    'Methyl',
    'Phenyl',
    'anchr0',
    'anchr1_var1',
    'anchr1_var2',
    'anchr2_var1',
    'anchr2_var2',
    'anchr2_var3',
    'anchr3_var1',
    'anchr3_var2',
    'anchr4',
]


x_range = range(4000)
modes = []
values = []
for file in lfiles:
    a = vfric.tools1.dftb_load_modes_out(file)
    b = vfric.tools1.sum_gaussian(x_range, a, gaussian_width)
    modes.append(a)
    values.append(b)


# vibrations = [
#     260.87,
#     829.83,
#     830.51,
#     1597.35,
#     1384.42,
#     1413.85,
#     558.36,
#     1765.47,
#     192.67,
#     511.91,
#     613.79,
#     673.07,
#     731.24,
#     1789.31,
#     135.74,
#     815.12,
# ]

dall = {}
y_max = 0
for num, label in enumerate(llabel):
    dall[label] = {}
    dall[label]['x'] = np.asarray(x_range)
    dall[label]['y'] = values[num]
    dall[label]['modes'] = modes[num]
    if y_max < max(values[num]):
        y_max = max(values[num])
    # dall[label]['vibrations'] = vibrations[num]


dmean = {}
lmean = ['anchr1', 'anchr2', 'anchr3']
for label in lmean:
    dmean[label] = {}
    dmean[label]['x'] = np.asarray(x_range)
dmean['anchr1']['y'] = (dall['anchr1_var1']['y'] + dall['anchr1_var2']['y']) / 2
dmean['anchr2']['y'] = (dall['anchr2_var1']['y'] + dall['anchr2_var2']['y'] + dall['anchr2_var3']['y']) / 3
dmean['anchr3']['y'] = (dall['anchr3_var1']['y'] + dall['anchr3_var2']['y']) / 2






dcolors = {
    'red': "#FF0000",
    'blue': "#0000FF",
    'green': "#00C11A",
    'turquoise': "#00FFFF",
    'black': "#000000",
    'grey': "#666666",
    'yellow': "#FFAA00",
    'pink': "#FF00EE",
    'dred': "#880000",
    'dgreen': "#008800",
    'dblue': "#000088",
    'violet': "#880088",
    'dyellow': "#888800",
    'dturquoise': "#008888",
    'orange': "#FF8800",
    'blue2': "#8800FF",
    'green2': "#88FF00",
    'pink2': "#FF0088",
    'lgreen': "#00FF88",
    'lblue': "#0088FF",
}
lcolors = [i for i in dcolors.values()] * 2



'''
===================================================================
FIRST PLOT
===================================================================
'''


# create a new plot with a title and axis labels
p = figure(title="Raman intensities", x_axis_label="wavenumber (cm-1)", y_axis_label="intensities (a.u.)", sizing_mode="stretch_width",
x_range=(0, 4000),
y_range=(0, y_max),
# max_width=500, 
# height=250
tools=[HoverTool(), BoxZoomTool(), ResetTool()],
tooltips="x: @x y: @y mode: @modes",
)

for num, label in enumerate(llabel):
    # print(label)
    line = p.line(dall[label]['x'], dall[label]['y'], legend_label=label, line_width=2, color=lcolors[num])
    line.visible = False

for num, label in enumerate(lmean):
    # print(label)
    line = p.line(dmean[label]['x'], dmean[label]['y'], legend_label=label, line_width=2, color=lcolors[num])
    line.visible = False






def update(attr, old, new):
    dsource = {
        'modes':np.asarray(list(dall[select.value]['modes'].keys())),
        'x0':np.asarray(list(dall[select.value]['modes'].values()))[:, 0],
        'x1':np.asarray(list(dall[select.value]['modes'].values()))[:, 0],
        'y0':np.zeros((len(np.asarray(list(dall[select.value]['modes'].values()))[:, 2]))),
        'y1':np.asarray(list(dall[select.value]['modes'].values()))[:, 2],
    }
    source.data = dsource



select = Select(title="import modes:", value=llabel[0], options=llabel)
select.on_change('value', update)


dsource = {
    'modes':np.asarray(list(dall[select.value]['modes'].keys())),
    'x0':np.asarray(list(dall[select.value]['modes'].values()))[:, 0],
    'x1':np.asarray(list(dall[select.value]['modes'].values()))[:, 0],
    'y0':np.zeros((len(np.asarray(list(dall[select.value]['modes'].values()))[:, 2]))),
    'y1':np.asarray(list(dall[select.value]['modes'].values()))[:, 2],
}
source = ColumnDataSource(data=dsource)


line_vib = p.segment(x0='x0', y0='y0', x1='x1', y1='y1', line_color='#000000', legend_label='Vib_modes', source=source)
line_vib.visible = False











p.legend.click_policy="hide"

# display legend in top left corner (default is top right corner)
# p.legend.location = "top_left"
p.add_layout(p.legend[0], 'left')





# set up RangeSlider
range_slider_x = RangeSlider(
    title="Adjust x-axis range",
    start=min(x_range),
    end=(max(x_range)),
    step=1,
    value=(p.x_range.start, p.x_range.end),
    max_width=800, 
)
range_slider_x.js_link("value", p.x_range, "start", attr_selector=0)
range_slider_x.js_link("value", p.x_range, "end", attr_selector=1)


# set up RangeSlider
range_slider_y = RangeSlider(
    title="Adjust y-axis range",
    start=-y_max*0.1,
    end=y_max,
    step=1,
    value=(p.y_range.start, p.y_range.end),
    max_width=500, 
)
range_slider_y.js_link("value", p.y_range, "start", attr_selector=0)
range_slider_y.js_link("value", p.y_range, "end", attr_selector=1)



'''
===================================================================
SECOND PLOT
===================================================================
'''


# create a new plot with a title and axis labels
p2 = figure(title="Comparison with experimental data", x_axis_label="wavenumber (cm-1)", y_axis_label="Simulated spectra intensities (a.u.)", sizing_mode="stretch_width",
x_range=(0, 4000),
y_range=(0, y_max),
# max_width=500, 
height=750,
tools=[HoverTool(), BoxZoomTool(), ResetTool()],
tooltips="x: @x y: @y mode: @modes",
)





for num, label in enumerate(llabel):
    # print(label)
    line = p2.line(dall[label]['x'], dall[label]['y'], legend_label=label, line_width=2, color=lcolors[num])
    line.visible = False
for num, label in enumerate(lmean):
    # print(label)
    line = p2.line(dmean[label]['x'], dmean[label]['y'], legend_label=label, line_width=2, color=lcolors[num])
    line.visible = False




def update_2(attr, old, new):
    dsource_2 = {
        'modes':np.asarray(list(dall[select_2.value]['modes'].keys())),
        'x0':np.asarray(list(dall[select_2.value]['modes'].values()))[:, 0],
        'x1':np.asarray(list(dall[select_2.value]['modes'].values()))[:, 0],
        'y0':np.zeros((len(np.asarray(list(dall[select_2.value]['modes'].values()))[:, 2]))),
        'y1':np.asarray(list(dall[select_2.value]['modes'].values()))[:, 2],
    }
    source_2.data = dsource_2



select_2 = Select(title="import modes:", value=llabel[0], options=llabel)
select_2.on_change('value', update_2)


dsource_2 = {
    'modes':np.asarray(list(dall[select_2.value]['modes'].keys())),
    'x0':np.asarray(list(dall[select_2.value]['modes'].values()))[:, 0],
    'x1':np.asarray(list(dall[select_2.value]['modes'].values()))[:, 0],
    'y0':np.zeros((len(np.asarray(list(dall[select_2.value]['modes'].values()))[:, 2]))),
    'y1':np.asarray(list(dall[select_2.value]['modes'].values()))[:, 2],
}
source_2 = ColumnDataSource(data=dsource_2)


line_vib = p2.segment(x0='x0', y0='y0', x1='x1', y1='y1', line_color='#000000', legend_label='Vib_modes', source=source_2)
line_vib.visible = False








p2.extra_y_ranges['foo'] = Range1d(0,1)
for num, key in enumerate(keys):
    # print(label)
    line = p2.line(sheets[key]['x'], sheets[key]['y'], legend_label=key, line_width=2, color=lcolors[num], y_range_name="foo")
    line.visible = False

ax2 = LinearAxis(y_range_name="foo", axis_label="Experimental data resized to 1")
p2.add_layout(ax2, 'right')









# display legend in top left corner (default is top right corner)
# p2.legend.location = "top_left"

p2.legend.click_policy="hide"
p2.add_layout(p2.legend[0], 'left')

# set up RangeSlider
range_slider_x2 = RangeSlider(
    title="Adjust x-axis range",
    start=min(x_range),
    end=(max(x_range)),
    step=1,
    value=(p2.x_range.start, p2.x_range.end),
    max_width=800, 
)
range_slider_x2.js_link("value", p2.x_range, "start", attr_selector=0)
range_slider_x2.js_link("value", p2.x_range, "end", attr_selector=1)


# set up RangeSlider
range_slider_y2 = RangeSlider(
    title="Adjust y-axis range of simulation data",
    start=-y_max*0.1,
    end=y_max,
    step=1,
    value=(p2.y_range.start, p2.y_range.end),
    max_width=500, 
)
range_slider_y2.js_link("value", p2.y_range, "start", attr_selector=0)
range_slider_y2.js_link("value", p2.y_range, "end", attr_selector=1)


# set up RangeSlider
range_slider_y22 = RangeSlider(
    title="Adjust y-axis range of experimental data",
    start=-y2_max*0.1,
    end=y2_max,
    step=0.01,
    value=(0, 1),
    max_width=500, 
)
range_slider_y22.js_link("value", p2.extra_y_ranges['foo'], "start", attr_selector=0)
range_slider_y22.js_link("value", p2.extra_y_ranges['foo'], "end", attr_selector=1)







p.legend.label_text_font_size = "9px"
p2.legend.label_text_font_size = "9px"



# create layout
layout = layout(
    [
        [range_slider_x],
        [range_slider_y],
        [select],
        [p],
        [range_slider_x2],
        [range_slider_y2],
        [range_slider_y22],
        [select_2],
        [p2],
    ],
    sizing_mode="stretch_width"
)

# show result
# show(layout)
curdoc().add_root(layout)
# show(row)

# show the results
# show(p)
# save(p)


#https://docs.bokeh.org/en/latest/docs/user_guide/interaction/callbacks.html

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import Figure, output_file, show

from bokeh.palettes import Category20 as palette


colors = palette[10]
# while len(colors)>3:
    # colors.pop()
# data['color'] = colors
# print(colors)
colors=[colors[0],colors[8]]
output_file("js_on_change.html")

# x = [x*0.005 for x in range(0, 200)]
# y = x

# source = ColumnDataSource(data=dict(x=x, y=y))

source = ColumnDataSource(data=dict(
    t=[ [1, 2, 3], [4, 5, 6] ],
    xs=[ [2, 2, 4], [7, 8, 9] ],
    color=colors,
))

plot = Figure(plot_width=400, plot_height=400)
# plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

plot.multi_line(xs='t', ys='xs', source=source,line_color='color')



callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var f = cb_obj.value
    var x = data['xs']
    var y = data['ys'][1]
    for (var i = 0; i < y.length; i++) {
        y[i] = Math.pow(2, f)
    }
    source.change.emit();
""")

slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")
slider.js_on_change('value', callback)

layout = column(slider, plot)

show(layout)
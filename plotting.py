import json
import plotly
import plotly.express as px
import math


def create_bar_plot(x_data, y_data, color_data, x_text, y_text, color_text):
    fig = px.bar(x=x_data, y=y_data, color=color_data,
                 labels={
                     "x": x_text,
                     "y": y_text,
                     "color": color_text})
    fig.update(layout_coloraxis_showscale=False)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_scatter_plot(x_data, y_data, color_data, x_text, y_text, color_text):

    fig = px.scatter(x=x_data,
                     y=y_data,
                     color=color_data,
                     labels={
                         "x": x_text,
                         "y": y_text,
                         "color": color_text
                     }
                     )
    fig.update_traces(mode="markers")

    # Set axis limits
    max_x = max(x_data)
    max_y = max(y_data)

    overall_max = math.ceil(max([max_x, max_y]))
    fig.update_layout(xaxis=dict(range=[0, overall_max]))
    fig.update_layout(yaxis=dict(range=[0, overall_max]))
    fig.add_shape(type="line",
                  x0=0,
                  y0=0,
                  x1=overall_max,
                  y1=overall_max,
                  layer='below',
                  opacity=0.5)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

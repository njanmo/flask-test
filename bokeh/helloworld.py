# import core modules
import os
import pandas as pd

# import flask modules
from flask import Flask, render_template, request

#import bokeh modules
from bokeh.io import curdoc, output_notebook
from bokeh.plotting import figure, show
from bokeh.layouts import row, widgetbox, gridplot
from bokeh.models import Slider, ColumnDataSource, Select, HoverTool, CDSView
from bokeh.palettes import Spectral5
from bokeh.embed import components

app = Flask(__name__)

# add the current directory to the script
os.path.abspath(os.curdir)

# read in .csv file of 2016 cencer incidents UK
d = pd.read_csv("data/data.csv", delimiter=',')

# instantiate dataframe to pass data to graphical models
df = pd.DataFrame(data=d)

# pivot dataframe to switch columns to rows
df2 = pd.pivot_table(df, columns=['Males', 'Females'])

# sort index manually by age
df2 = pd.DataFrame(df2, index = ['< 1', '1 -4', '5 - 9', '10 - 14', '15 - 19', '20 - 24', '25 - 29', '30 - 34', '35 - 39', '40 - 44', '45 - 49', '50 - 54', '55 - 59', '60 - 64', '65 - 69', '70 - 74', '75 - 79', '80 - 84', '85 - 89', '90 +'] )

# create column out of the index
df2['Age'] = df2.index

#create data source
source = ColumnDataSource(df2)

# create labels for x axis / 'Age' axis
label = ['< 1', '1 -4', '5 - 9', '10 - 14', '15 - 19', '20 - 24', '25 - 29', '30 - 34', '35 - 39', '40 - 44', '45 - 49', '50 - 54', '55 - 59', '60 - 64', '65 - 69', '70 - 74', '75 - 79', '80 - 84', '85 - 89', '90 +']

# instantiate shared generic plot settings
# hover tool
hoverm = HoverTool(
    tooltips=[
    ("Age", "(@Age)"),
        ("Incidents", "(@Males{0,0.000})"),
    ],
    mode='vline'
)

hoverf = HoverTool(
    tooltips=[
    ("Age", "(@Age)"),
        ("Incidents", "(@Females{0,0.000})"),
    ],
    mode='hline'
)

hoverm.point_policy='snap_to_data'
hoverm.line_policy='nearest'

# graph tool bar
toolsm = ["box_select", hoverm, "reset"]
toolsf = ["box_select", hoverf, "reset"]


#create the main plot
def create_figure(*args):
	#create new plot with sizing & labels
	mplot = figure(x_range=label, plot_width=900, plot_height=400, tools=toolsm, title = "Cancer Incidents in Males 2016")
	#remove bokeh logo, add axis labels
	mplot.toolbar.logo = None
	mplot.xaxis.axis_label = 'Age Range'
	mplot.yaxis.axis_label = 'Cancer Incidents'
	#plot circles Age vs Males of cancer incidence
	mplot.circle(x="Age", y="Males", alpha=0.5, source=source)

	return mplot

# Index page, no args
@app.route('/')
@app.route('/index')
def index():
	# Create the plot
	plot = create_figure()

	# Embed plot into HTML via Flask Render
	script, div = components(plot)
	return render_template("index.html", script=script, div=div)

# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)

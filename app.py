import pandas as pd
import requests
from flask import Flask, render_template
from datetime import datetime
from math import pi
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, output_file, save
from bokeh.embed import components
import os
import time

app = Flask(__name__)


# Read in the data from a SODA API
url = "https://data.oaklandnet.com/resource/ym6k-rx7a.json"
query = {"$select" : "date_trunc_ymd(datetime) AS date,count(*)",
        "$group" : "date",
        "$where" : "date < \'%s\'" % time.strftime("%Y-%m-%d"),
        "crimetype" : "ROBBERY"}
r = requests.get(url, params=query)

# Create a pandas dataframe, then a bokeh ColumnDataSource for use with 
# the HoverTool. Convert columns to appropriate data types and sort by date
df = pd.DataFrame(r.json())
df['count'] = df['count'].astype(int)
df['date'] = map(lambda x: datetime.strptime(str(x), 
    '%Y-%m-%dT%H:%M:%S'), df['date'])
df = df.sort('date')

source = ColumnDataSource(
        data=dict(
            date=df['date'],
            date_str=map(lambda x: datetime.strftime(x,'%m/%d'),
                df['date']),
            count=df['count']))

hover = HoverTool(tooltips=[
            ("date", "@date_str"),
            ("total", "@count")])

# Make it look nice. 'x_axis_type=datetime' allows for x-axis arrays
# of datetime.datetime objects
fig = figure(width=1000, x_axis_type='datetime', tools=[hover],
        title='Robberies in Oakland',
        title_text_align='center',
        title_text_font='monospace',
        title_text_color='Tomato',
        title_text_font_size='28pt',
        title_text_font_style='bold',
        y_axis_label='no. committed')
fig.yaxis.axis_label_text_font_style='bold'
fig.yaxis.axis_label_text_font='monospace'
fig.xaxis.major_label_orientation = pi/4
fig.background_fill = 'WhiteSmoke'
fig.grid.grid_line_color = 'White'
fig.grid.grid_line_width = 2
fig.grid.grid_line_dash = [6,4]

# Create the plot
fig.line('date', 'count', line_width=4, line_join='round',
        line_cap='round', line_color='DeepSkyBlue', source=source)
fig.circle('date', 'count', size=10, fill_color='White',
        line_color='Tomato', source=source)
script, div = components(fig)

@app.route('/')
def index():    
    return render_template('index.html', script=script, div=div)

if __name__ == '__main__':
    app.run()

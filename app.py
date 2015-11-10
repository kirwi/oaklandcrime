from flask import Flask, render_template
import os
from bokeh.charts import Bar, output_file, show
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    soql_params = {"$select" : "policebeat AS district,count(*)",
                   "$group" : "policebeat"}
    r = requests.get("https://data.oaklandnet.com/resource/ym6k-rx7a.json",
                     params=soql_params)
    labels = []
    vals = []
    for d in r.json():
        labels.append(d.get('district', False))
        vals.append(d.get('count', 0))
    
    p = Bar(r.json(), 'district', values='count', title='Oakland Crime Totals by Police District')
    output_file('templates/index.html')
    show(p)
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT','8080')))
import csv
import os
from datetime import datetime

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure

DATA_FILE = os.path.join(os.path.dirname(__file__), "monthly_averages.csv")


def load_averages(path):
    averages = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            month = datetime.strptime(row["month"], "%Y-%m")
            averages.setdefault(row["zipcode"], []).append((month, float(row["avg_hours"])))
    for zipcode in averages:
        averages[zipcode].sort()
    return averages


def curve(zipcode):
    points = averages.get(zipcode, [])
    return {"month": [p[0] for p in points], "hours": [p[1] for p in points]}


averages = load_averages(DATA_FILE)
zipcodes = sorted(z for z in averages if z != "ALL")

zip1 = Select(title="Zipcode 1", value="10001" if "10001" in zipcodes else zipcodes[0], options=zipcodes)
zip2 = Select(title="Zipcode 2", value="11201" if "11201" in zipcodes else zipcodes[1], options=zipcodes)

all_source = ColumnDataSource(curve("ALL"))
zip1_source = ColumnDataSource(curve(zip1.value))
zip2_source = ColumnDataSource(curve(zip2.value))

plot = figure(
    title="Monthly average 311 response time (incidents created in 2024)",
    x_axis_type="datetime",
    x_axis_label="Month incident was closed",
    y_axis_label="Average create-to-closed time (hours)",
    width=800,
    height=450,
)
plot.line("month", "hours", source=all_source, line_width=2, color="black", legend_label="All zipcodes")
plot.line("month", "hours", source=zip1_source, line_width=2, color="#1f77b4", legend_label="Zipcode 1")
plot.line("month", "hours", source=zip2_source, line_width=2, color="#d62728", legend_label="Zipcode 2")
plot.legend.location = "top_left"


def update(attr, old, new):
    zip1_source.data = curve(zip1.value)
    zip2_source.data = curve(zip2.value)
    plot.legend.items[1].label = {"value": "Zipcode " + zip1.value}
    plot.legend.items[2].label = {"value": "Zipcode " + zip2.value}


zip1.on_change("value", update)
zip2.on_change("value", update)
update(None, None, None)

curdoc().add_root(column(zip1, zip2, plot))
curdoc().title = "NYC 311 response time by zipcode"

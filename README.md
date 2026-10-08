# COMP 370 Homework 5: NYC 311 Data Analysis

Tools for exploring NYC 311 service requests from 2024: a CLI tool that counts complaint types per borough, a Jupyter analysis, and a Bokeh dashboard that compares response times between zipcodes.

## Data

The data is not in this repository. Download `311_records.csv.tgz` from the HW 05 assignment on MyCourses (a derivative of [NYC 311 Data](https://data.cityofnewyork.us/Social-Services/NYC-311-Data/jrb2-thup/about_data)), then unpack it into `data/` and trim it to incidents created in 2024 with one `grep` call:

```bash
mkdir -p data
tar -xzf 311_records.csv.tgz -C data
grep -E '^(Unique Key,|[0-9]+,[0-9]{2}/[0-9]{2}/2024 )' data/311_Service_Requests_from_2010_to_Present_20250928.csv > data/311_2024.csv
```

## Installation

```bash
pip install -r requirements.txt
```

## Task 1: `borough_complaints.py`

Counts each complaint type per borough for incidents created between two dates (inclusive).

```bash
python borough_complaints.py -i data/311_2024.csv -s 2024-01-01 -e 2024-02-29
python borough_complaints.py -i data/311_2024.csv -s 2024-01-01 -e 2024-02-29 -o data/jan_feb.csv
python borough_complaints.py -h
```

Output is CSV with the columns `complaint type,borough,count`.

## Task 3: `task3.ipynb`

Runs `borough_complaints.py` for January–February and June–July 2024 and plots the most abundant complaint type per borough. Results are written up in `complaint_type_analysis.md`.

## Task 4: Bokeh dashboard

Precompute the monthly averages once (about a minute), then start the dashboard:

```bash
cd dashboard
python preprocess.py -i ../data/311_2024.csv -o monthly_averages.csv
bokeh serve --show dashboard.py
```

The dashboard has two zipcode dropdowns and a line plot of the monthly average create-to-closed time in hours, with three curves: all zipcodes, zipcode 1 and zipcode 2.

Preprocessing rules:
- only incidents created in 2024
- no missing zipcode (and not `00000`)
- no missing closed date
- no negative response time
- an incident counts in the month it was closed
- only incidents closed in 2024, so the x-axis covers January–December 2024

## Conceptual questions

Answers are in `conceptual_answers.md`.

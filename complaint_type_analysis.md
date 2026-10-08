# Task 3: Complaint Type Analysis

## How the analysis was done

The dataset was first trimmed to incidents created in 2024 with a single `grep` call. It matches the header line, plus every line whose `Created Date` (the second field) is in 2024:

```bash
grep -E '^(Unique Key,|[0-9]+,[0-9]{2}/[0-9]{2}/2024 )' 311_Service_Requests_from_2010_to_Present_20250928.csv > 311_2024.csv
```

The trimmed file has 3,458,320 incidents. A full CSV parse of the original file finds the same number of 2024 incidents.

In Jupyter (`task3.ipynb`), I ran `borough_complaints.py` for each period:

```bash
python borough_complaints.py -i 311_2024.csv -s 2024-01-01 -e 2024-02-29 -o jan_feb.csv
python borough_complaints.py -i 311_2024.csv -s 2024-06-01 -e 2024-07-31 -o jun_jul.csv
```

I then added up each complaint type's counts across all boroughs to find the most abundant type in January–February 2024.

## Most abundant complaint type in January–February 2024

There were 527,654 complaints in January–February 2024. The top five complaint types were:

| Rank | Complaint type | Count |
|---|---|---|
| 1 | HEAT/HOT WATER | 81,641 |
| 2 | Illegal Parking | 79,916 |
| 3 | Noise - Residential | 43,602 |
| 4 | Blocked Driveway | 28,608 |
| 5 | UNSANITARY CONDITION | 19,208 |

The most abundant type is **HEAT/HOT WATER**, with 15.5% of all complaints. The bar chart in the notebook shows its count in each borough:

| Borough | Jan–Feb 2024 |
|---|---|
| BRONX | 30,139 |
| BROOKLYN | 20,915 |
| MANHATTAN | 17,604 |
| QUEENS | 12,117 |
| STATEN ISLAND | 866 |
| **Total** | **81,641** |

## Comparison with June–July 2024

| Borough | Jan–Feb 2024 | Jun–Jul 2024 | Change |
|---|---|---|---|
| BRONX | 30,139 | 2,227 | −92.6% |
| BROOKLYN | 20,915 | 1,929 | −90.8% |
| MANHATTAN | 17,604 | 1,778 | −89.9% |
| QUEENS | 12,117 | 835 | −93.1% |
| STATEN ISLAND | 866 | 121 | −86.0% |
| **Total** | **81,641** | **6,890** | **−91.6%** |

## What the analysis revealed

- **HEAT/HOT WATER complaints are strongly seasonal.** They are the most common complaint in January–February, but there are only 6,890 in June–July, about 12 times fewer. In June–July they make up just 1.1% of all complaints and rank only 25th among complaint types. Total 311 volume is higher in June–July (605,676 complaints), so the drop is not because fewer complaints were filed overall. The likely reason is that NYC's heating season requires landlords to provide heat from October to May. In winter, most of these complaints are about missing heat. In summer, only hot-water problems remain.
- **The Bronx files the most HEAT/HOT WATER complaints in both periods.** It has 36.9% of them in January–February and 32.3% in June–July, even though it is not the most populous borough. Brooklyn and Manhattan come next, and Staten Island has very few. The borough ranking is the same in both periods.
- **Other complaint types lead in summer.** In June–July the top types are Illegal Parking (86,240), Noise - Residential (58,197) and Noise - Street/Sidewalk (47,320). City resources needed for 311 complaints shift from housing and heating in winter to parking and noise in summer.

import argparse
import csv
from datetime import datetime

DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute monthly average 311 response times (hours) for every zipcode and for all of NYC."
    )
    parser.add_argument("-i", "--input", required=True, help="the 2024 311 csv file")
    parser.add_argument("-o", "--output", default="monthly_averages.csv", help="output csv file")
    return parser.parse_args()


def clean_zip(text):
    text = text.strip()
    if len(text) >= 5 and text[:5].isdigit() and text[:5] != "00000" and (len(text) == 5 or text[5] == "-"):
        return text[:5]
    return None


def compute_averages(input_file):
    totals = {}
    with open(input_file, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header = next(reader)
        created_col = header.index("Created Date")
        closed_col = header.index("Closed Date")
        zip_col = header.index("Incident Zip")
        for row in reader:
            zipcode = clean_zip(row[zip_col])
            if zipcode is None or row[closed_col] == "":
                continue
            created = datetime.strptime(row[created_col], DATE_FORMAT)
            closed = datetime.strptime(row[closed_col], DATE_FORMAT)
            if created.year != 2024 or closed.year != 2024:
                continue
            hours = (closed - created).total_seconds() / 3600
            if hours < 0:
                continue
            month = closed.strftime("%Y-%m")
            for key in [(zipcode, month), ("ALL", month)]:
                if key not in totals:
                    totals[key] = [0.0, 0]
                totals[key][0] += hours
                totals[key][1] += 1
    return totals


def main():
    args = parse_args()
    totals = compute_averages(args.input)
    with open(args.output, "w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["zipcode", "month", "avg_hours", "count"])
        for (zipcode, month), (hour_sum, count) in sorted(totals.items()):
            writer.writerow([zipcode, month, round(hour_sum / count, 3), count])


if __name__ == "__main__":
    main()

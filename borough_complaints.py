import argparse
import csv
import sys
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(
        description="Count the number of each complaint type per borough for 311 incidents created in a date range."
    )
    parser.add_argument("-i", "--input", required=True, help="the input 311 csv file")
    parser.add_argument("-s", "--start", required=True, help="start creation date, inclusive (YYYY-MM-DD)")
    parser.add_argument("-e", "--end", required=True, help="end creation date, inclusive (YYYY-MM-DD)")
    parser.add_argument("-o", "--output", help="output csv file (default: print to stdout)")
    return parser.parse_args()


def to_date(text):
    return datetime.strptime(text, "%Y-%m-%d").date()


def count_complaints(input_file, start, end):
    counts = {}
    with open(input_file, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header = next(reader)
        created_col = header.index("Created Date")
        type_col = header.index("Complaint Type")
        borough_col = header.index("Borough")
        for row in reader:
            created = row[created_col]
            day = created[6:10] + "-" + created[0:2] + "-" + created[3:5]
            if start <= day <= end:
                key = (row[type_col], row[borough_col])
                counts[key] = counts.get(key, 0) + 1
    return counts


def write_counts(counts, out):
    writer = csv.writer(out)
    writer.writerow(["complaint type", "borough", "count"])
    for (complaint_type, borough), count in sorted(counts.items()):
        writer.writerow([complaint_type, borough, count])


def main():
    args = parse_args()
    start = to_date(args.start)
    end = to_date(args.end)
    if start > end:
        sys.exit("error: start date must be on or before end date")
    counts = count_complaints(args.input, start.isoformat(), end.isoformat())
    if args.output:
        with open(args.output, "w", newline="") as out:
            write_counts(counts, out)
    else:
        write_counts(counts, sys.stdout)


if __name__ == "__main__":
    main()

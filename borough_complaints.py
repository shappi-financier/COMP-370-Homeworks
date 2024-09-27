import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description='Count complaints by type and borough for a given date range.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-s', '--start_date', required=True, help='Start date in MM/DD/YYYY format')
    parser.add_argument('-e', '--end_date', required=True, help='End date in MM/DD/YYYY format')
    parser.add_argument('-o', '--output', help='Output file (optional)')
    return parser.parse_args()

def valid_date(date_str):
    try:
        return datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        raise ValueError(f"Invalid date: {date_str}. Date format should be MM/DD/YYYY")

def filter_complaints_by_date_and_borough(input_file, start_date, end_date):
    start = valid_date(start_date)
    end = valid_date(end_date)
    
    complaints_count = defaultdict(lambda: defaultdict(int))  # complaint_type -> borough -> count
    
    with open(input_file, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            creation_date = row[1]  # The 2nd column is 'Creation Date'
            complaint_type = row[5]  # The 6th column is 'Complaint Type'
            borough = row[23]  # The 24th column is 'Borough'
            
            # Parse the date part of 'Creation Date' (removing the time part)
            complaint_date = valid_date(creation_date.split()[0])  
            
            # Check if the complaint falls within the given date range
            if start <= complaint_date <= end:
                complaints_count[complaint_type][borough] += 1
    
    return complaints_count

def write_output(complaints_count, output=None):
    output_lines = ["complaint type,borough,count"]
    for complaint_type in sorted(complaints_count):
        for borough in sorted(complaints_count[complaint_type]):
            count = complaints_count[complaint_type][borough]
            output_lines.append(f"{complaint_type},{borough},{count}")
    
    if output:
        with open(output, mode='w', newline='', encoding='utf-8') as f:
            f.write("\n".join(output_lines))
    else:
        print("\n".join(output_lines))

def main():
    args = parse_args()
    
    complaints_count = filter_complaints_by_date_and_borough(args.input, args.start_date, args.end_date)
    
    write_output(complaints_count, args.output)

if __name__ == '__main__':
    main()

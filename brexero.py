import argparse
import csv
from datetime import datetime

FIELD_MAP = {'Posted Date (UTC)': 'Date',
             'Amount': 'Amount',
             'Merchant Name': 'Payee',
             'Statement Descriptor': 'Description'}

def main():
    parser = argparse.ArgumentParser(description='Convert Brex export into Xero import format.')
    parser.add_argument('--brex-file', required=True,
                        help='Brex file (input)')
    parser.add_argument('--xero-file', required=True,
                        help='Xero file (output)')

    args = parser.parse_args()

    data = import_brex_file(args.brex_file)
    output_xero_file(args.xero_file, data)


# returns an array of dicts with the data
def import_brex_file(filename):
    ret = []

    with open(filename, "r") as f:
       reader = csv.DictReader(f)
       for row in reader:
           # ignore Brex payments, etc.
           if row['Type'] == 'Payment to Brex':
               row['Merchant Name'] = 'Brex'
               row['Statement Descriptor'] = 'Payment'
           ret.append(row)

    return ret


def write_line(writer, line):
    data = {}
    for key, value in line.items():
        if key in FIELD_MAP:
            if 'Date' in key:
                # write dates in MM-DD-YYYY format
                data[FIELD_MAP[key]] = datetime.strftime(datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%fZ'), '%m-%d-%Y')
            elif key == 'Amount':
                # brex output shows 1300 as 1.3e3, plus negate to indicate 'spent'
                data[FIELD_MAP[key]] = -float(value)
            else:
                data[FIELD_MAP[key]] = value

    writer.writerow(data)


def output_xero_file(filename, data):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_MAP.values())
        writer.writeheader()
        for line in data:
            write_line(writer, line)

if __name__ == '__main__':
    main()

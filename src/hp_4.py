# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    return [datetime.strptime(date, "%Y-%m-%d").strftime("%d %b %Y") for date in old_dates]

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int): 
        raise TypeError
    else:
        return [datetime.strptime(start, "%Y-%m-%d") + timedelta(days=i) for i in range(n)]




def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    return [(datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i), value) for i, value in enumerate(values)]


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile) as f:
        data = [
            {
                'patron_id': item['patron_id'],
                'late_fees': round((datetime.strptime(item['date_returned'], '%m/%d/%Y') - datetime.strptime(item['date_due'], '%m/%d/%Y')).days * 0.25, 2) if (datetime.strptime(item['date_returned'], '%m/%d/%Y') - datetime.strptime(item['date_due'], '%m/%d/%Y')).days > 0 else 0
            }
            for item in DictReader(f)
        ]
    
    aggregated_data = defaultdict(float)
    
    for entry in data:
        aggregated_data[entry['patron_id']] += entry['late_fees']
    
    final_data = [{'patron_id': key, 'late_fees': round(value, 2) if value > 0 else 0} for key, value in aggregated_data.items()]
    
    with open(outfile, "w", newline="") as file:
        writer = DictWriter(file, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        writer.writerows(final_data)
    

# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())

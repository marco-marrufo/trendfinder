import xlrd
import csv
import sys

# Script that takes in an xlsx file path as input and converts the data to CSV
# Calling Format:
# python3 xlsx_to_csv <INPUT LSX FILE PATH> <OPTIONAL OUTPUT CSV FILE PATH>
def main():
    xlsx_path = sys.argv[1]
    # If we have more than two arguments, assume optional CSV File Path is given
    if len(sys.argv) > 2:
        csv_path = sys.argv[2]
    # Otherwise, build store our CSV file with the XLSX file using the same name.
    else:
        csv_path = xlsx_path.split('xlsx')[0]+'csv'

    wb = xlrd.open_workbook(xlsx_path)
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open(csv_path, 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    # Writing our XLSX data to a CSV
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

if __name__ == "__main__":
    main()

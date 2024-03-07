import csv
from bs4 import BeautifulSoup


import chardet


def parse_html_to_csv(html_file_path, csv_file_path):
    # Detect the encoding of the HTML file
    with open(html_file_path, 'rb') as html_file:
        rawdata = html_file.read()
        encoding_result = chardet.detect(rawdata)
        encoding = encoding_result['encoding']

    # Open the HTML file with detected encoding
    with open(html_file_path, 'r', encoding=encoding) as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        table = soup.find('table')

        # Open the CSV file with ANSI encoding
        with open(csv_file_path, 'w', newline='', encoding='ANSI') as csv_file:
            writer = csv.writer(csv_file)
            # Write header row
            header_row = [th.text for th in table.find_all('th')]
            writer.writerow(header_row)

            # Write data rows
            for row in table.find_all('tr'):
                data_row = [td.text for td in row.find_all('td')]
                writer.writerow(data_row)

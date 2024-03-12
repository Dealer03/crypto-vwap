import csv
from bs4 import BeautifulSoup


def parse_html_to_csv(html_file_path, csv_file_path):
    with open(html_file_path, 'r', encoding='ANSI') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        table = soup.find('table')

        with open(csv_file_path, 'w', newline='', encoding='ANSI') as csv_file:
            writer = csv.writer(csv_file)
            # Write header row
            header_row = [th.text for th in table.find_all('th')]
            writer.writerow(header_row)

            # Write data rows
            for row in table.find_all('tr'):
                data_row = [td.text for td in row.find_all('td')]
                writer.writerow(data_row)

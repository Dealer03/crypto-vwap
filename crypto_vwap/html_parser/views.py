from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
import csv
import os


def parse_html_to_csv(request):
    # Read HTML file
    with open('div class=ant-table-content style=p24html', 'r') as file:
        html_content = file.read()

    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract data
    data_rows = soup.find_all('tr', class_='ant-table-row-level-0')

    # Prepare CSV data
    csv_data = []
    for row in data_rows:
        # Extract data from each column of the table row
        columns = row.find_all('td')

        # Extracting data for each column
        time = columns[0].text.strip()
        side = columns[1].find('span').text.strip()
        sub_wallet = columns[2].text.strip()
        type = columns[3].text.strip()
        average = columns[4].text.strip()
        filled = columns[5].text.strip()
        fees = columns[6].text.strip()
        realized_profit = columns[7].text.strip()

        # Append data as a list to csv_data
        csv_data.append([time, side, sub_wallet, type,
                        average, filled, fees, realized_profit])

    # Define directory and CSV file path
    output_directory = 'BYDFI Trade History'
    csv_file = os.path.join(output_directory, 'output.csv')

    # Create directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Write data to CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Time', 'Side', 'Sub-wallet', 'Type', 'Average',
                            'Filled', 'Fees', 'Realized Profit'])  # Write header
        csv_writer.writerows(csv_data)  # Write data rows

    # Return a response indicating success
    return HttpResponse("HTML parsed and CSV file created successfully!")

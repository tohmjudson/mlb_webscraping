#! /usr/bin/env python3
# Using Python and Beautiful Soup to Scrape Baseball-Reference.com

import requests
import os
import bs4
import csv

# Example URL: http://www.baseball-reference.com/teams/NYM/2016-schedule-scores.shtml
url = 'http://www.baseball-reference.com/teams/'  # Starting url

# Variables
team = 'NYM'
yearStart = 1986
yearEnd = 2016

# Create Save Folder
saveFolder = team + ' Schedule and Results (' + str(yearStart) + '-' + str(yearEnd) + ')'
os.makedirs(saveFolder, exist_ok=True)

# Run once for each year
for year in range(yearStart, yearEnd + 1):

    # Create URL
    fullUrl = url + team + '/' + str(year) + '-schedule-scores.shtml'

    # Download the page
    print('Downloading page %s...' % fullUrl)
    response = requests.get(fullUrl)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # Extract Table
    table = soup.find('table', attrs={"id": "team_schedule"})

    # Extract Header
    headers = [header.text for header in table.find('thead').findAll('th')]
    headers[5] = 'at'  # replace symbol with at in header

    # Extract Rows
    rows = []
    for row in table.find_all('tr'):
        rows.append([val.text for val in row.find_all('td')])

    # Write to csv
    fileName = team + str(year) + '.csv'
    with open(os.path.join(saveFolder, fileName), 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(row for row in rows if row)

print('Done')

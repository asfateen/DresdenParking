import requests
from bs4 import BeautifulSoup
import csv
import os
import re
from datetime import datetime

BASE_URL = "https://www.dresden.de"
INDEX_URL = BASE_URL + "/apps_ext/ParkplatzApp/index"
DETAIL_BASE_URL = BASE_URL + "/apps_ext/ParkplatzApp"

response = requests.get(INDEX_URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

detail_links = soup.find_all("a", href=re.compile(r"^\./detail\?id=\d+"))

data_filename = 'parking_data.csv'
data_exists = os.path.isfile(data_filename)

with open(data_filename, mode='a', newline='', encoding='utf-8') as data_file:
    data_writer = csv.writer(data_file)

    if not data_exists:
        data_writer.writerow(['Timestamp', 'ID', 'Parking Name', 'Total Spaces', 'Free Spaces', 'Last Updated'])

    for link in detail_links:
        relative_href = link['href']
        full_url = DETAIL_BASE_URL + relative_href[1:]  
        match = re.search(r"id=(\d+)", relative_href)
        parking_id = match.group(1) if match else 'N/A'
        parking_name = link.get_text(strip=True)

        detail_response = requests.get(full_url)
        detail_response.raise_for_status()
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

        total_spaces_div = detail_soup.select_one("h3+ .data-row .size6+ .size6")
        total_spaces = total_spaces_div.get_text(strip=True) if total_spaces_div else 'N/A'

        free_spaces_div = detail_soup.select_one(".size6 .data-row:nth-child(1) .size6+ .size6")
        free_spaces = free_spaces_div.get_text(strip=True) if free_spaces_div else 'N/A'

        last_updated_div = detail_soup.select_one(".data-row:nth-child(4) .size6+ .size6")
        last_updated = last_updated_div.get_text(strip=True) if last_updated_div else 'N/A'

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_writer.writerow([timestamp, parking_id, parking_name, total_spaces, free_spaces, last_updated])

        print(f"✅ Scraped: {parking_id} - {parking_name} | Free: {free_spaces}/{total_spaces}")

print(f"🚀 All parking data saved to {data_filename}")
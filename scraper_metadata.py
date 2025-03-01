import requests
from bs4 import BeautifulSoup
import csv
import os
import re

BASE_URL = "https://www.dresden.de"
INDEX_URL = BASE_URL + "/apps_ext/ParkplatzApp/index"
DETAIL_BASE_URL = BASE_URL + "/apps_ext/ParkplatzApp"

response = requests.get(INDEX_URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

detail_links = soup.find_all("a", href=re.compile(r"^\./detail\?id=\d+"))

metadata_filename = 'metadata.csv'
metadata_exists = os.path.isfile(metadata_filename)

if not metadata_exists:
    with open(metadata_filename, mode='a', newline='', encoding='utf-8') as meta_file:
        meta_writer = csv.writer(meta_file)
        meta_writer.writerow(['ID', 'Parking Name', 'Address', 'GPS-Lon', 'GPS-Lat', 'Opening Hours', 'Fees'])

for link in detail_links:
    relative_href = link['href']
    full_url = DETAIL_BASE_URL + relative_href[1:]  
    match = re.search(r"id=(\d+)", relative_href)
    parking_id = match.group(1) if match else 'N/A'
    parking_name = link.get_text(strip=True)

    detail_response = requests.get(full_url)
    detail_response.raise_for_status()
    detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

    address_div = detail_soup.select_one("div:nth-child(9)")
    address = address_div.get_text(strip=True) if address_div else 'N/A'

    lon_div = detail_soup.select_one(".data-row:nth-child(12) .size6+ .size6")
    lon = lon_div.get_text(strip=True) if lon_div else 'N/A'

    lat_div = detail_soup.select_one("div~ .data-row+ .data-row .size6+ .size6")
    lat = lat_div.get_text(strip=True) if lat_div else 'N/A'

    opening_hours_div = detail_soup.select_one(".size12:nth-child(16)")
    opening_hours = opening_hours_div.get_text(strip=True) if opening_hours_div else 'N/A'

    fees_list = detail_soup.select("#id2 li")
    fees = "; ".join([fee.get_text(strip=True) for fee in fees_list]) if fees_list else 'N/A'

    with open(metadata_filename, mode='a', newline='', encoding='utf-8') as meta_file:
        meta_writer = csv.writer(meta_file)
        meta_writer.writerow([parking_id, parking_name, address, lon, lat, opening_hours, fees])

    print(f"📌 Metadata saved for: {parking_id} - {parking_name}")

print(f"🚀 All metadata saved to {metadata_filename}")
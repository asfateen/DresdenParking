# My Parking Project

This project is designed to scrape parking metadata and data from the Dresden parking website. It automates the process of collecting and updating information about parking locations, including their availability and fees.

## Project Structure

- **.github/workflows/update_metadata.yml**: GitHub Actions workflow for manually updating parking metadata.
- **.github/workflows/update_parking_data.yml**: GitHub Actions workflow that runs every 15 minutes to update parking data.
- **.gitignore**: Specifies files and directories to be ignored by Git.
- **metadata.csv**: Contains metadata for parking locations (ID, Parking Name, Address, GPS coordinates, Opening Hours, Fees).
- **parking_data.csv**: Stores scraped parking data (Timestamp, ID, Parking Name, Total Spaces, Free Spaces, Last Updated).
- **requirements.txt**: Lists Python dependencies required for the project (requests, beautifulsoup4).
- **scraper.py**: Python script that scrapes parking metadata and data from the website.

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/my-parking-project.git
   cd my-parking-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the scraper manually:
   ```
   python scraper.py
   ```

## Usage

- The metadata can be updated manually by triggering the `update_metadata.yml` workflow in GitHub Actions.
- The parking data is automatically updated every 15 minutes through the `update_parking_data.yml` workflow.

## Contributing

Feel free to submit issues or pull requests to improve the project!
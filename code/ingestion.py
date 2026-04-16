import os
import requests
import logging
import time
from dotenv import load_dotenv
from pymongo import MongoClient, errors, UpdateOne

# Loading environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in environment. Check your .env file.")

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("ingest.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration constants
DB_NAME = "climate_db"
COLLECTION_NAME = "temperature_anomalies"

# Berkeley Earth TAVG trend file URL pattern
BASE_URL = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Regional/TAVG/{country}-TAVG-Trend.txt"

# 10 countries representing 6 continents
COUNTRIES = [
    "united-states",  # North America
    "canada",         # North America
    "brazil",         # South America
    "germany",        # Europe
    "russia",         # Europe
    "nigeria",        # Africa
    "egypt",          # Africa
    "india",          # Asia
    "china",          # Asia
    "australia"       # Oceania
]

# Helper function to safely convert strings to floats, treating NaN and missing values as None
def safe_float(val):
    """Convert string to float, return None for NaN/missing values."""
    try:
        f = float(val)
        return None if f != f else f  
    except ValueError:
        return None


def fetch_country_data(country: str) -> list:
    """
    Fetches and parses the Berkeley Earth TAVG trend file for a given country.

    Args:
        country: Lowercase hyphenated country name (e.g. 'united-states')

    Returns:
        A list of document dicts, one per valid monthly observation.
        Returns empty list if the fetch or parse fails.
    """
    url = BASE_URL.format(country=country)
    documents = []

    # Fetching the data with a timeout and handle HTTP errors gracefully
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.warning(f"HTTP error fetching {country}: {e}")
        return documents
    except requests.exceptions.RequestException as e:
        logger.warning(f"Request failed for {country}: {e}")
        return documents

    try:
        # Skipping comment lines and parsing whitespace-delimited data
        lines = response.text.splitlines()
        data_lines = [l for l in lines if l.strip() and not l.strip().startswith("%")]

        for line in data_lines:
            parts = line.split()

            # Skipping rows that don't have at least year + month + monthly anomaly + uncertainty
            if len(parts) < 4:
                continue

            try:
                doc = {
                    "country": country,
                    "year": int(parts[0]),
                    "month": int(parts[1]),
                    "monthly_anomaly_c": safe_float(parts[2]),
                    "monthly_anomaly_unc_c": safe_float(parts[3]),
                    "annual_anomaly_c": safe_float(parts[4]) if len(parts) > 4 else None,
                    "annual_anomaly_unc_c": safe_float(parts[5]) if len(parts) > 5 else None,
                    "five_year_anomaly_c": safe_float(parts[6]) if len(parts) > 6 else None,
                    "five_year_unc_c": safe_float(parts[7]) if len(parts) > 7 else None,
                    "ten_year_anomaly_c": safe_float(parts[8]) if len(parts) > 8 else None,
                    "ten_year_unc_c": safe_float(parts[9]) if len(parts) > 9 else None,
                    "twenty_year_anomaly_c": safe_float(parts[10]) if len(parts) > 10 else None,
                    "twenty_year_unc_c": safe_float(parts[11]) if len(parts) > 11 else None,
                    "baseline": "1951-1980",
                    "source": "Berkeley Earth",
                    "source_url": url
                }
                documents.append(doc)

            except (ValueError, IndexError) as e:
                logger.debug(f"Skipping malformed row for {country}: {line.strip()} | {e}")
                continue

    except Exception as e:
        logger.error(f"Failed to parse data for {country}: {e}")

    logger.info(f"  {country}: {len(documents)} records parsed")
    return documents


def ingest_all(countries: list) -> None:
    """
    Main ingestion function. Fetches data for all countries and upserts
    into MongoDB. Uses upsert to avoid duplicate documents on re-runs.

    Args:
        countries: List of country name strings to ingest.
    """
    # Connecting to MongoDB Atlas
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()
        logger.info("Connected to MongoDB Atlas successfully.")
    except errors.ServerSelectionTimeoutError as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        return

    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Creating a unique index on (country, year, month) to prevent duplicates
    collection.create_index(
        [("country", 1), ("year", 1), ("month", 1)],
        unique=True,
        name="country_year_month_unique"
    )
    logger.info("Unique index on (country, year, month) ensured.")

    # Fetching and inserting data for each country
    total_inserted = 0
    total_updated = 0

    for i, country in enumerate(countries):
        logger.info(f"[{i+1}/{len(countries)}] Fetching: {country}")
        documents = fetch_country_data(country)

        if not documents:
            logger.warning(f"  No data retrieved for {country}, skipping.")
            continue

        # Building upsert operations to safely re-run without duplicates
        operations = [
            UpdateOne(
                filter={"country": doc["country"], "year": doc["year"], "month": doc["month"]},
                update={"$set": doc},
                upsert=True
            )
            for doc in documents
        ]

        try:
            result = collection.bulk_write(operations, ordered=False)
            total_inserted += result.upserted_count
            total_updated += result.modified_count
            logger.info(f"  Upserted: {result.upserted_count} new, {result.modified_count} updated")
        except errors.BulkWriteError as e:
            logger.error(f"  Bulk write error for {country}: {e.details}")

        # Small delay 
        time.sleep(0.2)

    # Summary of ingestion results
    final_count = collection.count_documents({})
    logger.info("=" * 50)
    logger.info(f"Ingestion complete.")
    logger.info(f"  New documents inserted: {total_inserted}")
    logger.info(f"  Documents updated:      {total_updated}")
    logger.info(f"  Total in collection:    {final_count}")
    logger.info("=" * 50)

    client.close()

if __name__ == "__main__":
    ingest_all(COUNTRIES)
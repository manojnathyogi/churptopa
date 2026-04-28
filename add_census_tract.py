#!/usr/bin/env python3
"""
Add Census Tract column to geocoded CSV files using the Formatted Address.
Uses the Census Bureau geocoding API.
"""

import csv
import time
import sys
from pathlib import Path

import requests


def get_full_census_tract(full_address):
    """
    Takes full DC address string
    Returns full 11-digit Census Tract GEOID (e.g. 11001009902)
    """
    if not full_address or not str(full_address).strip():
        return None

    url = "https://geocoding.geo.census.gov/geocoder/geographies/address"

    # Extract street part (before first comma) for Census API - we specify city/state separately
    street = str(full_address).split(",")[0].strip() if "," in str(full_address) else str(full_address).strip()

    params = {
        "street": street,
        "city": "Washington",
        "state": "DC",
        "benchmark": "Public_AR_Current",
        "vintage": "Current_Current",
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        matches = data.get("result", {}).get("addressMatches", [])
        if not matches:
            return None

        tract_info = matches[0]["geographies"]["Census Tracts"][0]

        state = tract_info["STATE"]
        county = tract_info["COUNTY"]
        tract = tract_info["TRACT"]

        # Full GEOID = State + County + Tract
        full_geoid = state + county + tract

        return full_geoid

    except Exception:
        return None


def add_census_tract_to_csv(input_path, output_path=None, cache=None):
    """Add Census Tract column to CSV using Formatted Address."""
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else input_path
    if cache is None:
        cache = {}

    rows = []
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Deduplicate fieldnames (keep first occurrence)
        raw_fieldnames = list(reader.fieldnames) if reader.fieldnames else []
        seen = []
        for fn in raw_fieldnames:
            if fn not in seen:
                seen.append(fn)
        fieldnames = seen
        if "Census Tract" not in fieldnames:
            fieldnames = fieldnames + ["Census Tract"]
        for row in reader:
            rows.append(row)

    total = len(rows)
    print(f"Processing {total} rows from {input_path.name}...")

    for i, row in enumerate(rows):
        formatted_addr = row.get("Formatted Address", "")
        existing = row.get("Census Tract", "")
        if formatted_addr in cache:
            tract = cache[formatted_addr]
        elif existing:
            tract = existing
            cache[formatted_addr] = tract
        else:
            tract = get_full_census_tract(formatted_addr)
            cache[formatted_addr] = tract
            time.sleep(0.1)  # Rate limit for API calls only
        row["Census Tract"] = tract if tract else ""

        if (i + 1) % 100 == 0:
            print(f"  Progress: {i + 1}/{total}", flush=True)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Done. Wrote to {output_path}")
    return output_path, cache


def load_cache_from_csv(csv_path):
    """Pre-load cache from a CSV that already has Census Tract column."""
    cache = {}
    path = Path(csv_path)
    if not path.exists():
        return cache
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "Census Tract" not in (reader.fieldnames or []):
            return cache
        for row in reader:
            addr = row.get("Formatted Address", "")
            tract = row.get("Census Tract", "")
            if addr and tract:
                cache[addr] = tract
    return cache


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    files = [
        script_dir / "final_merged_5_geocoded.csv",
        script_dir / "final_merged_24_geocoded.csv",
    ]

    # Pre-load cache from file 5 (already has Census Tract) to speed up file 24
    shared_cache = load_cache_from_csv(files[0])
    if shared_cache:
        print(f"Pre-loaded {len(shared_cache)} addresses from {files[0].name}")

    for fp in files:
        if fp.exists():
            _, shared_cache = add_census_tract_to_csv(fp, cache=shared_cache)
        else:
            print(f"File not found: {fp}", file=sys.stderr)

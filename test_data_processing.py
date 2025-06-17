#!/usr/bin/env python3
"""
Test script to debug data processing issues
"""

import sys
import os
sys.path.insert(0, 'src')

import requests
from data_processor import DataProcessor

def test_data_processing():
    # Get real SerpAPI data
    api_key = 'c84e8c2b0bcf76e9b1030c2a11100215c9a4f891d41c65f16d7f9136ddf57d2c'
    test_params = {
        'api_key': api_key,
        'engine': 'google',
        'q': 'plumbing repair',
        'location': 'Spokane, Washington, United States',
        'num': 10
    }

    print("Making SerpAPI request...")
    response = requests.get('https://serpapi.com/search', params=test_params, timeout=15)
    data = response.json()

    # Process it with our data processor
    print("Processing data...")
    processor = DataProcessor()
    processed = processor.process_search_results(data, 'plumbing repair', 'test')

    print('=== RAW SERPAPI DATA ===')
    print(f'Organic results: {len(data.get("organic_results", []))}')
    print(f'Local results type: {type(data.get("local_results", {}))}')
    print(f'Local services: {len(data.get("local_services", []))}')
    print(f'Available keys: {list(data.keys())}')

    # Check local_map structure
    local_map = data.get('local_map', {})
    print(f'Local map type: {type(local_map)}')
    print(f'Local map keys: {list(local_map.keys()) if isinstance(local_map, dict) else "Not a dict"}')
    if isinstance(local_map, dict) and 'places' in local_map:
        places = local_map['places']
        print(f'Local map places: {len(places)}')
        if places:
            print(f'First place: {places[0].get("title", "No title")}')
            print(f'First place keys: {list(places[0].keys())}')

    # Check local_results structure
    local_results = data.get('local_results', {})
    print(f'Local results keys: {list(local_results.keys()) if isinstance(local_results, dict) else "Not a dict"}')

    print('\n=== PROCESSED DATA ===')
    print(f'Maps listings: {len(processed["maps_listings"])}')
    print(f'Local services ads: {len(processed["local_services_ads"])}')
    print(f'Organic results: {len(processed["organic_results"])}')
    print(f'Has error: {processed.get("error", False)}')

    if processed['organic_results']:
        print(f'First organic result: {processed["organic_results"][0]["title"]}')
    
    if processed['maps_listings']:
        print(f'First maps listing: {processed["maps_listings"][0]["title"]}')

    # Test aggregation
    print('\n=== TESTING AGGREGATION ===')
    aggregated = processor.aggregate_results([processed])
    print(f'Total keywords: {aggregated["summary"]["total_keywords"]}')
    print(f'Successful searches: {aggregated["summary"]["successful_searches"]}')
    print(f'Failed searches: {aggregated["summary"]["failed_searches"]}')

if __name__ == "__main__":
    test_data_processing()

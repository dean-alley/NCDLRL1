#!/usr/bin/env python3
"""
Debug script to trace data flow through LocalRankLens pipeline
"""

import sys
import json
import logging
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config_manager import ConfigManager
from search_scraper import SearchScraper
from data_processor import DataProcessor
from report_writer import ReportWriter

def setup_debug_logging():
    """Setup detailed logging for debugging."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('debug_data_flow.log')
        ]
    )

def debug_single_keyword(keyword="sprinkler system installation Spokane", location="Spokane, WA"):
    """Debug the complete flow for a single keyword."""
    print(f"\n=== DEBUGGING KEYWORD: '{keyword}' in {location} ===\n")
    
    # Initialize components
    config_manager = ConfigManager()
    api_key = config_manager.get_serpapi_key()
    
    search_scraper = SearchScraper(api_key, rate_limit_delay=0.5)
    data_processor = DataProcessor()
    
    # Step 1: Raw SerpAPI Response
    print("STEP 1: Getting raw SerpAPI response...")
    try:
        raw_response = search_scraper.search(keyword, location)
        print(f"✓ Raw response keys: {list(raw_response.keys())}")
        
        # Save raw response for inspection
        with open('debug_raw_response.json', 'w') as f:
            json.dump(raw_response, f, indent=2)
        print("✓ Raw response saved to debug_raw_response.json")
        
        # Check for key data sections
        maps_data = raw_response.get('local_results', [])
        local_services = raw_response.get('local_services', [])
        organic_data = raw_response.get('organic_results', [])
        
        print(f"  - local_results (Maps): {len(maps_data)} items")
        print(f"  - local_services: {len(local_services)} items")
        print(f"  - organic_results: {len(organic_data)} items")
        
    except Exception as e:
        print(f"✗ SerpAPI search failed: {e}")
        return
    
    # Step 2: Data Processing
    print("\nSTEP 2: Processing data...")
    try:
        processed_data = data_processor.process_search_results(
            raw_response, keyword, "debug_group"
        )
        
        # Save processed data for inspection
        with open('debug_processed_data.json', 'w') as f:
            json.dump(processed_data, f, indent=2)
        print("✓ Processed data saved to debug_processed_data.json")
        
        # Check processed data counts
        maps_count = len(processed_data.get('maps_listings', []))
        local_services_count = len(processed_data.get('local_services_ads', []))
        organic_count = len(processed_data.get('organic_results', []))
        
        print(f"  - maps_listings: {maps_count} items")
        print(f"  - local_services_ads: {local_services_count} items")
        print(f"  - organic_results: {organic_count} items")
        
        # Show sample data
        if maps_count > 0:
            print(f"  - Sample maps listing: {processed_data['maps_listings'][0].get('title', 'No title')}")
        if local_services_count > 0:
            print(f"  - Sample local service: {processed_data['local_services_ads'][0].get('title', 'No title')}")
        if organic_count > 0:
            print(f"  - Sample organic result: {processed_data['organic_results'][0].get('title', 'No title')}")
            
    except Exception as e:
        print(f"✗ Data processing failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 3: Aggregation
    print("\nSTEP 3: Aggregating results...")
    try:
        aggregated_data = data_processor.aggregate_results([processed_data])
        
        # Save aggregated data for inspection
        with open('debug_aggregated_data.json', 'w') as f:
            json.dump(aggregated_data, f, indent=2)
        print("✓ Aggregated data saved to debug_aggregated_data.json")
        
        # Check aggregated counts
        summary = aggregated_data.get('summary', {})
        print(f"  - Total keywords: {summary.get('total_keywords', 0)}")
        print(f"  - Successful searches: {summary.get('successful_searches', 0)}")
        
        by_group = aggregated_data.get('by_keyword_group', {})
        for group_name, group_data in by_group.items():
            print(f"  - Group '{group_name}':")
            print(f"    - Maps listings: {group_data.get('total_maps_listings', 0)}")
            print(f"    - Local services: {group_data.get('total_local_services', 0)}")
            print(f"    - Organic results: {group_data.get('total_organic_results', 0)}")
            
    except Exception as e:
        print(f"✗ Aggregation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Report Generation
    print("\nSTEP 4: Generating report...")
    try:
        report_writer = ReportWriter(
            template_dir="templates",
            output_dir="debug_output"
        )
        
        # Create output directory
        Path("debug_output").mkdir(exist_ok=True)
        
        report_path = report_writer.generate_report(
            aggregated_data, "Debug Business", location, "debug"
        )
        print(f"✓ Report generated: {report_path}")
        
        # Check template data preparation
        template_data = report_writer._prepare_template_data(
            aggregated_data, "Debug Business", location
        )
        
        with open('debug_template_data.json', 'w') as f:
            json.dump(template_data, f, indent=2)
        print("✓ Template data saved to debug_template_data.json")
        
        print(f"  - Total maps listings in template: {template_data.get('total_maps_listings', 0)}")
        print(f"  - Total local services in template: {template_data.get('total_local_services', 0)}")
        print(f"  - Total organic results in template: {template_data.get('total_organic_results', 0)}")
        
    except Exception as e:
        print(f"✗ Report generation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n=== DEBUG COMPLETE ===")
    print("Check the generated JSON files for detailed data inspection:")
    print("- debug_raw_response.json")
    print("- debug_processed_data.json") 
    print("- debug_aggregated_data.json")
    print("- debug_template_data.json")
    print(f"- {report_path}")

if __name__ == "__main__":
    setup_debug_logging()
    debug_single_keyword()

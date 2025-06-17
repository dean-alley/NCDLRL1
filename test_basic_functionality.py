#!/usr/bin/env python3
"""
Basic functionality test for LocalRankLens

Tests the core components without making actual API calls.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from config_manager import ConfigManager, ConfigurationError
        print("✓ config_manager imported successfully")
        
        from search_scraper import SearchScraper, SearchScraperError
        print("✓ search_scraper imported successfully")
        
        from data_processor import DataProcessor
        print("✓ data_processor imported successfully")
        
        from report_writer import ReportWriter, ReportWriterError
        print("✓ report_writer imported successfully")
        
        from localranklens import LocalRankLens
        print("✓ localranklens imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_config_manager():
    """Test configuration manager with the actual config file."""
    print("\nTesting ConfigManager...")
    
    try:
        from config_manager import ConfigManager
        
        # Test with actual config file
        config = ConfigManager('config.json')
        
        print(f"✓ Business name: {config.get_business_name()}")
        print(f"✓ Location: {config.get_location_string()}")
        print(f"✓ Keyword groups: {config.get_keyword_groups()}")
        print(f"✓ Output prefix: {config.get_output_prefix()}")
        
        # Test report settings
        settings = config.get_report_settings()
        print(f"✓ Report settings loaded: {len(settings)} settings")
        
        return True
        
    except Exception as e:
        print(f"✗ ConfigManager test failed: {e}")
        return False

def test_data_processor():
    """Test data processor with mock data."""
    print("\nTesting DataProcessor...")
    
    try:
        from data_processor import DataProcessor
        
        processor = DataProcessor()
        
        # Create mock SerpAPI response
        mock_response = {
            'search_metadata': {
                'query': 'test query',
                'location': 'Test City, TS',
                'total_results': 1000
            },
            'local_results': [
                {
                    'position': 1,
                    'title': 'Test Business',
                    'rating': 4.5,
                    'reviews': 100,
                    'phone': '(555) 123-4567',
                    'address': '123 Test St'
                }
            ],
            'organic_results': [
                {
                    'position': 1,
                    'title': 'Test Result',
                    'link': 'https://example.com',
                    'snippet': 'Test snippet'
                }
            ]
        }
        
        # Process the mock data
        result = processor.process_search_results(
            mock_response, 'test keyword', 'test_group'
        )
        
        print(f"✓ Processed search results for: {result['keyword']}")
        print(f"✓ Found {len(result['maps_listings'])} maps listings")
        print(f"✓ Found {len(result['organic_results'])} organic results")
        
        # Test aggregation
        aggregated = processor.aggregate_results([result])
        print(f"✓ Aggregated results: {aggregated['summary']['total_keywords']} keywords")
        
        return True
        
    except Exception as e:
        print(f"✗ DataProcessor test failed: {e}")
        return False

def test_report_writer():
    """Test report writer with mock data."""
    print("\nTesting ReportWriter...")
    
    try:
        from report_writer import ReportWriter
        from data_processor import DataProcessor
        
        # Create mock aggregated data
        mock_aggregated_data = {
            'summary': {
                'total_keywords': 1,
                'successful_searches': 1,
                'failed_searches': 0
            },
            'by_keyword_group': {
                'test_group': {
                    'keyword_count': 1,
                    'successful_searches': 1,
                    'total_maps_listings': 1,
                    'total_local_services': 0,
                    'total_organic_results': 1,
                    'results': [
                        {
                            'keyword': 'test keyword',
                            'keyword_group': 'test_group',
                            'maps_listings': [
                                {
                                    'title': 'Test Business',
                                    'rating': 4.5,
                                    'reviews': 100,
                                    'phone': '(555) 123-4567'
                                }
                            ],
                            'organic_results': [
                                {
                                    'title': 'Test Result',
                                    'domain': 'example.com',
                                    'position': 1
                                }
                            ],
                            'local_services_ads': []
                        }
                    ]
                }
            }
        }
        
        # Test report generation
        writer = ReportWriter(template_dir="templates", output_dir="output")
        
        # Generate summary report (doesn't require template)
        summary = writer.generate_summary_report(
            mock_aggregated_data, 
            "Test Business", 
            "Test City, TS"
        )
        
        print(f"✓ Generated summary report for: {summary['business_name']}")
        print(f"✓ Summary contains {summary['total_keywords']} keywords")
        
        return True
        
    except Exception as e:
        print(f"✗ ReportWriter test failed: {e}")
        return False

def test_directory_structure():
    """Test that required directories exist."""
    print("\nTesting directory structure...")
    
    required_dirs = ['src', 'templates', 'output', 'tests']
    required_files = ['config.json', 'requirements.txt', 'README.md']
    
    all_good = True
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✓ Directory exists: {directory}")
        else:
            print(f"✗ Missing directory: {directory}")
            all_good = False
    
    for file in required_files:
        if Path(file).exists():
            print(f"✓ File exists: {file}")
        else:
            print(f"✗ Missing file: {file}")
            all_good = False
    
    return all_good

def main():
    """Run all basic tests."""
    print("="*60)
    print("LocalRankLens Basic Functionality Test")
    print("="*60)
    
    tests = [
        test_directory_structure,
        test_imports,
        test_config_manager,
        test_data_processor,
        test_report_writer
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"Test {test.__name__} failed")
        except Exception as e:
            print(f"Test {test.__name__} crashed: {e}")
    
    print("\n" + "="*60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic functionality tests passed!")
        print("The LocalRankLens components are working correctly.")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    print("="*60)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

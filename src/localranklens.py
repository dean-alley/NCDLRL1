"""
LocalRankLens - Main Orchestrator

Main entry point that coordinates all modules and handles the complete workflow
for local search competitive intelligence analysis.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, List

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_manager import ConfigManager, ConfigurationError, setup_logging
from search_scraper import SearchScraper, SearchScraperError
from data_processor import DataProcessor
from report_writer import ReportWriter, ReportWriterError


class LocalRankLens:
    """Main orchestrator for the LocalRankLens application."""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize LocalRankLens with configuration.
        
        Args:
            config_path: Path to the configuration file
        """
        self.logger = None
        self.config_manager = None
        self.search_scraper = None
        self.data_processor = None
        self.report_writer = None
        
        try:
            # Load configuration
            self.config_manager = ConfigManager(config_path)
            
            # Set up logging
            setup_logging(self.config_manager)
            self.logger = logging.getLogger(__name__)
            
            self.logger.info("LocalRankLens initialized successfully")
            
        except ConfigurationError as e:
            print(f"Configuration error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Initialization error: {e}")
            sys.exit(1)
    
    def initialize_components(self) -> None:
        """Initialize all components with proper error handling."""
        try:
            # Initialize search scraper
            api_key = self.config_manager.get_serpapi_key()
            self.search_scraper = SearchScraper(api_key, rate_limit_delay=1.5)
            
            # Validate API key
            if not self.search_scraper.validate_api_key():
                raise SearchScraperError("Invalid SerpAPI key")
            
            # Initialize data processor
            self.data_processor = DataProcessor()
            
            # Initialize report writer
            self.report_writer = ReportWriter(
                template_dir="templates",
                output_dir=str(self.config_manager.get_output_dir())
            )
            
            self.logger.info("All components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Component initialization failed: {e}")
            raise
    
    def run_analysis(self) -> str:
        """
        Run the complete analysis workflow.
        
        Returns:
            Path to the generated report
        """
        try:
            self.logger.info("Starting LocalRankLens analysis")
            
            # Initialize components
            self.initialize_components()
            
            # Get configuration data
            business_name = self.config_manager.get_business_name()
            location = self.config_manager.get_location_string()
            keywords = self.config_manager.get_keywords()
            output_prefix = self.config_manager.get_output_prefix()
            
            self.logger.info(f"Analyzing {business_name} in {location}")
            
            # Collect all search results
            all_results = []
            
            for group_name, keyword_list in keywords.items():
                self.logger.info(f"Processing {group_name} keywords ({len(keyword_list)} keywords)")
                
                for keyword in keyword_list:
                    try:
                        # Perform search
                        search_result = self.search_scraper.search(keyword, location)
                        
                        # Process the data
                        processed_data = self.data_processor.process_search_results(
                            search_result, keyword, group_name
                        )
                        
                        all_results.append(processed_data)
                        
                        self.logger.info(f"Successfully processed: {keyword}")
                        
                    except SearchScraperError as e:
                        self.logger.error(f"Search failed for '{keyword}': {e}")
                        # Add error result
                        error_result = self.data_processor._create_empty_result(keyword, group_name)
                        error_result['error_message'] = str(e)
                        all_results.append(error_result)
                    
                    except Exception as e:
                        self.logger.error(f"Unexpected error processing '{keyword}': {e}")
                        error_result = self.data_processor._create_empty_result(keyword, group_name)
                        error_result['error_message'] = f"Unexpected error: {e}"
                        all_results.append(error_result)
            
            # Aggregate results
            self.logger.info("Aggregating results for reporting")
            aggregated_data = self.data_processor.aggregate_results(all_results)
            
            # Generate report
            self.logger.info("Generating HTML report")
            report_path = self.report_writer.generate_report(
                aggregated_data, business_name, location, output_prefix
            )
            
            # Generate summary
            summary = self.report_writer.generate_summary_report(
                aggregated_data, business_name, location
            )
            
            # Log summary statistics
            self._log_summary_stats(summary)
            
            self.logger.info(f"Analysis completed successfully. Report saved to: {report_path}")
            return report_path
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            raise

    def _log_summary_stats(self, summary: Dict[str, Any]) -> None:
        """Log summary statistics."""
        self.logger.info("=== ANALYSIS SUMMARY ===")
        self.logger.info(f"Business: {summary['business_name']}")
        self.logger.info(f"Location: {summary['location']}")
        self.logger.info(f"Total Keywords: {summary['total_keywords']}")
        self.logger.info(f"Successful Searches: {summary['successful_searches']}")
        self.logger.info(f"Total Competitors Found: {summary['total_competitors']}")

        if summary['top_competing_domains']:
            self.logger.info("Top Competing Domains:")
            for domain, count in summary['top_competing_domains'][:5]:
                self.logger.info(f"  - {domain}: {count} appearances")

        for group_name, group_stats in summary['keyword_groups'].items():
            self.logger.info(f"{group_name.title()} Group:")
            self.logger.info(f"  - Keywords: {group_stats['keyword_count']}")
            self.logger.info(f"  - Maps Listings: {group_stats['maps_listings']}")
            self.logger.info(f"  - Local Services: {group_stats['local_services']}")
            self.logger.info(f"  - Organic Results: {group_stats['organic_results']}")


def main():
    """Main entry point for the application."""
    try:
        # Check for custom config path from environment variable
        import os
        config_path = os.environ.get('CONFIG_PATH', 'config.json')

        # Create and run LocalRankLens with custom config path
        lrl = LocalRankLens(config_path=config_path)
        report_path = lrl.run_analysis()

        print("\n" + "="*60)
        print("LocalRankLens Analysis Complete!")
        print("="*60)
        print(f"Report generated: {report_path}")
        print(f"Open the file in your browser to view the results")
        print("="*60)

        return 0

    except KeyboardInterrupt:
        print("\nAnalysis cancelled by user")
        return 1

    except Exception as e:
        print(f"\nAnalysis failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

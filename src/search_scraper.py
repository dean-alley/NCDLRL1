"""
Search Scraper for LocalRankLens

Handles SerpAPI integration with error handling, rate limiting, and retry logic.
"""

import time
import logging
import requests
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class SearchScraperError(Exception):
    """Custom exception for search scraper errors."""
    pass


class SearchScraper:
    """Handles search queries using SerpAPI with robust error handling."""
    
    def __init__(self, api_key: str, rate_limit_delay: float = 1.0):
        """
        Initialize the search scraper.
        
        Args:
            api_key: SerpAPI key
            rate_limit_delay: Delay between requests in seconds
        """
        self.api_key = api_key
        self.rate_limit_delay = rate_limit_delay
        self.base_url = "https://serpapi.com/search"
        self.logger = logging.getLogger(__name__)
        
        # Set up session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.last_request_time = 0
    
    def search(self, query: str, location: str, **kwargs) -> Dict[str, Any]:
        """
        Perform a search query using SerpAPI.
        
        Args:
            query: Search query string
            location: Location for the search (e.g., "Seattle, WA")
            **kwargs: Additional parameters for SerpAPI
            
        Returns:
            SerpAPI response as dictionary
            
        Raises:
            SearchScraperError: If the search fails
        """
        # Rate limiting
        self._enforce_rate_limit()
        
        # Prepare search parameters
        params = {
            'api_key': self.api_key,
            'engine': 'google',
            'q': query,
            'location': location,
            'google_domain': 'google.com',
            'gl': 'us',
            'hl': 'en',
            'num': kwargs.get('num_results', 10),
            'start': kwargs.get('start', 0)
        }
        
        # Add any additional parameters
        params.update(kwargs)
        
        try:
            self.logger.info(f"Searching for '{query}' in '{location}'")
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for SerpAPI errors
            if 'error' in data:
                error_msg = data['error']
                self.logger.error(f"SerpAPI error: {error_msg}")
                raise SearchScraperError(f"SerpAPI error: {error_msg}")
            
            self.logger.info(f"Successfully retrieved search results for '{query}'")
            return data
            
        except requests.exceptions.RequestException as e:
            error_msg = f"HTTP request failed for query '{query}': {e}"
            self.logger.error(error_msg)
            raise SearchScraperError(error_msg)
        
        except ValueError as e:
            error_msg = f"Failed to parse JSON response for query '{query}': {e}"
            self.logger.error(error_msg)
            raise SearchScraperError(error_msg)
        
        except Exception as e:
            error_msg = f"Unexpected error during search for '{query}': {e}"
            self.logger.error(error_msg)
            raise SearchScraperError(error_msg)
    
    def search_local(self, query: str, location: str) -> Dict[str, Any]:
        """
        Perform a local search optimized for local business results.
        
        Args:
            query: Search query string
            location: Location for the search
            
        Returns:
            SerpAPI response with local results
        """
        return self.search(
            query=query,
            location=location,
            tbm='lcl',  # Local search
            num_results=20  # Get more results for local searches
        )
    
    def search_maps(self, query: str, location: str) -> Dict[str, Any]:
        """
        Perform a Google Maps search.
        
        Args:
            query: Search query string
            location: Location for the search
            
        Returns:
            SerpAPI response with maps results
        """
        params = {
            'api_key': self.api_key,
            'engine': 'google_maps',
            'q': query,
            'location': location,
            'type': 'search'
        }
        
        # Rate limiting
        self._enforce_rate_limit()
        
        try:
            self.logger.info(f"Maps search for '{query}' in '{location}'")
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'error' in data:
                error_msg = data['error']
                self.logger.error(f"SerpAPI Maps error: {error_msg}")
                raise SearchScraperError(f"SerpAPI Maps error: {error_msg}")
            
            self.logger.info(f"Successfully retrieved maps results for '{query}'")
            return data
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Maps search failed for query '{query}': {e}"
            self.logger.error(error_msg)
            raise SearchScraperError(error_msg)
        
        except Exception as e:
            error_msg = f"Unexpected error during maps search for '{query}': {e}"
            self.logger.error(error_msg)
            raise SearchScraperError(error_msg)
    
    def batch_search(self, queries: list, location: str, 
                    search_type: str = 'regular') -> Dict[str, Dict[str, Any]]:
        """
        Perform multiple searches with proper rate limiting.
        
        Args:
            queries: List of search queries
            location: Location for all searches
            search_type: Type of search ('regular', 'local', 'maps')
            
        Returns:
            Dictionary mapping queries to their results
        """
        results = {}
        total_queries = len(queries)
        
        self.logger.info(f"Starting batch search for {total_queries} queries")
        
        for i, query in enumerate(queries, 1):
            try:
                self.logger.info(f"Processing query {i}/{total_queries}: {query}")
                
                if search_type == 'local':
                    result = self.search_local(query, location)
                elif search_type == 'maps':
                    result = self.search_maps(query, location)
                else:
                    result = self.search(query, location)
                
                results[query] = result
                
                # Progress logging
                if i % 5 == 0 or i == total_queries:
                    self.logger.info(f"Completed {i}/{total_queries} searches")
                
            except SearchScraperError as e:
                self.logger.error(f"Failed to search for '{query}': {e}")
                results[query] = {'error': str(e)}
            
            except Exception as e:
                self.logger.error(f"Unexpected error searching for '{query}': {e}")
                results[query] = {'error': f"Unexpected error: {e}"}
        
        successful_searches = len([r for r in results.values() if 'error' not in r])
        self.logger.info(f"Batch search completed: {successful_searches}/{total_queries} successful")
        
        return results
    
    def _enforce_rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last_request
            self.logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def validate_api_key(self) -> bool:
        """
        Validate the SerpAPI key by making a test request.
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            test_params = {
                'api_key': self.api_key,
                'engine': 'google',
                'q': 'test',
                'location': 'United States',
                'num': 1
            }
            
            response = self.session.get(self.base_url, params=test_params, timeout=10)
            data = response.json()
            
            if 'error' in data:
                self.logger.error(f"API key validation failed: {data['error']}")
                return False
            
            self.logger.info("API key validation successful")
            return True
            
        except Exception as e:
            self.logger.error(f"API key validation error: {e}")
            return False
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information from SerpAPI.
        
        Returns:
            Account information dictionary
        """
        try:
            url = "https://serpapi.com/account"
            params = {'api_key': self.api_key}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Failed to get account info: {e}")
            return {'error': str(e)}

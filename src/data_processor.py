"""
Data Processor for LocalRankLens

Extracts and structures data from SerpAPI responses including:
- Google Maps listings
- Local Services Ads
- Organic search results
"""

import logging
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse


class DataProcessor:
    """Processes and extracts structured data from SerpAPI responses."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.logger = logging.getLogger(__name__)
    
    def process_search_results(self, serpapi_response: Dict[str, Any], keyword: str, 
                             keyword_group: str) -> Dict[str, Any]:
        """
        Process a complete SerpAPI response and extract structured data.
        
        Args:
            serpapi_response: Raw response from SerpAPI
            keyword: The search keyword used
            keyword_group: The group this keyword belongs to
            
        Returns:
            Structured data dictionary
        """
        try:
            processed_data = {
                'keyword': keyword,
                'keyword_group': keyword_group,
                'search_metadata': self._extract_search_metadata(serpapi_response),
                'maps_listings': self._extract_maps_listings(serpapi_response),
                'local_services_ads': self._extract_local_services_ads(serpapi_response),
                'organic_results': self._extract_organic_results(serpapi_response),
                'ads': self._extract_ads(serpapi_response),
                'knowledge_graph': self._extract_knowledge_graph(serpapi_response)
            }
            
            self.logger.info(f"Processed search results for keyword: {keyword}")
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Error processing search results for {keyword}: {e}")
            self.logger.error(f"Exception type: {type(e)}")
            self.logger.error(f"Response keys: {list(serpapi_response.keys()) if isinstance(serpapi_response, dict) else 'Not a dict'}")
            import traceback
            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            return self._create_empty_result(keyword, keyword_group)
    
    def _extract_search_metadata(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract search metadata from the response."""
        search_metadata = response.get('search_metadata', {})
        return {
            'query': search_metadata.get('query', ''),
            'location': search_metadata.get('location', ''),
            'total_results': search_metadata.get('total_results', 0),
            'time_taken': search_metadata.get('total_time_taken', 0),
            'search_url': search_metadata.get('google_url', '')
        }
    
    def _extract_maps_listings(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract Google Maps listings from the response."""
        local_results = response.get('local_results', [])
        maps_listings = []

        # Debug: Check what type local_results is
        self.logger.debug(f"local_results type: {type(local_results)}, value: {local_results}")

        # Ensure local_results is a list before slicing
        if not isinstance(local_results, list):
            self.logger.warning(f"local_results is not a list, it's {type(local_results)}. Converting to empty list.")
            local_results = []

        for result in local_results[:3]:  # Top 3 results
            listing = {
                'position': result.get('position', 0),
                'title': result.get('title', ''),
                'business_name': result.get('title', ''),
                'rating': result.get('rating', 0),
                'reviews': result.get('reviews', 0),
                'type': result.get('type', ''),
                'address': result.get('address', ''),
                'phone': result.get('phone', ''),
                'website': result.get('website', ''),
                'hours': result.get('hours', ''),
                'service_options': result.get('service_options', {}),
                'gps_coordinates': result.get('gps_coordinates', {}),
                'place_id': result.get('place_id', ''),
                'thumbnail': result.get('thumbnail', '')
            }
            maps_listings.append(listing)
        
        self.logger.debug(f"Extracted {len(maps_listings)} maps listings")
        return maps_listings
    
    def _extract_local_services_ads(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract Local Services Ads from the response."""
        local_services = response.get('local_services', [])
        ads_listings = []

        # Ensure local_services is a list
        if not isinstance(local_services, list):
            self.logger.warning(f"local_services is not a list, it's {type(local_services)}. Converting to empty list.")
            local_services = []

        for ad in local_services:
            ad_data = {
                'position': ad.get('position', 0),
                'title': ad.get('title', ''),
                'phone': ad.get('phone', ''),
                'website': ad.get('website', ''),
                'rating': ad.get('rating', 0),
                'reviews': ad.get('reviews', 0),
                'years_in_business': ad.get('years_in_business', ''),
                'license_info': ad.get('license_info', ''),
                'thumbnail': ad.get('thumbnail', ''),
                'service_areas': ad.get('service_areas', [])
            }
            ads_listings.append(ad_data)
        
        self.logger.debug(f"Extracted {len(ads_listings)} local services ads")
        return ads_listings
    
    def _extract_organic_results(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract organic search results from the response."""
        organic_results = response.get('organic_results', [])
        structured_results = []

        # Ensure organic_results is a list
        if not isinstance(organic_results, list):
            self.logger.warning(f"organic_results is not a list, it's {type(organic_results)}. Converting to empty list.")
            organic_results = []

        for result in organic_results[:5]:  # Top 5 results
            organic_data = {
                'position': result.get('position', 0),
                'title': result.get('title', ''),
                'link': result.get('link', ''),
                'domain': self._extract_domain(result.get('link', '')),
                'snippet': result.get('snippet', ''),
                'displayed_link': result.get('displayed_link', ''),
                'favicon': result.get('favicon', ''),
                'sitelinks': result.get('sitelinks', []),
                'rich_snippet': result.get('rich_snippet', {}),
                'about_this_result': result.get('about_this_result', {})
            }
            structured_results.append(organic_data)
        
        self.logger.debug(f"Extracted {len(structured_results)} organic results")
        return structured_results
    
    def _extract_ads(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract paid ads from the response."""
        ads = response.get('ads', [])
        structured_ads = []

        # Ensure ads is a list
        if not isinstance(ads, list):
            self.logger.warning(f"ads is not a list, it's {type(ads)}. Converting to empty list.")
            ads = []

        for ad in ads:
            ad_data = {
                'position': ad.get('position', 0),
                'title': ad.get('title', ''),
                'link': ad.get('link', ''),
                'domain': self._extract_domain(ad.get('link', '')),
                'displayed_link': ad.get('displayed_link', ''),
                'snippet': ad.get('snippet', ''),
                'extensions': ad.get('extensions', []),
                'tracking_link': ad.get('tracking_link', '')
            }
            structured_ads.append(ad_data)
        
        self.logger.debug(f"Extracted {len(structured_ads)} paid ads")
        return structured_ads
    
    def _extract_knowledge_graph(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract knowledge graph information if present."""
        knowledge_graph = response.get('knowledge_graph', {})
        
        if not knowledge_graph:
            return {}
        
        return {
            'title': knowledge_graph.get('title', ''),
            'type': knowledge_graph.get('type', ''),
            'description': knowledge_graph.get('description', ''),
            'website': knowledge_graph.get('website', ''),
            'phone': knowledge_graph.get('phone', ''),
            'address': knowledge_graph.get('address', ''),
            'hours': knowledge_graph.get('hours', {}),
            'rating': knowledge_graph.get('rating', 0),
            'reviews': knowledge_graph.get('reviews', 0),
            'thumbnail': knowledge_graph.get('thumbnail', '')
        }
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from a URL."""
        if not url:
            return ''
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            # Remove www. prefix if present
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except Exception:
            return ''
    
    def _create_empty_result(self, keyword: str, keyword_group: str) -> Dict[str, Any]:
        """Create an empty result structure for failed processing."""
        return {
            'keyword': keyword,
            'keyword_group': keyword_group,
            'search_metadata': {},
            'maps_listings': [],
            'local_services_ads': [],
            'organic_results': [],
            'ads': [],
            'knowledge_graph': {},
            'error': True
        }
    
    def aggregate_results(self, all_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate results from multiple keywords for reporting.
        
        Args:
            all_results: List of processed search results
            
        Returns:
            Aggregated data organized by keyword groups
        """
        aggregated = {
            'summary': {
                'total_keywords': len(all_results),
                'successful_searches': len([r for r in all_results if not r.get('error', False)]),
                'failed_searches': len([r for r in all_results if r.get('error', False)])
            },
            'by_keyword_group': {},
            'all_results': all_results
        }
        
        # Group results by keyword group
        for result in all_results:
            group = result['keyword_group']
            if group not in aggregated['by_keyword_group']:
                aggregated['by_keyword_group'][group] = []
            aggregated['by_keyword_group'][group].append(result)
        
        # Add group-level statistics
        for group, results in aggregated['by_keyword_group'].items():
            group_stats = {
                'keyword_count': len(results),
                'successful_searches': len([r for r in results if not r.get('error', False)]),
                'total_maps_listings': sum(len(r['maps_listings']) for r in results),
                'total_local_services': sum(len(r['local_services_ads']) for r in results),
                'total_organic_results': sum(len(r['organic_results']) for r in results),
                'results': results
            }
            aggregated['by_keyword_group'][group] = group_stats
        
        self.logger.info(f"Aggregated {len(all_results)} search results into {len(aggregated['by_keyword_group'])} groups")
        return aggregated

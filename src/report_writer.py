"""
Report Writer for LocalRankLens

Generates professional HTML reports using Jinja2 templating with 
timestamped filenames and organized data presentation.
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, Template


class ReportWriterError(Exception):
    """Custom exception for report writer errors."""
    pass


class ReportWriter:
    """Generates professional HTML reports from processed search data."""
    
    def __init__(self, template_dir: str = "templates", output_dir: str = "output"):
        """
        Initialize the report writer.
        
        Args:
            template_dir: Directory containing Jinja2 templates
            output_dir: Directory for generated reports
        """
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.logger = logging.getLogger(__name__)
        
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)
        
        # Set up Jinja2 environment
        if self.template_dir.exists():
            self.jinja_env = Environment(
                loader=FileSystemLoader(str(self.template_dir)),
                autoescape=True
            )
        else:
            self.logger.warning(f"Template directory {self.template_dir} not found")
            self.jinja_env = None
    
    def generate_report(self, aggregated_data: Dict[str, Any], 
                       business_name: str, location: str, 
                       output_prefix: str) -> str:
        """
        Generate a complete HTML report from aggregated search data.
        
        Args:
            aggregated_data: Processed and aggregated search results
            business_name: Name of the business being analyzed
            location: Location string (e.g., "Seattle, WA")
            output_prefix: Prefix for the output filename
            
        Returns:
            Path to the generated report file
            
        Raises:
            ReportWriterError: If report generation fails
        """
        try:
            # Prepare template data
            template_data = self._prepare_template_data(
                aggregated_data, business_name, location
            )
            
            # Generate HTML content
            html_content = self._render_template(template_data)
            
            # Generate filename with timestamp
            filename = self._generate_filename(output_prefix)
            
            # Write report to file
            report_path = self.output_dir / filename
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Report generated successfully: {report_path}")
            return str(report_path)
            
        except Exception as e:
            error_msg = f"Failed to generate report: {e}"
            self.logger.error(error_msg)
            raise ReportWriterError(error_msg)
    
    def _prepare_template_data(self, aggregated_data: Dict[str, Any], 
                              business_name: str, location: str) -> Dict[str, Any]:
        """Prepare data for template rendering."""
        summary = aggregated_data.get('summary', {})
        by_group = aggregated_data.get('by_keyword_group', {})
        
        # Calculate totals
        total_maps_listings = sum(
            group.get('total_maps_listings', 0) 
            for group in by_group.values()
        )
        total_local_services = sum(
            group.get('total_local_services', 0) 
            for group in by_group.values()
        )
        total_organic_results = sum(
            group.get('total_organic_results', 0) 
            for group in by_group.values()
        )
        
        template_data = {
            'business_name': business_name,
            'location': location,
            'report_date': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
            'total_keywords': summary.get('total_keywords', 0),
            'summary': summary,
            'total_maps_listings': total_maps_listings,
            'total_local_services': total_local_services,
            'total_organic_results': total_organic_results,
            'results_by_group': by_group,
            'competitive_insights': self._generate_insights(aggregated_data)
        }
        
        return template_data
    
    def _render_template(self, template_data: Dict[str, Any]) -> str:
        """Render the HTML template with data."""
        if not self.jinja_env:
            # Fallback to basic HTML if no template environment
            return self._generate_basic_html(template_data)
        
        try:
            template = self.jinja_env.get_template('report_template.html')
            return template.render(**template_data)
        except Exception as e:
            self.logger.warning(f"Template rendering failed, using fallback: {e}")
            return self._generate_basic_html(template_data)
    
    def _generate_basic_html(self, data: Dict[str, Any]) -> str:
        """Generate basic HTML report as fallback."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>LocalRankLens Report - {data['business_name']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: #f0f0f0; padding: 20px; margin-bottom: 30px; }}
                .group {{ margin-bottom: 30px; border: 1px solid #ddd; padding: 20px; }}
                .keyword {{ margin-bottom: 20px; }}
                .result {{ margin: 10px 0; padding: 10px; background: #f9f9f9; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>LocalRankLens Report</h1>
                <h2>{data['business_name']} - {data['location']}</h2>
                <p>Generated on {data['report_date']}</p>
                <p>Total Keywords: {data['total_keywords']}</p>
            </div>
        """
        
        for group_name, group_data in data['results_by_group'].items():
            html += f"""
            <div class="group">
                <h3>{group_name.title()} Keywords</h3>
            """
            
            for result in group_data.get('results', []):
                if result.get('error'):
                    continue
                    
                html += f"""
                <div class="keyword">
                    <h4>"{result['keyword']}"</h4>
                """
                
                # Maps listings
                if result.get('maps_listings'):
                    html += "<h5>Google Maps Listings:</h5>"
                    for listing in result['maps_listings']:
                        html += f"""
                        <div class="result">
                            <strong>{listing.get('title', 'N/A')}</strong><br>
                            Rating: {listing.get('rating', 'N/A')} 
                            ({listing.get('reviews', 0)} reviews)<br>
                            Phone: {listing.get('phone', 'N/A')}<br>
                            Address: {listing.get('address', 'N/A')}
                        </div>
                        """
                
                # Organic results
                if result.get('organic_results'):
                    html += "<h5>Organic Results:</h5>"
                    for organic in result['organic_results']:
                        html += f"""
                        <div class="result">
                            <strong>{organic.get('title', 'N/A')}</strong><br>
                            Domain: {organic.get('domain', 'N/A')}<br>
                            Position: {organic.get('position', 'N/A')}
                        </div>
                        """
                
                html += "</div>"
            
            html += "</div>"
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def _generate_insights(self, aggregated_data: Dict[str, Any]) -> list:
        """Generate competitive insights from the data."""
        insights = []
        by_group = aggregated_data.get('by_keyword_group', {})
        
        # Analyze maps presence
        total_maps = sum(
            group.get('total_maps_listings', 0) 
            for group in by_group.values()
        )
        
        if total_maps > 0:
            insights.append({
                'title': 'Local Maps Presence',
                'text': f'Found {total_maps} Google Maps listings across all keywords, indicating active local competition.'
            })
        
        # Analyze local services ads
        total_local_services = sum(
            group.get('total_local_services', 0) 
            for group in by_group.values()
        )
        
        if total_local_services > 0:
            insights.append({
                'title': 'Local Services Advertising',
                'text': f'Detected {total_local_services} Local Services Ads, showing competitors are investing in Google\'s premium local advertising.'
            })
        
        # Analyze keyword group performance
        for group_name, group_data in by_group.items():
            success_rate = (group_data.get('successful_searches', 0) / 
                          max(group_data.get('keyword_count', 1), 1)) * 100
            
            if success_rate < 100:
                insights.append({
                    'title': f'{group_name.title()} Keywords Analysis',
                    'text': f'Success rate: {success_rate:.1f}%. Some keywords may need refinement or have limited local competition.'
                })
        
        return insights
    
    def _generate_filename(self, prefix: str) -> str:
        """Generate timestamped filename."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Check if file exists and add suffix if needed
        base_filename = f"{prefix}_{timestamp}.html"
        filename = base_filename
        counter = 1
        
        while (self.output_dir / filename).exists():
            filename = f"{prefix}_{timestamp}_{counter:02d}.html"
            counter += 1
        
        return filename
    
    def generate_summary_report(self, aggregated_data: Dict[str, Any], 
                               business_name: str, location: str) -> Dict[str, Any]:
        """
        Generate a summary report with key metrics.
        
        Args:
            aggregated_data: Processed search results
            business_name: Business name
            location: Location string
            
        Returns:
            Summary report dictionary
        """
        summary = aggregated_data.get('summary', {})
        by_group = aggregated_data.get('by_keyword_group', {})
        
        # Calculate competitive metrics
        total_competitors = set()
        top_domains = {}
        
        for group_data in by_group.values():
            for result in group_data.get('results', []):
                if result.get('error'):
                    continue
                
                # Collect competitor domains from organic results
                for organic in result.get('organic_results', []):
                    domain = organic.get('domain', '')
                    if domain:
                        total_competitors.add(domain)
                        top_domains[domain] = top_domains.get(domain, 0) + 1
        
        # Sort domains by frequency
        top_domains_sorted = sorted(
            top_domains.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        summary_report = {
            'business_name': business_name,
            'location': location,
            'analysis_date': datetime.now().isoformat(),
            'total_keywords': summary.get('total_keywords', 0),
            'successful_searches': summary.get('successful_searches', 0),
            'total_competitors': len(total_competitors),
            'top_competing_domains': top_domains_sorted,
            'keyword_groups': {
                name: {
                    'keyword_count': data.get('keyword_count', 0),
                    'maps_listings': data.get('total_maps_listings', 0),
                    'local_services': data.get('total_local_services', 0),
                    'organic_results': data.get('total_organic_results', 0)
                }
                for name, data in by_group.items()
            }
        }
        
        return summary_report

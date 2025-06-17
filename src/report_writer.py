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
    
    def _generate_insights(self, aggregated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive competitive insights and actionable recommendations."""
        by_group = aggregated_data.get('by_keyword_group', {})
        all_results = aggregated_data.get('all_results', [])

        # Generate different types of insights
        competitive_analysis = self._analyze_competitive_landscape(by_group, all_results)
        seo_recommendations = self._generate_seo_recommendations(by_group, all_results)
        gmb_recommendations = self._generate_gmb_recommendations(by_group, all_results)
        business_insights = self._generate_business_insights(by_group, all_results)

        return {
            'competitive_analysis': competitive_analysis,
            'seo_recommendations': seo_recommendations,
            'gmb_recommendations': gmb_recommendations,
            'business_insights': business_insights
        }

    def _analyze_competitive_landscape(self, by_group: Dict[str, Any], all_results: list) -> Dict[str, Any]:
        """Analyze the competitive landscape and identify key competitors."""
        # Collect all competitors from Maps and Organic results
        maps_competitors = {}
        organic_competitors = {}

        for result in all_results:
            if result.get('error'):
                continue

            # Analyze Maps listings
            for maps_listing in result.get('maps_listings', []):
                name = maps_listing.get('title', '')
                if name:
                    if name not in maps_competitors:
                        maps_competitors[name] = {
                            'name': name,
                            'appearances': 0,
                            'avg_rating': 0,
                            'total_reviews': 0,
                            'phone': maps_listing.get('phone', ''),
                            'keywords': []
                        }
                    maps_competitors[name]['appearances'] += 1
                    maps_competitors[name]['keywords'].append(result.get('keyword', ''))
                    if maps_listing.get('rating'):
                        maps_competitors[name]['avg_rating'] = maps_listing.get('rating', 0)
                        maps_competitors[name]['total_reviews'] = maps_listing.get('reviews', 0)

            # Analyze Organic results
            for organic in result.get('organic_results', []):
                domain = organic.get('domain', '')
                if domain:
                    if domain not in organic_competitors:
                        organic_competitors[domain] = {
                            'domain': domain,
                            'appearances': 0,
                            'keywords': [],
                            'avg_position': 0,
                            'positions': []
                        }
                    organic_competitors[domain]['appearances'] += 1
                    organic_competitors[domain]['keywords'].append(result.get('keyword', ''))
                    organic_competitors[domain]['positions'].append(organic.get('position', 0))

        # Calculate average positions
        for competitor in organic_competitors.values():
            if competitor['positions']:
                competitor['avg_position'] = sum(competitor['positions']) / len(competitor['positions'])

        # Sort competitors by appearances
        top_maps_competitors = sorted(
            maps_competitors.values(),
            key=lambda x: x['appearances'],
            reverse=True
        )[:5]

        top_organic_competitors = sorted(
            organic_competitors.values(),
            key=lambda x: x['appearances'],
            reverse=True
        )[:5]

        return {
            'total_maps_competitors': len(maps_competitors),
            'total_organic_competitors': len(organic_competitors),
            'top_maps_competitors': top_maps_competitors,
            'top_organic_competitors': top_organic_competitors,
            'market_analysis': self._generate_market_analysis(maps_competitors, organic_competitors)
        }

    def _generate_seo_recommendations(self, by_group: Dict[str, Any], all_results: list) -> Dict[str, Any]:
        """Generate specific SEO action items based on competitive analysis."""
        # Extract location from first result
        location = ""
        business_name = ""
        if all_results:
            # Try to extract location from search metadata or infer from keywords
            for result in all_results:
                keyword = result.get('keyword', '')
                if 'Spokane' in keyword:
                    location = "Spokane, WA"
                    break
                elif 'Seattle' in keyword:
                    location = "Seattle, WA"
                    break

        # Analyze competitor titles and meta descriptions
        competitor_titles = []
        competitor_domains = []
        common_keywords = []

        for result in all_results:
            if result.get('error'):
                continue

            keyword = result.get('keyword', '')
            common_keywords.append(keyword)

            for organic in result.get('organic_results', []):
                title = organic.get('title', '')
                domain = organic.get('domain', '')
                if title:
                    competitor_titles.append(title)
                if domain:
                    competitor_domains.append(domain)

        # Generate specific recommendations
        recommendations = {
            'immediate_fixes': self._generate_immediate_seo_fixes(location, common_keywords),
            'title_tag_suggestions': self._generate_title_suggestions(location, common_keywords, competitor_titles),
            'meta_description_suggestions': self._generate_meta_suggestions(location, common_keywords),
            'content_optimization': self._generate_content_recommendations(location, common_keywords),
            'technical_seo': self._generate_technical_recommendations()
        }

        return recommendations

    def _generate_immediate_seo_fixes(self, location: str, keywords: list) -> list:
        """Generate immediate SEO fixes within 7 days."""
        city = location.split(',')[0] if location else "your city"
        primary_service = self._extract_primary_service(keywords)

        fixes = [
            {
                'priority': 'HIGH',
                'task': 'Add Meta Description to Homepage',
                'description': f'Write a compelling 150-160 character summary including "{city}", "{primary_service}", and key services.',
                'example': f'"{city}\'s trusted {primary_service} pros for installation, repairs, and maintenance. Serving residential & commercial clients with guaranteed results."',
                'timeframe': '1-2 hours'
            },
            {
                'priority': 'HIGH',
                'task': 'Update Title Tag',
                'description': f'Change homepage title to include location and primary service.',
                'example': f'Your Business Name | {primary_service} & Repair Services {city}',
                'timeframe': '30 minutes'
            },
            {
                'priority': 'MEDIUM',
                'task': 'Add Missing Keywords to Main Page Copy',
                'description': f'Inject geo-targeted keywords naturally into body content.',
                'example': f'Include phrases like "{primary_service} {city}", "local {primary_service} contractor", "{city} {primary_service} installation"',
                'timeframe': '2-3 hours'
            },
            {
                'priority': 'MEDIUM',
                'task': 'Optimize Image Alt Tags',
                'description': 'Add keyword-rich alt tags to every image on homepage and service pages.',
                'example': f'Alt text: "{primary_service} installation project in {city}" instead of "IMG_001.jpg"',
                'timeframe': '1-2 hours'
            },
            {
                'priority': 'HIGH',
                'task': 'Update Header Tag Structure (H1-H3)',
                'description': f'Make H1 more specific and add service-focused H2/H3 tags.',
                'example': f'H1: "{primary_service} Experts in {city}" | H2: "Professional Installation Services" | H3: "Emergency Repair & Maintenance"',
                'timeframe': '1 hour'
            }
        ]

        return fixes

    def _extract_primary_service(self, keywords: list) -> str:
        """Extract the primary service from keywords."""
        # Common service patterns
        service_patterns = {
            'sprinkler': 'sprinkler system',
            'irrigation': 'irrigation',
            'plumbing': 'plumbing',
            'hvac': 'HVAC',
            'landscaping': 'landscaping',
            'roofing': 'roofing',
            'electrical': 'electrical',
            'pest control': 'pest control',
            'cleaning': 'cleaning'
        }

        for keyword in keywords:
            keyword_lower = keyword.lower()
            for pattern, service in service_patterns.items():
                if pattern in keyword_lower:
                    return service

        return 'professional services'

    def _generate_title_suggestions(self, location: str, keywords: list, competitor_titles: list) -> list:
        """Generate title tag suggestions based on competitive analysis."""
        city = location.split(',')[0] if location else "Your City"
        primary_service = self._extract_primary_service(keywords)

        suggestions = [
            f'Your Business Name | {primary_service.title()} Installation & Repair {city}',
            f'{primary_service.title()} Contractors {city} | Professional Installation & Service',
            f'Best {primary_service.title()} Company {city} | Licensed & Insured Professionals',
            f'{city} {primary_service.title()} Experts | Installation, Repair & Maintenance'
        ]

        return suggestions

    def _generate_meta_suggestions(self, location: str, keywords: list) -> list:
        """Generate meta description suggestions."""
        city = location.split(',')[0] if location else "your area"
        primary_service = self._extract_primary_service(keywords)

        suggestions = [
            f'Professional {primary_service} installation, repair, and maintenance in {city}. Licensed contractors with guaranteed work and competitive pricing. Call today!',
            f'{city}\'s trusted {primary_service} experts. Quality installation, fast repairs, and reliable service for residential & commercial clients. Free estimates available.',
            f'Expert {primary_service} services in {city}. From new installations to emergency repairs, we deliver quality results with satisfaction guaranteed.'
        ]

        return suggestions

    def _generate_content_recommendations(self, location: str, keywords: list) -> Dict[str, Any]:
        """Generate content optimization recommendations."""
        city = location.split(',')[0] if location else "your city"
        primary_service = self._extract_primary_service(keywords)

        return {
            'header_structure': {
                'h1': f'{primary_service.title()} Experts in {city}',
                'h2_suggestions': [
                    f'Professional {primary_service.title()} Installation',
                    f'{primary_service.title()} Repair & Maintenance',
                    f'Emergency {primary_service.title()} Services',
                    f'Serving {city} & Surrounding Areas'
                ]
            },
            'geo_targeted_keywords': [
                f'{primary_service} {city}',
                f'{primary_service} installation {city}',
                f'{primary_service} repair {city}',
                f'local {primary_service} contractor',
                f'{city} {primary_service} company'
            ],
            'content_sections': [
                f'Why Choose Our {primary_service.title()} Services in {city}',
                f'{primary_service.title()} Installation Process',
                f'Maintenance & Repair Services',
                f'Service Areas in {city}'
            ]
        }

    def _generate_technical_recommendations(self) -> list:
        """Generate technical SEO recommendations."""
        return [
            {
                'category': 'Page Speed',
                'recommendation': 'Optimize images and enable compression',
                'impact': 'HIGH',
                'effort': 'MEDIUM'
            },
            {
                'category': 'Mobile Optimization',
                'recommendation': 'Ensure responsive design and mobile-friendly navigation',
                'impact': 'HIGH',
                'effort': 'LOW'
            },
            {
                'category': 'Schema Markup',
                'recommendation': 'Add LocalBusiness and Service schema markup',
                'impact': 'MEDIUM',
                'effort': 'HIGH'
            },
            {
                'category': 'Internal Linking',
                'recommendation': 'Create service-specific landing pages with internal links',
                'impact': 'MEDIUM',
                'effort': 'MEDIUM'
            }
        ]

    def _generate_gmb_recommendations(self, by_group: Dict[str, Any], all_results: list) -> Dict[str, Any]:
        """Generate Google My Business optimization recommendations."""
        # Analyze competitor GMB profiles
        competitor_ratings = []
        competitor_review_counts = []

        for result in all_results:
            for maps_listing in result.get('maps_listings', []):
                rating = maps_listing.get('rating')
                reviews = maps_listing.get('reviews')
                if rating:
                    competitor_ratings.append(rating)
                if reviews:
                    competitor_review_counts.append(reviews)

        avg_competitor_rating = sum(competitor_ratings) / len(competitor_ratings) if competitor_ratings else 0
        avg_competitor_reviews = sum(competitor_review_counts) / len(competitor_review_counts) if competitor_review_counts else 0

        location = self._extract_location_from_results(all_results)
        primary_service = self._extract_primary_service([r.get('keyword', '') for r in all_results])

        return {
            'competitive_benchmarks': {
                'average_rating': round(avg_competitor_rating, 1),
                'average_reviews': int(avg_competitor_reviews),
                'top_rated_competitor': max(competitor_ratings) if competitor_ratings else 0
            },
            'posting_strategy': [
                {
                    'frequency': 'Weekly',
                    'type': 'Offer Posts',
                    'example': f'Get a FREE {primary_service} inspection with any service call this month – a $150+ value!',
                    'cta': 'Call now to schedule'
                },
                {
                    'frequency': 'Bi-weekly',
                    'type': 'Service Highlights',
                    'example': f'Professional {primary_service} installation with 100% satisfaction guarantee',
                    'cta': 'Book your consultation'
                },
                {
                    'frequency': 'Monthly',
                    'type': 'Educational Content',
                    'example': f'5 Signs You Need {primary_service} Repair in {location}',
                    'cta': 'Learn more on our website'
                }
            ],
            'photo_strategy': [
                'Upload job-site photos weekly',
                f'Geo-tag photos with {location} neighborhoods',
                'Show before/after project results',
                'Include team photos and equipment'
            ],
            'review_strategy': [
                'Respond to all reviews within 24 hours',
                'Ask satisfied customers for reviews via email/text',
                'Address negative reviews professionally',
                f'Target {int(avg_competitor_reviews * 1.2)} total reviews to exceed competition'
            ]
        }

    def _generate_business_insights(self, by_group: Dict[str, Any], all_results: list) -> Dict[str, Any]:
        """Generate business development insights in layman terms."""
        location = self._extract_location_from_results(all_results)
        primary_service = self._extract_primary_service([r.get('keyword', '') for r in all_results])

        # Count total competitors
        total_maps_competitors = len(set(
            listing.get('title', '')
            for result in all_results
            for listing in result.get('maps_listings', [])
            if listing.get('title')
        ))

        total_organic_competitors = len(set(
            organic.get('domain', '')
            for result in all_results
            for organic in result.get('organic_results', [])
            if organic.get('domain')
        ))

        return {
            'market_overview': {
                'competition_level': self._assess_competition_level(total_maps_competitors, total_organic_competitors),
                'market_opportunity': self._assess_market_opportunity(all_results),
                'key_findings': self._generate_key_findings(all_results, location, primary_service)
            },
            'layman_explanation': {
                'why_not_showing_up': [
                    f'Your website isn\'t using the words people actually search for (like "{primary_service} {location}")',
                    'You\'re not active on your Google Business profile with regular posts and updates',
                    f'Google can\'t tell you\'re the best {primary_service} option in {location}',
                    'Your competitors are more visible because they\'re doing basic SEO you\'re missing'
                ],
                'whats_getting_fixed': [
                    f'Your website will start using the exact words people search for in {location}',
                    'You\'ll have compelling offers posted to your Google Business profile',
                    f'You\'ll show up when people in {location} search for {primary_service} help',
                    'Your business will look more professional and trustworthy online'
                ]
            },
            'next_steps': [
                {
                    'priority': 1,
                    'action': 'Fix Your Website Basics',
                    'description': 'Update title tags, meta descriptions, and add location-specific keywords',
                    'timeline': '1-2 weeks',
                    'impact': 'HIGH'
                },
                {
                    'priority': 2,
                    'action': 'Activate Google My Business',
                    'description': 'Start posting weekly offers and uploading job photos',
                    'timeline': 'Ongoing weekly',
                    'impact': 'HIGH'
                },
                {
                    'priority': 3,
                    'action': 'Build Review Strategy',
                    'description': 'Systematically collect customer reviews to match competition',
                    'timeline': '2-3 months',
                    'impact': 'MEDIUM'
                }
            ]
        }

    def _extract_location_from_results(self, all_results: list) -> str:
        """Extract location from search results."""
        for result in all_results:
            keyword = result.get('keyword', '')
            if 'Spokane' in keyword:
                return 'Spokane'
            elif 'Seattle' in keyword:
                return 'Seattle'
            elif 'Portland' in keyword:
                return 'Portland'
        return 'your city'

    def _assess_competition_level(self, maps_count: int, organic_count: int) -> str:
        """Assess the level of competition."""
        total_competitors = maps_count + organic_count
        if total_competitors > 50:
            return 'HIGH - Very competitive market with many established players'
        elif total_competitors > 25:
            return 'MEDIUM - Moderate competition with room for growth'
        else:
            return 'LOW - Limited competition, good opportunity for market entry'

    def _assess_market_opportunity(self, all_results: list) -> str:
        """Assess market opportunity based on search results."""
        total_searches = len([r for r in all_results if not r.get('error')])
        if total_searches > 10:
            return 'STRONG - High search volume indicates strong market demand'
        elif total_searches > 5:
            return 'MODERATE - Decent search activity with growth potential'
        else:
            return 'LIMITED - Lower search volume, may need broader keyword strategy'

    def _generate_key_findings(self, all_results: list, location: str, primary_service: str) -> list:
        """Generate key findings from the analysis."""
        findings = []

        # Count successful vs failed searches
        successful = len([r for r in all_results if not r.get('error')])
        total = len(all_results)

        if successful < total:
            findings.append(f'{total - successful} keywords had no results - opportunity for first-mover advantage')

        # Analyze Maps presence
        maps_listings = [listing for result in all_results for listing in result.get('maps_listings', [])]
        if maps_listings:
            avg_rating = sum(l.get('rating', 0) for l in maps_listings if l.get('rating')) / len([l for l in maps_listings if l.get('rating')])
            findings.append(f'Competitors average {avg_rating:.1f} stars - quality service is expected in this market')

        # Analyze organic competition
        organic_results = [org for result in all_results for org in result.get('organic_results', [])]
        if organic_results:
            findings.append(f'{len(organic_results)} organic competitors found - SEO investment is necessary')

        findings.append(f'Local search is active for {primary_service} services in {location}')

        return findings

    def _generate_market_analysis(self, maps_competitors: dict, organic_competitors: dict) -> Dict[str, Any]:
        """Generate market analysis insights."""
        return {
            'market_saturation': 'MODERATE' if len(maps_competitors) < 20 else 'HIGH',
            'opportunity_score': min(100, max(0, 100 - (len(maps_competitors) * 3))),
            'recommended_strategy': 'Focus on local SEO and Google My Business optimization' if len(maps_competitors) < 15 else 'Differentiate through specialized services and superior customer experience'
        }
    
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

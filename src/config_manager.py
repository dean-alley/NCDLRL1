"""
Configuration Manager for LocalRankLens

Handles loading, validation, and management of configuration files
and environment variables.
"""

import json
import os
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from dotenv import load_dotenv


class ConfigurationError(Exception):
    """Custom exception for configuration-related errors."""
    pass


class ConfigManager:
    """Manages configuration loading and validation for LocalRankLens."""
    
    def __init__(self, config_path: str = "config.json", env_path: str = ".env"):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the JSON configuration file
            env_path: Path to the environment variables file
        """
        self.config_path = Path(config_path)
        self.env_path = Path(env_path)
        self.config: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)
        
        # Load environment variables
        self._load_environment()
        
        # Load and validate configuration
        self._load_config()
        self._validate_config()
    
    def _load_environment(self) -> None:
        """Load environment variables from .env file."""
        if self.env_path.exists():
            load_dotenv(self.env_path)
            self.logger.info(f"Loaded environment variables from {self.env_path}")
        else:
            self.logger.warning(f"Environment file {self.env_path} not found")
    
    def _load_config(self) -> None:
        """Load configuration from JSON file."""
        if not self.config_path.exists():
            raise ConfigurationError(f"Configuration file {self.config_path} not found")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            self.logger.info(f"Loaded configuration from {self.config_path}")
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in {self.config_path}: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error loading {self.config_path}: {e}")
    
    def _validate_config(self) -> None:
        """Validate the loaded configuration."""
        required_fields = [
            'business_name',
            'location',
            'keywords',
            'output_prefix'
        ]
        
        # Check required top-level fields
        for field in required_fields:
            if field not in self.config:
                raise ConfigurationError(f"Missing required field: {field}")
        
        # Validate location structure
        location = self.config.get('location', {})
        if not isinstance(location, dict):
            raise ConfigurationError("'location' must be an object")
        
        for loc_field in ['city', 'state']:
            if loc_field not in location:
                raise ConfigurationError(f"Missing required location field: {loc_field}")
            if not isinstance(location[loc_field], str) or not location[loc_field].strip():
                raise ConfigurationError(f"Location field '{loc_field}' must be a non-empty string")
        
        # Validate keywords structure
        keywords = self.config.get('keywords', {})
        if not isinstance(keywords, dict):
            raise ConfigurationError("'keywords' must be an object")
        
        if not keywords:
            raise ConfigurationError("At least one keyword group must be defined")
        
        for group_name, keyword_list in keywords.items():
            if not isinstance(keyword_list, list):
                raise ConfigurationError(f"Keyword group '{group_name}' must be a list")
            if not keyword_list:
                raise ConfigurationError(f"Keyword group '{group_name}' cannot be empty")
            for keyword in keyword_list:
                if not isinstance(keyword, str) or not keyword.strip():
                    raise ConfigurationError(f"All keywords in '{group_name}' must be non-empty strings")
        
        # Validate business name and output prefix
        if not isinstance(self.config['business_name'], str) or not self.config['business_name'].strip():
            raise ConfigurationError("'business_name' must be a non-empty string")
        
        if not isinstance(self.config['output_prefix'], str) or not self.config['output_prefix'].strip():
            raise ConfigurationError("'output_prefix' must be a non-empty string")
        
        self.logger.info("Configuration validation passed")
    
    def get_serpapi_key(self) -> str:
        """Get the SerpAPI key from environment variables."""
        api_key = os.getenv('SERPAPI_KEY')
        if not api_key:
            raise ConfigurationError(
                "SERPAPI_KEY not found in environment variables. "
                "Please set it in your .env file or environment."
            )
        return api_key
    
    def get_business_name(self) -> str:
        """Get the business name from configuration."""
        return self.config['business_name']
    
    def get_location(self) -> Dict[str, str]:
        """Get the location information."""
        return self.config['location']
    
    def get_location_string(self) -> str:
        """Get location as a formatted string for search queries."""
        location = self.get_location()
        return f"{location['city']}, {location['state']}"
    
    def get_keywords(self) -> Dict[str, List[str]]:
        """Get all keyword groups."""
        return self.config['keywords']
    
    def get_keyword_groups(self) -> List[str]:
        """Get list of keyword group names."""
        return list(self.config['keywords'].keys())
    
    def get_keywords_for_group(self, group_name: str) -> List[str]:
        """Get keywords for a specific group."""
        keywords = self.config['keywords']
        if group_name not in keywords:
            raise ConfigurationError(f"Keyword group '{group_name}' not found")
        return keywords[group_name]
    
    def get_all_keywords_flat(self) -> List[str]:
        """Get all keywords as a flat list."""
        all_keywords = []
        for keyword_list in self.config['keywords'].values():
            all_keywords.extend(keyword_list)
        return all_keywords
    
    def get_output_prefix(self) -> str:
        """Get the output filename prefix."""
        return self.config['output_prefix']
    
    def get_report_settings(self) -> Dict[str, Any]:
        """Get report settings with defaults."""
        default_settings = {
            'include_maps_listings': True,
            'include_local_services': True,
            'include_organic_results': True,
            'max_maps_results': 3,
            'max_organic_results': 5
        }
        
        user_settings = self.config.get('report_settings', {})
        default_settings.update(user_settings)
        return default_settings
    
    def get_output_dir(self) -> Path:
        """Get the output directory path."""
        output_dir = Path(os.getenv('OUTPUT_DIR', 'output'))
        output_dir.mkdir(exist_ok=True)
        return output_dir
    
    def get_log_level(self) -> str:
        """Get the logging level from environment."""
        return os.getenv('LOG_LEVEL', 'INFO').upper()


def setup_logging(config_manager: ConfigManager) -> None:
    """Set up logging configuration."""
    log_level = getattr(logging, config_manager.get_log_level(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

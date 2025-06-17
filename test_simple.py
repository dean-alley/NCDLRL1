#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '.')

from src.config_manager import ConfigManager

def test_config_loading():
    """Simple test to verify config loading works."""
    try:
        # Test with the actual config.json file
        config_manager = ConfigManager('config.json')
        
        print("✓ Configuration loaded successfully")
        print(f"Business name: {config_manager.get_business_name()}")
        print(f"Location: {config_manager.get_location_string()}")
        print(f"Keyword groups: {config_manager.get_keyword_groups()}")
        print(f"Output prefix: {config_manager.get_output_prefix()}")
        
        # Test report settings
        settings = config_manager.get_report_settings()
        print(f"Report settings: {settings}")
        
        print("\n✓ All basic functionality working!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_config_loading()
    sys.exit(0 if success else 1)

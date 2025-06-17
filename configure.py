#!/usr/bin/env python3
"""
LocalRankLens Configuration Helper

Simple script to update business configuration for LocalRankLens analysis.
"""

import json
import sys
from pathlib import Path

def load_config():
    """Load current configuration."""
    config_path = Path("config.json")
    if not config_path.exists():
        print("❌ config.json not found!")
        return None
    
    with open(config_path, 'r') as f:
        return json.load(f)

def save_config(config):
    """Save configuration to file."""
    with open("config.json", 'w') as f:
        json.dump(config, f, indent=2)
    print("✅ Configuration saved!")

def main():
    print("🔧 LocalRankLens Configuration Helper")
    print("=" * 50)
    
    config = load_config()
    if not config:
        return 1
    
    print(f"Current Business: {config['business_name']}")
    print(f"Current Location: {config['location']['city']}, {config['location']['state']}")
    print()
    
    # Ask if user wants to change business details
    change = input("Change business details? (y/n): ").lower()
    if change == 'y':
        business_name = input(f"Business Name [{config['business_name']}]: ").strip()
        if business_name:
            config['business_name'] = business_name
            # Update output prefix
            config['output_prefix'] = business_name.lower().replace(' ', '-').replace('&', 'and')
        
        city = input(f"City [{config['location']['city']}]: ").strip()
        if city:
            config['location']['city'] = city
        
        state = input(f"State [{config['location']['state']}]: ").strip()
        if state:
            config['location']['state'] = state
        
        save_config(config)
    
    print()
    print("📊 Current Keyword Groups:")
    for group, keywords in config['keywords'].items():
        print(f"  {group.title()}: {len(keywords)} keywords")
    
    print()
    print("🚀 Ready to run LocalRankLens!")
    print("   Run: python run_localranklens.py")
    print("   Or:  ./run.bat")
    print("   Or:  ./run.ps1")

if __name__ == "__main__":
    sys.exit(main())

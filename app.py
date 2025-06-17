#!/usr/bin/env python3
"""
LocalRankLens Flask Web API

Flask wrapper for LocalRankLens to run on Heroku.
"""

import os
import sys
import json
import tempfile
import logging
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# Add src directory to Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from localranklens import LocalRankLens

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'LocalRankLens API',
        'version': '1.0.0'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Analyze local search competition.
    
    Expected JSON payload:
    {
        "business_name": "Business Name",
        "location": {
            "city": "City",
            "state": "State"
        },
        "keywords": "keyword1\nkeyword2\nkeyword3"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('business_name') or not data.get('location') or not data.get('keywords'):
            return jsonify({'error': 'Missing required fields: business_name, location, or keywords'}), 400
        
        # Process keywords - convert from textarea string to structured format
        keyword_lines = [line.strip() for line in data['keywords'].split('\n') if line.strip()]
        
        if not keyword_lines:
            return jsonify({'error': 'No valid keywords provided'}), 400
        
        # Create structured config for LocalRankLens
        config = {
            "business_name": data['business_name'],
            "location": {
                "city": data['location']['city'],
                "state": data['location']['state']
            },
            "keywords": {
                "core": keyword_lines[:max(1, len(keyword_lines) * 6 // 10)],  # 60% as core
                "upsell": keyword_lines[len(keyword_lines) * 6 // 10:len(keyword_lines) * 8 // 10],  # 20% as upsell
                "efficiency": keyword_lines[len(keyword_lines) * 8 // 10:len(keyword_lines) * 9 // 10],  # 10% as efficiency
                "emergency": keyword_lines[len(keyword_lines) * 9 // 10:]  # 10% as emergency
            },
            "output_prefix": data['business_name'].lower().replace(' ', '-').replace('&', 'and')
        }
        
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_config:
            json.dump(config, temp_config, indent=2)
            temp_config_path = temp_config.name
        
        try:
            # Run LocalRankLens analysis
            logger.info(f"Starting analysis for {config['business_name']}")
            lrl = LocalRankLens(config_path=temp_config_path)
            report_path = lrl.run_analysis()

            logger.info(f"Analysis complete. Report saved to: {report_path}")

            # Clean up temp config file
            os.unlink(temp_config_path)

            # Return PDF file for download
            pdf_filename = f"{config['business_name'].lower().replace(' ', '-')}_report.pdf"
            return send_file(
                report_path,
                as_attachment=True,
                download_name=pdf_filename,
                mimetype='application/pdf'
            )
            
        except Exception as e:
            # Clean up temp config file on error
            if os.path.exists(temp_config_path):
                os.unlink(temp_config_path)
            raise e
            
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/config', methods=['POST'])
def generate_config():
    """
    Generate a config file for local use.
    
    Same payload as /api/analyze but returns JSON config instead of running analysis.
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('business_name') or not data.get('location') or not data.get('keywords'):
            return jsonify({'error': 'Missing required fields: business_name, location, or keywords'}), 400
        
        # Process keywords
        keyword_lines = [line.strip() for line in data['keywords'].split('\n') if line.strip()]
        
        if not keyword_lines:
            return jsonify({'error': 'No valid keywords provided'}), 400
        
        # Create structured config
        config = {
            "business_name": data['business_name'],
            "location": {
                "city": data['location']['city'],
                "state": data['location']['state']
            },
            "keywords": {
                "core": keyword_lines[:max(1, len(keyword_lines) * 6 // 10)],
                "upsell": keyword_lines[len(keyword_lines) * 6 // 10:len(keyword_lines) * 8 // 10],
                "efficiency": keyword_lines[len(keyword_lines) * 8 // 10:len(keyword_lines) * 9 // 10],
                "emergency": keyword_lines[len(keyword_lines) * 9 // 10:]
            },
            "output_prefix": data['business_name'].lower().replace(' ', '-').replace('&', 'and')
        }
        
        return jsonify(config)
        
    except Exception as e:
        logger.error(f"Config generation failed: {str(e)}")
        return jsonify({'error': f'Config generation failed: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

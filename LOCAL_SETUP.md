# LocalRankLens - Local Setup Guide

## 🚀 Quick Start

### Option 1: Double-click to run
- **Windows**: Double-click `run.bat`
- **PowerShell**: Right-click `run.ps1` → "Run with PowerShell"

### Option 2: Command line
```bash
python run_localranklens.py
```

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Required packages** (install with):
   ```bash
   pip install -r requirements.txt
   ```
3. **SerpAPI Key** (already configured in `.env`)

## ⚙️ Configuration

### Quick Configuration
```bash
python configure.py
```

### Manual Configuration
Edit `config.json`:
```json
{
  "business_name": "Your Business Name",
  "location": {
    "city": "Your City",
    "state": "Your State"
  },
  "keywords": {
    "core": ["keyword 1", "keyword 2"],
    "upsell": ["upsell keyword 1"],
    "efficiency": ["efficiency keyword 1"],
    "emergency": ["emergency keyword 1"]
  }
}
```

## 📊 What You Get

The enhanced LocalRankLens generates comprehensive reports with:

- **🏆 Competitive Landscape Analysis**
  - Market opportunity scoring
  - Top Maps & Organic competitors
  - Strategic recommendations

- **🚀 SEO Action Plan**
  - 7-day immediate fixes with examples
  - Title tag & meta description suggestions
  - Content optimization recommendations
  - Technical SEO checklist

- **📍 Google My Business Strategy**
  - Competitive benchmarking
  - Weekly posting strategies with dollar offers
  - Photo & review strategies

- **💼 Business Development Insights**
  - Plain English explanations for clients
  - Prioritized next steps with timelines
  - Market analysis and opportunities

## 📁 Output

Reports are saved to the `output/` folder as HTML files:
- Format: `business-name_YYYYMMDD_HHMMSS.html`
- Open in any web browser
- Professional styling for client presentations

## 🔧 Troubleshooting

### Common Issues:
1. **"Module not found"** → Run `pip install -r requirements.txt`
2. **"API key invalid"** → Check `.env` file has correct SerpAPI key
3. **"No results"** → Check internet connection and keyword spelling

### Support:
- Check logs in console output
- Verify configuration in `config.json`
- Ensure all dependencies are installed

## 🎯 Tips for Best Results

1. **Keywords**: Use location-specific terms
2. **Business Name**: Keep it consistent with your actual business
3. **Location**: Use city, state format for best results
4. **Review Reports**: Check competitor analysis for strategic insights

---

**Ready to analyze your local search competition!** 🚀

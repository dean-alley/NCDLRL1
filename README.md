# LocalRankLens

A competitive intelligence tool for digital marketing consultants and agencies. LocalRankLens simulates local search engine results for target cities and keyword sets, providing actionable insights for sales pitches, SEO strategy, and paid media planning.

## 🌐 Live Deployment

- **Frontend**: [lrl.northcurrent.digital](https://lrl.northcurrent.digital)
- **Backend API**: Deployed on Heroku
- **Status**: Production Ready ✅

## Features

- **Local Search Simulation**: Query Google search results for specific cities and keywords
- **Competitive Intelligence**: Extract top Google Maps listings, Local Services Ads, and organic results
- **Professional PDF Reports**: Generate client-ready PDF reports with actionable SEO recommendations
- **Web Interface**: Modern React/Next.js frontend with dark mode design
- **REST API**: Flask-based backend API for programmatic access
- **Flexible Configuration**: JSON-based configuration for easy customization
- **Error Handling**: Robust error handling and retry logic for API calls
- **Auto-Suggestions**: Smart keyword suggestions based on business type and location

## Quick Start

### Prerequisites

- Python 3.10 or higher
- SerpAPI account and API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd NCDLRL1
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.template .env
# Edit .env and add your SERPAPI_KEY
```

5. Configure your search parameters:
```bash
# Edit config.json with your business details and keywords
```

### Usage

```bash
python src/localranklens.py
```

Reports will be generated in the `output/` directory.

## Configuration

Edit `config.json` to customize:

- **business_name**: Your client's business name
- **location**: Target city and state
- **keywords**: Organized by category (core, upsell, emergency)
- **output_prefix**: Filename prefix for reports
- **report_settings**: Control what data to include in reports

## 📁 Project Structure

```
NCDLRL1/
├── 🎨 Frontend (Next.js/React)
│   └── localranklens-frontend/
│       ├── src/app/
│       │   ├── page.tsx              # Main UI form component
│       │   ├── layout.tsx            # App layout and metadata
│       │   ├── globals.css           # TailwindCSS styling
│       │   └── api/                  # API route handlers
│       ├── package.json              # Node.js dependencies
│       ├── tailwind.config.js        # TailwindCSS configuration
│       ├── next.config.ts            # Next.js configuration
│       └── vercel.json              # Vercel deployment config
│
├── 🔧 Backend (Python/Flask)
│   ├── app.py                       # Flask API server
│   ├── src/
│   │   ├── localranklens.py         # Main analysis engine
│   │   ├── config_manager.py        # Configuration handling
│   │   ├── search_scraper.py        # SerpAPI integration
│   │   ├── data_processor.py        # Data extraction and processing
│   │   └── report_writer.py         # PDF report generation
│   ├── requirements.txt             # Python dependencies
│   ├── runtime.txt                  # Python version for Heroku
│   └── Procfile                     # Heroku deployment config
│
├── 📊 Configuration & Data
│   ├── config.json                  # Main configuration file
│   ├── templates/                   # HTML templates
│   ├── output/                      # Generated reports
│   └── docs/                        # Documentation
│
├── 🧪 Testing & Scripts
│   ├── tests/                       # Test suite
│   ├── test_*.py                    # Individual test files
│   ├── run.bat                      # Windows run script
│   └── run.ps1                      # PowerShell run script
│
└── 📚 Documentation
    ├── README.md                    # This file
    ├── DEPLOYMENT.md                # Deployment instructions
    ├── LOCAL_SETUP.md               # Local development setup
    └── *.rtf                        # Business requirements docs
```

## 🔗 Integration Guide for Developers

LocalRankLens offers three integration approaches depending on your needs:

### Option 1: Link Integration (Recommended for WordPress)

**Best for**: WordPress sites, quick integration, zero maintenance

```html
<!-- Simple button integration -->
<a href="https://lrl.northcurrent.digital" target="_blank" class="lrl-button">
  Local Rank Lens Tool
</a>

<!-- Styled button with CSS -->
<style>
.lrl-button {
  background-color: #0073aa;
  color: white;
  padding: 12px 24px;
  text-decoration: none;
  border-radius: 4px;
  display: inline-block;
  font-weight: bold;
  transition: background-color 0.3s;
}
.lrl-button:hover {
  background-color: #005a87;
}
</style>
```

**Benefits:**
- ✅ Zero maintenance - auto-updates
- ✅ No hosting costs
- ✅ Professional separation
- ✅ Always latest version

### Option 2: Frontend Code Integration

**Best for**: Custom React/Next.js sites, branded integration

1. **Copy the frontend code:**
```bash
cp -r localranklens-frontend/src/app/* your-nextjs-app/src/app/lrl/
```

2. **Install dependencies:**
```bash
npm install @tailwindcss/forms lucide-react
```

3. **Configure API endpoint:**
```typescript
// Update API calls to point to your backend
const API_BASE = 'https://your-backend-url.herokuapp.com';
```

4. **Add route to your site:**
```
your-site.com/lrl → LocalRankLens tool
```

### Option 3: Full Code Integration

**Best for**: Complete control, custom modifications, enterprise deployment

1. **Clone the entire repository**
2. **Set up both frontend and backend**
3. **Deploy to your infrastructure**
4. **Customize branding and features**

## 🚀 Technical Setup Instructions

### Backend Setup (Python/Flask)

#### Prerequisites
- Python 3.10 or higher
- SerpAPI account and API key

#### Local Development
```bash
# 1. Clone and navigate
git clone <repository-url>
cd NCDLRL1

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
export SERPAPI_KEY="your_serpapi_key_here"
export FLASK_ENV="development"

# 5. Run the Flask server
python app.py
```

#### Production Deployment (Heroku)
```bash
# 1. Install Heroku CLI
# 2. Login and create app
heroku login
heroku create your-app-name

# 3. Set environment variables
heroku config:set SERPAPI_KEY="your_serpapi_key_here"

# 4. Deploy
git push heroku main
```

### Frontend Setup (Next.js/React)

#### Prerequisites
- Node.js 18+ and npm

#### Local Development
```bash
# 1. Navigate to frontend directory
cd localranklens-frontend

# 2. Install dependencies
npm install

# 3. Set environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:5000" > .env.local

# 4. Run development server
npm run dev
```

#### Production Deployment (Vercel)
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
vercel --prod

# 3. Set environment variables in Vercel dashboard
NEXT_PUBLIC_API_URL=https://your-backend-url.herokuapp.com
```

## 🔌 API Documentation

### Base URL
- **Production**: `https://your-backend-url.herokuapp.com`
- **Development**: `http://localhost:5000`

### Endpoints

#### POST /api/analyze
Generate a LocalRankLens analysis report.

**Request Body:**
```json
{
  "business_name": "Revive Irrigation",
  "location": "Spokane, WA",
  "keywords": {
    "core": ["irrigation repair", "sprinkler installation"],
    "upsell": ["smart irrigation", "drip systems"],
    "emergency": ["broken sprinkler", "irrigation emergency"]
  },
  "report_settings": {
    "include_maps": true,
    "include_ads": true,
    "include_organic": true,
    "include_recommendations": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "report_url": "/download/report_20241220_123456.pdf",
  "analysis_summary": {
    "total_keywords": 6,
    "competitors_found": 15,
    "opportunities": 8
  }
}
```

#### GET /download/{filename}
Download generated PDF report.

**Response:** PDF file download

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-12-20T12:34:56Z"
}
```

## 🏗️ System Architecture

### Data Flow Overview
```
User Input (Frontend)
    ↓
Next.js Form Validation
    ↓
API Request to Flask Backend
    ↓
SerpAPI Integration (search_scraper.py)
    ↓
Data Processing (data_processor.py)
    ↓
PDF Report Generation (report_writer.py)
    ↓
File Storage & Download Link
    ↓
PDF Download (Frontend)
```

### Component Communication
- **Frontend ↔ Backend**: REST API calls over HTTPS
- **Backend ↔ SerpAPI**: HTTP requests with API key authentication
- **Backend ↔ File System**: Local file storage for generated reports
- **Frontend ↔ User**: React state management and form handling

### Technology Stack
- **Frontend**: Next.js 14, React 18, TypeScript, TailwindCSS
- **Backend**: Python 3.11, Flask, Jinja2, WeasyPrint
- **APIs**: SerpAPI for search data
- **Deployment**: Vercel (frontend), Heroku (backend)
- **Storage**: Local file system with temporary cleanup

## ⚙️ Environment Variables

### Backend (.env)
```bash
# Required
SERPAPI_KEY=your_serpapi_key_here

# Optional
FLASK_ENV=production
PORT=5000
DEBUG=False
MAX_WORKERS=4
REPORT_CLEANUP_HOURS=24
```

### Frontend (.env.local)
```bash
# Required
NEXT_PUBLIC_API_URL=https://your-backend-url.herokuapp.com

# Optional
NEXT_PUBLIC_ANALYTICS_ID=your_analytics_id
NEXT_PUBLIC_ENVIRONMENT=production
```

### Getting API Keys

#### SerpAPI Key
1. Visit [serpapi.com](https://serpapi.com)
2. Create account and verify email
3. Navigate to Dashboard → API Key
4. Copy your API key
5. **Free tier**: 100 searches/month
6. **Paid plans**: Start at $50/month for 5,000 searches

## 🧪 Testing & Quality Assurance

### Available Test Files
```bash
# Basic functionality tests
python test_basic_functionality.py

# Data processing tests
python test_data_processing.py

# Simple integration tests
python test_simple.py

# Full test suite
pytest tests/ -v --cov=src
```

### Test Coverage Areas
- ✅ **API Integration**: SerpAPI connection and response handling
- ✅ **Data Processing**: Keyword analysis and competitor extraction
- ✅ **Report Generation**: PDF creation and formatting
- ✅ **Configuration**: JSON config validation
- ✅ **Error Handling**: Network failures and invalid inputs

### Manual Testing Checklist
```bash
# 1. Backend API Health Check
curl https://your-backend-url.herokuapp.com/health

# 2. Frontend Accessibility
# Visit https://lrl.northcurrent.digital
# Test form submission with sample data

# 3. End-to-End Report Generation
# Submit form → Verify PDF download → Check report content

# 4. Error Handling
# Test with invalid API key, malformed requests, network issues
```

## 🌐 Domain Configuration

### Current Setup
- **Primary Domain**: `northcurrent.digital` (WordPress on Bluehost)
- **Tool Subdomain**: `lrl.northcurrent.digital` (Next.js on Vercel)
- **Backend API**: `your-app.herokuapp.com` (Flask on Heroku)

### DNS Configuration (Squarespace)
```
# Main domain redirect
northcurrent.digital → ixw.dyz.mybluehost.me (WordPress)

# Subdomain for tool
lrl.northcurrent.digital → CNAME → 7c17do671e75c5b2.vercel-dns-017.com
```

### SSL/HTTPS
- ✅ **Vercel**: Automatic SSL certificates
- ✅ **Heroku**: Automatic SSL certificates
- ✅ **Squarespace**: Managed DNS with SSL support

## 🔧 Development Workflow

### Local Development Setup
```bash
# 1. Start backend
cd NCDLRL1
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export SERPAPI_KEY="your_key"
python app.py

# 2. Start frontend (new terminal)
cd localranklens-frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:5000" > .env.local
npm run dev

# 3. Access application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
```

### Making Changes
1. **Backend Changes**: Edit Python files in `src/`, restart Flask server
2. **Frontend Changes**: Edit React files in `src/app/`, hot reload automatic
3. **Styling Changes**: Edit TailwindCSS classes, automatic rebuild
4. **Configuration**: Edit `config.json`, restart backend

### Deployment Process
```bash
# Backend deployment (Heroku)
git add .
git commit -m "Backend updates"
git push heroku main

# Frontend deployment (Vercel)
cd localranklens-frontend
vercel --prod

# Or use GitHub integration for automatic deployments
```
## 🚨 Troubleshooting Common Issues

### Frontend Issues

#### "API Connection Failed"
```bash
# Check if backend is running
curl https://your-backend-url.herokuapp.com/health

# Verify environment variables
echo $NEXT_PUBLIC_API_URL

# Check browser console for CORS errors
# Open DevTools → Console → Look for network errors
```

#### "Build Failed on Vercel"
```bash
# Common causes:
1. Missing environment variables in Vercel dashboard
2. Node.js version mismatch (ensure Node 18+)
3. TypeScript errors in code

# Solutions:
vercel env add NEXT_PUBLIC_API_URL
vercel --prod --force  # Force rebuild
```

### Backend Issues

#### "SerpAPI Rate Limit Exceeded"
```bash
# Check your SerpAPI usage
curl "https://serpapi.com/account?api_key=YOUR_KEY"

# Solutions:
1. Upgrade SerpAPI plan
2. Implement request caching
3. Add rate limiting to frontend
```

#### "PDF Generation Failed"
```bash
# Check WeasyPrint dependencies
pip install --upgrade weasyprint

# On Ubuntu/Debian:
sudo apt-get install python3-dev python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0

# On macOS:
brew install pango
```

#### "Heroku Deployment Failed"
```bash
# Check logs
heroku logs --tail --app your-app-name

# Common issues:
1. Missing Procfile
2. Wrong Python version in runtime.txt
3. Missing environment variables

# Solutions:
heroku config:set SERPAPI_KEY="your_key"
git push heroku main --force
```

### DNS/Domain Issues

#### "lrl.northcurrent.digital not resolving"
```bash
# Check DNS propagation
nslookup lrl.northcurrent.digital
dig lrl.northcurrent.digital

# Wait 24-48 hours for DNS propagation
# Verify CNAME record in Squarespace DNS settings
```

#### "SSL Certificate Issues"
```bash
# Vercel automatically handles SSL
# If issues persist:
1. Check domain verification in Vercel dashboard
2. Ensure CNAME record is correct
3. Wait for DNS propagation
```

## 📦 Dependencies & Version Requirements

### Backend Dependencies (requirements.txt)
```
Flask==2.3.3
requests==2.31.0
python-dotenv==1.0.0
Jinja2==3.1.2
WeasyPrint==60.2
gunicorn==21.2.0
```

### Frontend Dependencies (package.json)
```json
{
  "dependencies": {
    "next": "14.0.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@tailwindcss/forms": "^0.5.6",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@types/node": "^20.8.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.2.0",
    "tailwindcss": "^3.3.0"
  }
}
```

### System Requirements
- **Python**: 3.10+ (3.11 recommended)
- **Node.js**: 18+ (20 LTS recommended)
- **Memory**: 512MB minimum (1GB recommended)
- **Storage**: 100MB for code + temporary report files

## 🤝 Contributing Guidelines

### For Van Coco & Collaborators

#### Getting Started
1. **Clone the repository**
```bash
git clone https://github.com/dean-alley/NCDLRL1.git
cd NCDLRL1
```

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Set up development environment**
```bash
# Backend setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd localranklens-frontend
npm install
```

#### Development Standards
- **Code Style**: Follow PEP 8 for Python, Prettier for TypeScript
- **Testing**: Add tests for new features
- **Documentation**: Update README for significant changes
- **Commits**: Use descriptive commit messages

#### Pull Request Process
1. **Test your changes locally**
2. **Run the test suite**
3. **Update documentation if needed**
4. **Create pull request with description**
5. **Request review from project maintainer**

#### WordPress Integration Notes
- **Branding**: Tool can be styled to match northcurrent.digital theme
- **User Flow**: Consider single sign-on or user account integration
- **Data**: Reports can be stored in WordPress database if needed
- **Analytics**: Google Analytics integration available

### Code Organization
```bash
# Backend modifications
src/localranklens.py     # Core analysis logic
src/report_writer.py     # PDF customization
app.py                   # API endpoints

# Frontend modifications
src/app/page.tsx         # Main UI components
src/app/globals.css      # Styling and branding
src/app/layout.tsx       # Site metadata and structure
```

## 📊 Performance & Scaling

### Current Limitations
- **SerpAPI**: 100 searches/month on free tier
- **Heroku**: 550 free dyno hours/month
- **Vercel**: Unlimited static hosting, 100GB bandwidth/month
- **Report Storage**: Temporary files cleaned up after 24 hours

### Scaling Considerations
- **Database**: Consider PostgreSQL for report storage
- **Caching**: Implement Redis for search result caching
- **CDN**: Use Vercel Edge Network for global performance
- **Monitoring**: Add application monitoring (Sentry, LogRocket)

### Enterprise Features (Future)
- **Multi-tenant**: Support multiple agencies/clients
- **White-label**: Custom branding per client
- **API Rate Limiting**: Prevent abuse
- **Advanced Analytics**: Usage tracking and insights

## 📞 Support & Contact

### For Technical Issues
- **GitHub Issues**: [Create an issue](https://github.com/dean-alley/NCDLRL1/issues)
- **Documentation**: Check this README and `/docs` folder
- **Logs**: Check Heroku logs and Vercel function logs

### For Business/Integration Questions
- **Primary Contact**: Trei (Project Owner)
- **WordPress Integration**: Van Coco (WordPress Developer)
- **Domain/DNS**: Squarespace + Vercel support

## 📄 License

This project is proprietary software developed for North Current Digital. All rights reserved.

---

## 🎯 Quick Reference for Van Coco

### WordPress Integration Checklist
- [ ] Add button linking to `lrl.northcurrent.digital`
- [ ] Style button to match site theme
- [ ] Test user flow from main site to tool
- [ ] Consider adding tool description/landing page
- [ ] Optional: Add analytics tracking

### Integration Code Snippet
```html
<!-- Add this to your WordPress page/post -->
<div class="lrl-integration">
  <h3>Local SEO Analysis Tool</h3>
  <p>Generate comprehensive local search reports for any business and location.</p>
  <a href="https://lrl.northcurrent.digital" target="_blank" class="btn btn-primary">
    Launch LocalRankLens Tool →
  </a>
</div>
```

**That's it! The tool is ready for integration. 🚀**

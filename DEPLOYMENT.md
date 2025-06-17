# LocalRankLens Deployment Guide

## Frontend Deployment to Vercel

### Quick Deploy (Recommended)

1. **Push to GitHub**:
   ```bash
   git push origin master
   ```

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select the `localranklens-frontend` folder as the root directory
   - Click "Deploy"

3. **Configuration**:
   - Framework Preset: Next.js
   - Root Directory: `localranklens-frontend`
   - Build Command: `npm run build` (auto-detected)
   - Output Directory: `.next` (auto-detected)

### Manual Deployment

If you prefer manual deployment:

```bash
cd localranklens-frontend
npm install
npm run build
```

Then upload the `.next` folder to your hosting provider.

### Environment Variables

Currently, no environment variables are required for the frontend. The application generates config files client-side.

## Backend System (LocalRankLens Core)

The Python backend system requires:

1. **Python Environment**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file:
   ```
   SERPAPI_KEY=your_serpapi_key_here
   LOG_LEVEL=INFO
   OUTPUT_DIR=output
   ```

3. **Run Analysis**:
   ```bash
   python run_localranklens.py
   ```

## Complete Workflow

1. **Generate Config**: Use the web frontend to create config.json
2. **Download Config**: Save the generated configuration file
3. **Upload to Backend**: Place config.json in your LocalRankLens system
4. **Run Analysis**: Execute the Python script to generate reports
5. **View Results**: Open the generated HTML report

## System Requirements

### Frontend
- Node.js 18+
- Modern web browser
- Internet connection

### Backend
- Python 3.8+
- SerpAPI account and key
- Internet connection for API calls

## Troubleshooting

### Frontend Issues
- **Build Errors**: Check Node.js version (18+ required)
- **Styling Issues**: Ensure Tailwind CSS is properly configured
- **TypeScript Errors**: Run `npm run lint` to check for issues

### Backend Issues
- **API Errors**: Verify SERPAPI_KEY is valid and has credits
- **Config Errors**: Ensure config.json has required fields (business_name, location, keywords, output_prefix)
- **Slice Errors**: Update to latest version with fixed data processor

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify all requirements are met
3. Ensure API keys are valid and have sufficient credits
4. Review the generated config file format

## Next Steps

Future enhancements could include:
- Direct API integration between frontend and backend
- Real-time analysis progress tracking
- Report viewing within the web interface
- User authentication and saved configurations
- Batch processing for multiple businesses

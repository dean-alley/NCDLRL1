import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const config = await request.json();

    // Validate required fields
    if (!config.business_name || !config.location?.city || !config.location?.state || !config.keywords) {
      return NextResponse.json(
        { error: 'Missing required fields: business_name, location, or keywords' },
        { status: 400 }
      );
    }

    // Get Heroku backend URL from environment variable
    const backendUrl = process.env.HEROKU_BACKEND_URL || 'https://your-app-name.herokuapp.com';

    // Forward the request to the Heroku backend
    const response = await fetch(`${backendUrl}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config),
    });

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json(
        { error: `Backend analysis failed: ${errorText}` },
        { status: response.status }
      );
    }

    // Get the HTML report from the backend
    const htmlContent = await response.text();

    // Return the HTML report
    return new NextResponse(htmlContent, {
      headers: {
        'Content-Type': 'text/html',
        'Content-Disposition': `attachment; filename="localranklens-report.html"`,
      },
    });
  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

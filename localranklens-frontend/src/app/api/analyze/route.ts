import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import { writeFileSync, readFileSync, unlinkSync, readdirSync, statSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

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

    // Create temporary config file
    const tempConfigPath = join(tmpdir(), `config_${Date.now()}.json`);
    writeFileSync(tempConfigPath, JSON.stringify(config, null, 2));

    // Get the path to the LocalRankLens backend
    // This assumes the backend is in the parent directory
    const backendPath = join(process.cwd(), '..', 'run_localranklens.py');
    
    return new Promise<NextResponse>((resolve) => {
      // Run the LocalRankLens analysis
      const pythonProcess = spawn('python', [backendPath], {
        cwd: join(process.cwd(), '..'),
        env: {
          ...process.env,
          CONFIG_PATH: tempConfigPath
        }
      });

      let stderr = '';

      pythonProcess.stdout.on('data', (data) => {
        // Log stdout for debugging but don't store it
        console.log('Python output:', data.toString());
      });

      pythonProcess.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      pythonProcess.on('close', (code) => {
        // Clean up temp config file
        try {
          unlinkSync(tempConfigPath);
        } catch (e) {
          console.warn('Could not delete temp config file:', e);
        }

        if (code !== 0) {
          console.error('Python process failed:', stderr);
          resolve(NextResponse.json(
            { error: `Analysis failed: ${stderr || 'Unknown error'}` },
            { status: 500 }
          ));
          return;
        }

        try {
          // Find the most recent HTML report
          const outputDir = join(process.cwd(), '..', 'output');
          const files = readdirSync(outputDir);
          const htmlFiles = files.filter((file: string) => file.endsWith('.html'));

          // Sort by modification time and get the most recent
          const htmlFile = htmlFiles
            .map(file => ({
              name: file,
              path: join(outputDir, file),
              mtime: statSync(join(outputDir, file)).mtime
            }))
            .sort((a, b) => b.mtime.getTime() - a.mtime.getTime())[0]?.name;

          if (!htmlFile) {
            resolve(NextResponse.json(
              { error: 'Report file not found' },
              { status: 500 }
            ));
            return;
          }

          // Read the HTML report
          const htmlPath = join(outputDir, htmlFile);
          const htmlContent = readFileSync(htmlPath, 'utf-8');

          // Return the HTML as a downloadable file
          resolve(new NextResponse(htmlContent, {
            headers: {
              'Content-Type': 'text/html',
              'Content-Disposition': `attachment; filename="${htmlFile}"`,
            },
          }));

        } catch (error) {
          console.error('Error reading report file:', error);
          resolve(NextResponse.json(
            { error: 'Error reading generated report' },
            { status: 500 }
          ));
        }
      });

      // Handle process errors
      pythonProcess.on('error', (error) => {
        console.error('Failed to start Python process:', error);
        try {
          unlinkSync(tempConfigPath);
        } catch (e) {
          console.warn('Could not delete temp config file:', e);
        }
        
        resolve(NextResponse.json(
          { error: 'Failed to start analysis process' },
          { status: 500 }
        ));
      });
    });

  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

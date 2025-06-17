# LocalRankLens Frontend

A Next.js web application for generating LocalRankLens configuration files. This frontend provides an intuitive interface for setting up local search competitive intelligence analysis.

## Features

- **Business Information Setup**: Enter business name, location, and output preferences
- **Dynamic Keyword Groups**: Create multiple keyword categories (core, emergency, upsell, etc.)
- **Real-time Configuration**: Generate JSON config files for LocalRankLens analysis
- **Responsive Design**: Works on desktop and mobile devices
- **Vercel Ready**: Optimized for deployment on Vercel

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:

```bash
npm install
```

3. Run the development server:

```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Usage

1. **Fill Business Information**: Enter your business name and target location
2. **Add Keyword Groups**: Create categories like "core", "emergency", "upsell"
3. **Enter Keywords**: Add relevant search terms for each group
4. **Generate Config**: Download the JSON configuration file
5. **Use with LocalRankLens**: Upload the config to your LocalRankLens system

## Deployment

### Deploy to Vercel

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Deploy automatically with zero configuration

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/localranklens-frontend)

### Manual Deployment

```bash
npm run build
npm run start
```

## Technology Stack

- **Framework**: Next.js 15.3.3
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Deployment**: Vercel

## Project Structure

```
src/
├── app/
│   ├── page.tsx          # Main configuration form
│   ├── layout.tsx        # App layout
│   └── globals.css       # Global styles
└── components/           # Reusable components (future)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is part of the LocalRankLens system for local search competitive intelligence.

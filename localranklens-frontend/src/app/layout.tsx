import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "LocalRankLens - Local Search Competitive Intelligence",
  description: "Generate comprehensive competitive intelligence reports for local search rankings and SEO analysis. Discover competitor strategies, keyword gaps, and market opportunities in your local area.",
  keywords: ["local SEO", "competitive intelligence", "search rankings", "local search", "SEO analysis", "competitor research"],
  authors: [{ name: "LocalRankLens" }],
  creator: "LocalRankLens",
  publisher: "LocalRankLens",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://lrl.northcurrent.digital",
    siteName: "LocalRankLens",
    title: "LocalRankLens - Local Search Competitive Intelligence",
    description: "Generate comprehensive competitive intelligence reports for local search rankings and SEO analysis. Discover competitor strategies, keyword gaps, and market opportunities in your local area.",
    images: [
      {
        url: "/og-image.svg",
        width: 1200,
        height: 630,
        alt: "LocalRankLens - Local Search Competitive Intelligence",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    site: "@localranklens",
    creator: "@localranklens",
    title: "LocalRankLens - Local Search Competitive Intelligence",
    description: "Generate comprehensive competitive intelligence reports for local search rankings and SEO analysis.",
    images: ["/og-image.svg"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    google: "your-google-verification-code",
  },
  icons: {
    icon: [
      { url: "/favicon.svg", type: "image/svg+xml" },
      { url: "/favicon.ico", sizes: "any" },
    ],
    apple: "/apple-touch-icon.png",
  },
  manifest: "/site.webmanifest",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}

'use client';

import { useState, useEffect } from 'react';

interface KeywordGroup {
  name: string;
  keywords: string[];
}

// Default example data for quick testing
const defaultData = {
  businessName: "Dan's Dispensary",
  city: "Anoka",
  state: "MN",
  keywordGroups: [
    {
      name: 'core',
      keywords: [
        'cannabis dispensary near me',
        'marijuana dispensary Anoka',
        'weed shop Anoka MN',
        'THC products Anoka',
        'medical marijuana Anoka'
      ]
    },
    {
      name: 'products',
      keywords: [
        'indica sativa hybrid Anoka',
        'edibles gummies Anoka',
        'vape cartridges Anoka',
        'concentrates dabs Anoka'
      ]
    }
  ]
};

export default function Home() {
  const [businessName, setBusinessName] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [outputPrefix, setOutputPrefix] = useState('');
  const [keywordGroups, setKeywordGroups] = useState<KeywordGroup[]>([
    { name: 'core', keywords: [''] },
  ]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isGeneratingKeywords, setIsGeneratingKeywords] = useState(false);
  const [keywordSuggestionsGenerated, setKeywordSuggestionsGenerated] = useState(false);

  // Load data from localStorage on component mount
  useEffect(() => {
    const savedData = localStorage.getItem('localranklens-form-data');
    if (savedData) {
      try {
        const parsed = JSON.parse(savedData);
        setBusinessName(parsed.businessName || '');
        setCity(parsed.city || '');
        setState(parsed.state || '');
        setOutputPrefix(parsed.outputPrefix || '');
        setKeywordGroups(parsed.keywordGroups || [{ name: 'core', keywords: [''] }]);
        setKeywordSuggestionsGenerated(parsed.keywordSuggestionsGenerated || false);
      } catch (e) {
        console.warn('Failed to load saved form data:', e);
      }
    }
  }, []);

  // Save data to localStorage whenever form data changes
  useEffect(() => {
    const formData = {
      businessName,
      city,
      state,
      outputPrefix,
      keywordGroups,
      keywordSuggestionsGenerated
    };
    localStorage.setItem('localranklens-form-data', JSON.stringify(formData));
  }, [businessName, city, state, outputPrefix, keywordGroups, keywordSuggestionsGenerated]);

  // Auto-generate keywords when business info is complete
  useEffect(() => {
    if (businessName && city && state && !keywordSuggestionsGenerated) {
      // Small delay to avoid triggering while user is still typing
      const timer = setTimeout(() => {
        generateKeywordSuggestions(businessName, city, state);
      }, 500);

      return () => clearTimeout(timer);
    }
  }, [businessName, city, state, keywordSuggestionsGenerated]); // eslint-disable-line react-hooks/exhaustive-deps

  const loadExampleData = () => {
    setBusinessName(defaultData.businessName);
    setCity(defaultData.city);
    setState(defaultData.state);
    setOutputPrefix('');
    setKeywordGroups(defaultData.keywordGroups);
  };

  const clearForm = () => {
    setBusinessName('');
    setCity('');
    setState('');
    setOutputPrefix('');
    setKeywordGroups([{ name: 'core', keywords: [''] }]);
    setKeywordSuggestionsGenerated(false);
    localStorage.removeItem('localranklens-form-data');
  };

  // Industry keyword templates based on business analysis
  const generateKeywordSuggestions = async (businessName: string, city: string, state: string) => {
    if (!businessName || !city || !state || keywordSuggestionsGenerated) return;

    setIsGeneratingKeywords(true);

    try {
      // Analyze business type from name
      const businessLower = businessName.toLowerCase();
      const location = `${city}, ${state}`;
      const locationShort = `${city}`;

      let suggestedGroups: KeywordGroup[] = [];

      // Industry detection and keyword generation
      if (businessLower.includes('dispensary') || businessLower.includes('cannabis') || businessLower.includes('marijuana') || businessLower.includes('weed')) {
        suggestedGroups = [
          {
            name: 'core',
            keywords: [
              `cannabis dispensary ${locationShort}`,
              `marijuana dispensary near me`,
              `weed shop ${locationShort} ${state}`,
              `THC products ${locationShort}`,
              `medical marijuana ${locationShort}`
            ]
          },
          {
            name: 'products',
            keywords: [
              `indica sativa hybrid ${locationShort}`,
              `edibles gummies ${locationShort}`,
              `vape cartridges ${locationShort}`,
              `concentrates dabs ${locationShort}`,
              `CBD products ${locationShort}`
            ]
          },
          {
            name: 'services',
            keywords: [
              `cannabis delivery ${locationShort}`,
              `marijuana consultation ${locationShort}`,
              `medical card help ${locationShort}`
            ]
          }
        ];
      } else if (businessLower.includes('plumb') || businessLower.includes('pipe') || businessLower.includes('drain')) {
        suggestedGroups = [
          {
            name: 'core',
            keywords: [
              `plumber ${locationShort}`,
              `plumbing repair ${locationShort}`,
              `emergency plumber ${locationShort}`,
              `drain cleaning ${locationShort}`,
              `pipe repair ${locationShort}`
            ]
          },
          {
            name: 'emergency',
            keywords: [
              `24 hour plumber ${locationShort}`,
              `emergency plumbing ${locationShort}`,
              `burst pipe repair ${locationShort}`,
              `water leak repair ${locationShort}`
            ]
          },
          {
            name: 'services',
            keywords: [
              `water heater repair ${locationShort}`,
              `toilet repair ${locationShort}`,
              `sewer line repair ${locationShort}`,
              `bathroom plumbing ${locationShort}`
            ]
          }
        ];
      } else if (businessLower.includes('irrigation') || businessLower.includes('sprinkler') || businessLower.includes('lawn')) {
        suggestedGroups = [
          {
            name: 'core',
            keywords: [
              `sprinkler system installation ${locationShort}`,
              `irrigation system ${locationShort}`,
              `sprinkler repair ${locationShort}`,
              `lawn irrigation ${locationShort}`,
              `sprinkler startup ${locationShort}`
            ]
          },
          {
            name: 'seasonal',
            keywords: [
              `sprinkler blowout ${locationShort}`,
              `irrigation winterization ${locationShort}`,
              `spring sprinkler startup ${locationShort}`
            ]
          },
          {
            name: 'upsell',
            keywords: [
              `smart sprinkler system ${locationShort}`,
              `wifi irrigation controller ${locationShort}`,
              `water efficient irrigation ${locationShort}`
            ]
          }
        ];
      } else if (businessLower.includes('restaurant') || businessLower.includes('food') || businessLower.includes('cafe') || businessLower.includes('diner')) {
        suggestedGroups = [
          {
            name: 'core',
            keywords: [
              `restaurant ${locationShort}`,
              `best food ${locationShort}`,
              `dining ${locationShort}`,
              `${businessName.replace(/restaurant|cafe|diner/gi, '').trim()} ${locationShort}`,
              `restaurants near me`
            ]
          },
          {
            name: 'services',
            keywords: [
              `takeout ${locationShort}`,
              `delivery ${locationShort}`,
              `catering ${locationShort}`,
              `reservations ${locationShort}`
            ]
          }
        ];
      } else if (businessLower.includes('auto') || businessLower.includes('car') || businessLower.includes('mechanic') || businessLower.includes('repair')) {
        suggestedGroups = [
          {
            name: 'core',
            keywords: [
              `auto repair ${locationShort}`,
              `car mechanic ${locationShort}`,
              `automotive service ${locationShort}`,
              `car repair ${locationShort}`,
              `mechanic near me`
            ]
          },
          {
            name: 'services',
            keywords: [
              `oil change ${locationShort}`,
              `brake repair ${locationShort}`,
              `transmission repair ${locationShort}`,
              `tire service ${locationShort}`
            ]
          }
        ];
      } else {
        // Generic business keywords
        const businessType = businessName.split(' ')[0].toLowerCase();
        suggestedGroups = [
          {
            name: 'core',
            keywords: [
              `${businessType} ${locationShort}`,
              `${businessName} ${locationShort}`,
              `${businessType} near me`,
              `best ${businessType} ${locationShort}`,
              `${businessType} services ${locationShort}`
            ]
          },
          {
            name: 'local',
            keywords: [
              `${businessType} ${location}`,
              `local ${businessType} ${locationShort}`,
              `${locationShort} ${businessType}`
            ]
          }
        ];
      }

      // Set the generated keywords
      setKeywordGroups(suggestedGroups);
      setKeywordSuggestionsGenerated(true);

    } catch (error) {
      console.error('Error generating keyword suggestions:', error);
    } finally {
      setIsGeneratingKeywords(false);
    }
  };

  const addKeywordGroup = () => {
    setKeywordGroups([...keywordGroups, { name: '', keywords: [''] }]);
  };

  const updateGroupName = (index: number, name: string) => {
    const updated = [...keywordGroups];
    updated[index].name = name;
    setKeywordGroups(updated);
  };

  const addKeyword = (groupIndex: number) => {
    const updated = [...keywordGroups];
    updated[groupIndex].keywords.push('');
    setKeywordGroups(updated);
  };

  const updateKeyword = (groupIndex: number, keywordIndex: number, value: string) => {
    const updated = [...keywordGroups];
    updated[groupIndex].keywords[keywordIndex] = value;
    setKeywordGroups(updated);
  };

  const removeKeyword = (groupIndex: number, keywordIndex: number) => {
    const updated = [...keywordGroups];
    updated[groupIndex].keywords.splice(keywordIndex, 1);
    if (updated[groupIndex].keywords.length === 0) {
      updated[groupIndex].keywords.push('');
    }
    setKeywordGroups(updated);
  };

  const removeGroup = (index: number) => {
    if (keywordGroups.length > 1) {
      const updated = [...keywordGroups];
      updated.splice(index, 1);
      setKeywordGroups(updated);
    }
  };



  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);

    try {
      // Convert form data to simple keywords format for the API
      const allKeywords = keywordGroups
        .flatMap(group => group.keywords)
        .filter(keyword => keyword.trim())
        .join('\n');

      const formData = {
        business_name: businessName,
        location: {
          city: city,
          state: state
        },
        keywords: allKeywords
      };

      // Call the LocalRankLens API to generate the report
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }

      // Get the PDF report as a blob
      const pdfBlob = await response.blob();

      // Auto-download the PDF report
      const url = URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${businessName.toLowerCase().replace(/[^a-z0-9]/g, '-')}_${new Date().toISOString().slice(0, 10)}_report.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      alert('Analysis complete! Your comprehensive competitive intelligence report has been downloaded.');
    } catch (error) {
      console.error('Error:', error);
      alert(`Error generating report: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold text-white">LocalRankLens</h1>
              </div>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                Home
              </a>
              <a href="#" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                Features
              </a>
              <a href="#" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                Pricing
              </a>
              <a href="#" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                Contact
              </a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative bg-gray-900 py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
              YOUR GROWTH-DRIVEN
              <span className="block text-blue-400">COMPETITIVE INTELLIGENCE</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-4xl mx-auto">
              LocalRankLens is a competitive intelligence generator serving local businesses ready for hyper growth and market dominance.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="#analyzer" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold text-lg transition-colors">
                START FREE ANALYSIS
              </a>
              <a href="#features" className="border border-gray-600 hover:border-gray-500 text-gray-300 hover:text-white px-8 py-3 rounded-lg font-semibold text-lg transition-colors">
                Learn More
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">OUR PROVIDED SERVICES</h2>
            <p className="text-xl text-gray-300 max-w-4xl mx-auto">
              LocalRankLens redefines &quot;competitive intelligence&quot; by empowering companies to understand their local search landscape,
              moving them beyond guesswork to achieving true market insight.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-gray-900 p-6 rounded-lg border border-gray-700">
              <div className="text-blue-400 text-2xl mb-4">🔍</div>
              <h3 className="text-xl font-semibold text-white mb-3">Local Search Analysis</h3>
              <p className="text-gray-300">
                Comprehensive analysis of local search rankings, competitor positioning, and market opportunities.
              </p>
            </div>

            <div className="bg-gray-900 p-6 rounded-lg border border-gray-700">
              <div className="text-green-400 text-2xl mb-4">📊</div>
              <h3 className="text-xl font-semibold text-white mb-3">Competitive Intelligence</h3>
              <p className="text-gray-300">
                Detailed reports on competitor strategies, keyword gaps, and market positioning insights.
              </p>
            </div>

            <div className="bg-gray-900 p-6 rounded-lg border border-gray-700">
              <div className="text-purple-400 text-2xl mb-4">⚡</div>
              <h3 className="text-xl font-semibold text-white mb-3">Actionable Reports</h3>
              <p className="text-gray-300">
                Get clear, jargon-free reports with specific recommendations for improving your local search presence.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Analyzer Section */}
      <section id="analyzer" className="py-16 bg-gray-900">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">
              🔍 Generate Your Competitive Intelligence Report
            </h2>
            <p className="text-xl text-gray-300">
              Get a comprehensive analysis of your local search landscape—Free.
            </p>
          </div>

          <div className="bg-gray-800 shadow-2xl rounded-lg p-8 border border-gray-700">
            <form onSubmit={handleSubmit} className="space-y-8">
              {/* Business Information */}
              <div className="mb-6">
                <label htmlFor="businessName" className="block text-sm font-medium text-gray-300 mb-2">
                  Business Name *
                </label>
                <input
                  type="text"
                  id="businessName"
                  value={businessName}
                  onChange={(e) => setBusinessName(e.target.value)}
                  required
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                  placeholder="e.g., Revive Irrigation"
                />
              </div>

              {/* Location */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="city" className="block text-sm font-medium text-gray-300 mb-2">
                    City *
                  </label>
                  <input
                    type="text"
                    id="city"
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    required
                    className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    placeholder="e.g., Spokane"
                  />
                </div>

                <div>
                  <label htmlFor="state" className="block text-sm font-medium text-gray-300 mb-2">
                    State *
                  </label>
                  <input
                    type="text"
                    id="state"
                    value={state}
                    onChange={(e) => setState(e.target.value)}
                    required
                    className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    placeholder="e.g., WA"
                  />
                </div>
              </div>

              {/* Keyword Groups */}
              <div>
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-medium text-white">Keyword Groups</h3>
                  <button
                    type="button"
                    onClick={addKeywordGroup}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
                  >
                    Add Group
                  </button>
                </div>

                {/* Utility Buttons */}
                <div className="flex flex-wrap gap-3 mb-6 p-4 bg-gray-700 rounded-lg border border-gray-600">
                  <button
                    type="button"
                    onClick={loadExampleData}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors text-sm"
                  >
                    📝 Load Example (Dispensary)
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setKeywordSuggestionsGenerated(false);
                      generateKeywordSuggestions(businessName, city, state);
                    }}
                    disabled={!businessName || !city || !state || isGeneratingKeywords}
                    className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
                  >
                    {isGeneratingKeywords ? '🔄 Generating...' : '🤖 AI Suggest Keywords'}
                  </button>
                  <button
                    type="button"
                    onClick={clearForm}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors text-sm"
                  >
                    🗑️ Clear All
                  </button>
                  <div className="text-gray-300 text-sm flex items-center">
                    💾 Form auto-saves as you type
                  </div>
                </div>

                {/* Auto-generation status */}
                {isGeneratingKeywords && (
                  <div className="mb-4 p-3 bg-blue-900 border border-blue-700 rounded-lg">
                    <div className="flex items-center text-blue-200">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-400 mr-2"></div>
                      Analyzing &quot;{businessName}&quot; in {city}, {state} to generate industry-specific keywords...
                    </div>
                  </div>
                )}

                {keywordSuggestionsGenerated && !isGeneratingKeywords && (
                  <div className="mb-4 p-3 bg-green-900 border border-green-700 rounded-lg">
                    <div className="text-green-200">
                      ✅ AI-generated keywords based on your business type and location. You can edit or add more keywords below.
                    </div>
                  </div>
                )}

                {keywordGroups.map((group, groupIndex) => (
                  <div key={groupIndex} className="border border-gray-600 rounded-lg p-6 mb-6 bg-gray-700">
                    <div className="flex justify-between items-center mb-4">
                      <input
                        type="text"
                        value={group.name}
                        onChange={(e) => updateGroupName(groupIndex, e.target.value)}
                        placeholder="Group name (e.g., core, emergency, upsell)"
                        className="flex-1 px-4 py-3 bg-gray-600 border border-gray-500 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 mr-3 transition-colors"
                      />
                      {keywordGroups.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeGroup(groupIndex)}
                          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors"
                        >
                          Remove Group
                        </button>
                      )}
                    </div>

                    {group.keywords.map((keyword, keywordIndex) => (
                      <div key={keywordIndex} className="flex items-center mb-3">
                        <input
                          type="text"
                          value={keyword}
                          onChange={(e) => updateKeyword(groupIndex, keywordIndex, e.target.value)}
                          placeholder="Enter keyword (e.g., sprinkler repair Spokane)"
                          className="flex-1 px-4 py-3 bg-gray-600 border border-gray-500 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 mr-3 transition-colors"
                        />
                        <button
                          type="button"
                          onClick={() => removeKeyword(groupIndex, keywordIndex)}
                          className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-400 transition-colors"
                        >
                          Remove
                        </button>
                      </div>
                    ))}

                    <button
                      type="button"
                      onClick={() => addKeyword(groupIndex)}
                      className="mt-3 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors"
                    >
                      Add Keyword
                    </button>
                  </div>
                ))}
              </div>

              {/* Submit Button */}
              <div className="text-center">
                <button
                  type="submit"
                  disabled={isGenerating || !businessName || !city || !state}
                  className="px-8 py-4 bg-blue-600 text-white font-semibold text-lg rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isGenerating ? 'Analyzing...' : 'Generate Report'}
                </button>
              </div>
            </form>
          </div>

          {/* Instructions */}
          <div className="mt-12 bg-gray-800 border border-gray-700 rounded-lg p-8">
            <h3 className="text-xl font-semibold text-white mb-4">⚡ What You Get</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <ul className="space-y-3 text-gray-300">
                  <li className="flex items-start">
                    <span className="text-green-400 mr-2">✓</span>
                    Local Search Ranking Analysis
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-400 mr-2">✓</span>
                    Competitor Positioning Map
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-400 mr-2">✓</span>
                    Keyword Gap Analysis
                  </li>
                </ul>
              </div>
              <div>
                <ul className="space-y-3 text-gray-300">
                  <li className="flex items-start">
                    <span className="text-green-400 mr-2">✓</span>
                    Market Opportunity Insights
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-400 mr-2">✓</span>
                    Actionable Recommendations
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-400 mr-2">✓</span>
                    Comprehensive HTML Report
                  </li>
                </ul>
              </div>
            </div>

            <div className="mt-8 p-4 bg-blue-900 border border-blue-700 rounded-lg">
              <p className="text-blue-200 text-center">
                <strong>⚡ If we don&apos;t find at least 3 growth opportunities – we&apos;ll refund your time.</strong><br />
                No pressure, just results.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="col-span-1 md:col-span-2">
              <h3 className="text-xl font-bold text-white mb-4">LocalRankLens</h3>
              <p className="text-gray-300 mb-4">
                Your growth-driven competitive intelligence partner for local search dominance.
              </p>
              <p className="text-gray-400 text-sm">
                © 2024 LocalRankLens. All rights reserved.
              </p>
            </div>

            <div>
              <h4 className="text-lg font-semibold text-white mb-4">Services</h4>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors">Local SEO Analysis</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Competitor Research</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Market Intelligence</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Ranking Reports</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-lg font-semibold text-white mb-4">Contact</h4>
              <ul className="space-y-2 text-gray-300">
                <li>support@localranklens.com</li>
                <li>1-800-RANK-LENS</li>
                <li>Available 24/7</li>
              </ul>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

'use client';

import { useState } from 'react';

interface KeywordGroup {
  name: string;
  keywords: string[];
}

export default function Home() {
  const [businessName, setBusinessName] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [outputPrefix, setOutputPrefix] = useState('');
  const [keywordGroups, setKeywordGroups] = useState<KeywordGroup[]>([
    { name: 'core', keywords: [''] },
  ]);
  const [isGenerating, setIsGenerating] = useState(false);

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

  const generateConfig = () => {
    const config = {
      business_name: businessName,
      location: {
        city: city,
        state: state
      },
      keywords: {} as Record<string, string[]>,
      output_prefix: outputPrefix || businessName.toLowerCase().replace(/\s+/g, '-')
    };

    keywordGroups.forEach(group => {
      if (group.name && group.keywords.some(k => k.trim())) {
        config.keywords[group.name] = group.keywords.filter(k => k.trim());
      }
    });

    return config;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    
    try {
      const config = generateConfig();
      
      // For now, just download the config file
      // Later we'll integrate with the backend API
      const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'config.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      alert('Config file downloaded! Upload this to your LocalRankLens system to run the analysis.');
    } catch (error) {
      console.error('Error:', error);
      alert('Error generating config file');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            LocalRankLens
          </h1>
          <p className="text-xl text-gray-600">
            Local Search Competitive Intelligence Generator
          </p>
        </div>

        <div className="bg-white shadow-xl rounded-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Business Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="businessName" className="block text-sm font-medium text-gray-700 mb-2">
                  Business Name *
                </label>
                <input
                  type="text"
                  id="businessName"
                  value={businessName}
                  onChange={(e) => setBusinessName(e.target.value)}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="e.g., Revive Irrigation"
                />
              </div>
              
              <div>
                <label htmlFor="outputPrefix" className="block text-sm font-medium text-gray-700 mb-2">
                  Output Prefix
                </label>
                <input
                  type="text"
                  id="outputPrefix"
                  value={outputPrefix}
                  onChange={(e) => setOutputPrefix(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Auto-generated from business name"
                />
              </div>
            </div>

            {/* Location */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="city" className="block text-sm font-medium text-gray-700 mb-2">
                  City *
                </label>
                <input
                  type="text"
                  id="city"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="e.g., Spokane"
                />
              </div>
              
              <div>
                <label htmlFor="state" className="block text-sm font-medium text-gray-700 mb-2">
                  State *
                </label>
                <input
                  type="text"
                  id="state"
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="e.g., WA"
                />
              </div>
            </div>

            {/* Keyword Groups */}
            <div>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-900">Keyword Groups</h3>
                <button
                  type="button"
                  onClick={addKeywordGroup}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  Add Group
                </button>
              </div>

              {keywordGroups.map((group, groupIndex) => (
                <div key={groupIndex} className="border border-gray-200 rounded-lg p-4 mb-4">
                  <div className="flex justify-between items-center mb-3">
                    <input
                      type="text"
                      value={group.name}
                      onChange={(e) => updateGroupName(groupIndex, e.target.value)}
                      placeholder="Group name (e.g., core, emergency, upsell)"
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 mr-3"
                    />
                    {keywordGroups.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeGroup(groupIndex)}
                        className="px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
                      >
                        Remove Group
                      </button>
                    )}
                  </div>

                  {group.keywords.map((keyword, keywordIndex) => (
                    <div key={keywordIndex} className="flex items-center mb-2">
                      <input
                        type="text"
                        value={keyword}
                        onChange={(e) => updateKeyword(groupIndex, keywordIndex, e.target.value)}
                        placeholder="Enter keyword (e.g., sprinkler repair Spokane)"
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 mr-2"
                      />
                      <button
                        type="button"
                        onClick={() => removeKeyword(groupIndex, keywordIndex)}
                        className="px-3 py-2 bg-gray-400 text-white rounded-md hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-400"
                      >
                        Remove
                      </button>
                    </div>
                  ))}

                  <button
                    type="button"
                    onClick={() => addKeyword(groupIndex)}
                    className="mt-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
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
                className="px-8 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGenerating ? 'Generating...' : 'Generate Config File'}
              </button>
            </div>
          </form>
        </div>

        {/* Instructions */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-medium text-blue-900 mb-3">How to Use</h3>
          <ol className="list-decimal list-inside text-blue-800 space-y-2">
            <li>Fill in your business information and target location</li>
            <li>Add keyword groups (e.g., core, emergency, upsell) with relevant search terms</li>
            <li>Click "Generate Config File" to download your configuration</li>
            <li>Upload the config.json file to your LocalRankLens system</li>
            <li>Run the analysis to get your competitive intelligence report</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

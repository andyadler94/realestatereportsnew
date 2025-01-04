import React from 'react';
import { Key, Copy, Check } from 'lucide-react';
import { generateApiKey } from '../utils/apiKeys';

export default function ApiKeyManager() {
  const [apiKey, setApiKey] = React.useState<string>('');
  const [copied, setCopied] = React.useState(false);

  const handleGenerateKey = () => {
    const newKey = generateApiKey();
    setApiKey(newKey);
  };

  const handleCopyKey = () => {
    navigator.clipboard.writeText(apiKey);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex items-center mb-4">
        <Key className="w-5 h-5 text-blue-600 mr-2" />
        <h2 className="text-lg font-semibold">API Access</h2>
      </div>
      
      <p className="text-sm text-gray-600 mb-4">
        Generate an API key to access the real estate search API programmatically.
      </p>

      <div className="space-y-4">
        {apiKey ? (
          <div className="flex items-center space-x-2">
            <code className="flex-1 bg-gray-50 p-3 rounded-md text-sm font-mono">
              {apiKey}
            </code>
            <button
              onClick={handleCopyKey}
              className="p-2 text-gray-600 hover:text-blue-600 transition-colors"
              title="Copy API key"
            >
              {copied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
            </button>
          </div>
        ) : (
          <button
            onClick={handleGenerateKey}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
          >
            Generate API Key
          </button>
        )}
      </div>
    </div>
  );
}
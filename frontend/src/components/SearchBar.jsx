import React, { useState } from 'react';

const SearchBar = ({ onAnalyze, loading }) => {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url) onAnalyze(url);
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4 mb-6">
      <input 
        type="url" 
        required
        className="flex-grow border border-gray-300 p-3 rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500" 
        placeholder="Paste Amazon Best Sellers URL..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button 
        type="submit"
        className="bg-gray-900 text-white px-8 py-3 rounded font-semibold shadow hover:bg-gray-800 disabled:opacity-50 transition-colors"
        disabled={loading}
      >
        {loading ? 'Analyzing...' : 'Analyze Market'}
      </button>
    </form>
  );
};

export default SearchBar;
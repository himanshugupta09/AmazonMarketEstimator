import React, { useState } from 'react';
import axios from 'axios';
import SearchBar from './components/SearchBar';
import ResultsDashboard from './components/ResultsDashboard';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async (url) => {
    setLoading(true);
    setError('');
    setData(null);
    try {
      // NOTE: Change this to your live Render URL when deploying the frontend to Vercel
      const API_URL = process.env.REACT_APP_API_URL || 'https://amazonmarketestimator.onrender.com'; 
      const response = await axios.post(API_URL, { url });
      setData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'System Error: Failed to communicate with backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 py-12 px-4 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-5xl mx-auto bg-white p-6 sm:p-10 rounded-2xl shadow-xl border border-gray-200">
        <div className="mb-8 border-b border-gray-100 pb-6">
          <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Market Intelligence Estimator</h1>
          <p className="text-gray-500 mt-2 text-lg">AI-driven revenue analysis & heuristic sales estimation for Amazon categories.</p>
        </div>
        
        <SearchBar onAnalyze={handleAnalyze} loading={loading} />
        
        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-lg mb-6 border border-red-200 shadow-sm">
            {error}
          </div>
        )}
        
        <ResultsDashboard data={data} />
      </div>
    </div>
  );
}

export default App;
import React from 'react';

const ResultsDashboard = ({ data }) => {
  if (!data) return null;

  return (
    <div className="animate-fade-in">
      {data.is_mock_data && (
        <div className="bg-amber-50 border-l-4 border-amber-500 text-amber-800 p-4 mb-6 rounded-r">
          <p className="font-bold">Notice: Live Scraping Unreachable</p>
          <p className="text-sm mt-1">Amazon's WAF blocked the request or TinyFish timed out. Displaying resilient fallback mock data to demonstrate system UI and math functionality.</p>
        </div>
      )}

      <div className="bg-slate-50 p-6 rounded-lg mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center border border-slate-200 shadow-sm gap-4">
        <div>
          <p className="text-sm text-slate-500 font-semibold uppercase tracking-wider">AI Identified Niche</p>
          <p className="text-2xl font-bold capitalize text-slate-900">{data.market_niche}</p>
        </div>
        <div className="sm:text-right">
          <p className="text-sm text-slate-500 font-semibold uppercase tracking-wider">Top 10 Est. Revenue</p>
          <p className="text-3xl font-extrabold text-emerald-600">
            ${data.total_estimated_revenue.toLocaleString(undefined, {minimumFractionDigits: 2})}
          </p>
        </div>
      </div>

      <div className="overflow-x-auto border border-gray-200 rounded-lg shadow-sm">
        <table className="w-full text-left border-collapse bg-white">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-200">
              <th className="p-4 font-semibold text-gray-600 whitespace-nowrap">Rank</th>
              <th className="p-4 font-semibold text-gray-600 min-w-[300px]">Product Title</th>
              <th className="p-4 font-semibold text-gray-600 whitespace-nowrap">Price</th>
              <th className="p-4 font-semibold text-gray-600 whitespace-nowrap">Est. Sales</th>
              <th className="p-4 font-semibold text-gray-600 whitespace-nowrap">Est. Revenue</th>
            </tr>
          </thead>
          <tbody>
            {data.top_10_products.map((item) => (
              <tr key={item.rank} className="border-b border-gray-100 hover:bg-slate-50 transition-colors">
                <td className="p-4 font-bold text-gray-500">#{item.rank}</td>
                <td className="p-4 text-sm text-gray-800 font-medium">
                  {item.title.length > 70 ? item.title.substring(0, 70) + '...' : item.title}
                </td>
                <td className="p-4 text-gray-600">${item.price.toFixed(2)}</td>
                <td className="p-4 text-gray-600">{item.estimated_sales.toLocaleString()}</td>
                <td className="p-4 font-bold text-emerald-600">${item.estimated_revenue.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ResultsDashboard;
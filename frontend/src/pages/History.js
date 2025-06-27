import React, { useState, useEffect } from 'react';
import axios from 'axios';

const History = () => {
  const [analysisLogs, setAnalysisLogs] = useState([]);
  const [systemLogs, setSystemLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('analysis');

  useEffect(() => {
    fetchHistoryData();
  }, []);

  const fetchHistoryData = async () => {
    try {
      setLoading(true);
      
      // Fetch analysis logs
      const analysisResponse = await axios.get('http://localhost:8000/api/v1/logs/?limit=20');
      setAnalysisLogs(analysisResponse.data.logs);

      // Fetch system logs
      const systemResponse = await axios.get('http://localhost:8000/api/v1/logs/?limit=20');
      setSystemLogs(systemResponse.data.logs);

    } catch (err) {
      console.error('Error fetching history data:', err);
      setError('Failed to load history data');
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="bg-white shadow rounded-lg p-6">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-6"></div>
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-16 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <div className="bg-white shadow rounded-lg p-6">
          <div className="text-center text-red-600">
            <p>{error}</p>
            <button 
              onClick={fetchHistoryData}
              className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Analysis History</h2>
        <p className="text-gray-600 mb-6">
          View all previous analysis results and system activity.
        </p>

        {/* Tab Navigation */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('analysis')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'analysis'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Analysis Logs
            </button>
            <button
              onClick={() => setActiveTab('system')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'system'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              System Logs
            </button>
          </nav>
        </div>

        {/* Analysis Logs Tab */}
        {activeTab === 'analysis' && (
          <div>
            {analysisLogs.length > 0 ? (
              <div className="space-y-4">
                {analysisLogs.map((log, index) => (
                  <div key={index} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium text-gray-900">
                        File ID: {log.file_id}
                      </h3>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        log.status === 'completed' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {log.status}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500">Action:</span>
                        <span className="ml-2 font-medium">{log.action}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Model:</span>
                        <span className="ml-2 font-medium">{log.model_used}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Timestamp:</span>
                        <span className="ml-2 font-medium">{formatTimestamp(log.timestamp)}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500 py-8">
                <p>No analysis history available</p>
                <p className="text-sm">Upload files to see analysis history</p>
              </div>
            )}
          </div>
        )}

        {/* System Logs Tab */}
        {activeTab === 'system' && (
          <div>
            {systemLogs.length > 0 ? (
              <div className="space-y-4">
                {systemLogs.map((log, index) => (
                  <div key={index} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium text-gray-900">
                        {log.service}
                      </h3>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        log.level === 'ERROR' 
                          ? 'bg-red-100 text-red-800'
                          : log.level === 'WARNING'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-green-100 text-green-800'
                      }`}>
                        {log.level}
                      </span>
                    </div>
                    <p className="text-gray-700 mb-2">{log.message}</p>
                    <p className="text-xs text-gray-500">
                      {formatTimestamp(log.timestamp)}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500 py-8">
                <p>No system logs available</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default History; 
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalFiles: 0,
    realContent: 0,
    fakeContent: 0,
    averageConfidence: 0
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch logs for recent activity
      const logsResponse = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/logs/?limit=5`);
      setRecentActivity(logsResponse.data.logs);

      // For now, we'll use mock stats since we don't have a dedicated stats endpoint
      // In a real implementation, you'd have a /api/v1/stats endpoint
      setStats({
        totalFiles: 15,
        realContent: 12,
        fakeContent: 3,
        averageConfidence: 87.5
      });

    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="bg-white shadow rounded-lg p-6">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-2/3 mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="h-32 bg-gray-200 rounded"></div>
              <div className="h-32 bg-gray-200 rounded"></div>
              <div className="h-32 bg-gray-200 rounded"></div>
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
              onClick={fetchDashboardData}
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
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Welcome to Media Authentication System
        </h2>
        <p className="text-gray-600 mb-6">
          AI-powered deepfake detection for images, videos, and audio files.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">📸 Images</h3>
            <p className="text-blue-700">Detect deepfakes in photos and images</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-green-900 mb-2">🎥 Videos</h3>
            <p className="text-green-700">Analyze video content for authenticity</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-purple-900 mb-2">🎵 Audio</h3>
            <p className="text-purple-700">Detect synthetic or manipulated audio</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
          <div className="space-y-4">
            <div className="flex justify-between">
              <span className="text-gray-600">Total Files Analyzed</span>
              <span className="font-semibold">{stats.totalFiles}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Real Content</span>
              <span className="font-semibold text-green-600">{stats.realContent}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Fake Content</span>
              <span className="font-semibold text-red-600">{stats.fakeContent}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Average Confidence</span>
              <span className="font-semibold">{stats.averageConfidence}%</span>
            </div>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
          {recentActivity.length > 0 ? (
            <div className="space-y-3">
              {recentActivity.map((activity, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="flex-shrink-0">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900">{activity.message}</p>
                    <p className="text-xs text-gray-500">
                      {new Date(activity.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              <p>No recent activity</p>
              <p className="text-sm">Upload a file to get started</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 
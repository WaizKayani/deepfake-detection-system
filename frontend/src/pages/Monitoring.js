import React from 'react';

const Monitoring = () => {
  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">System Monitoring</h2>
        <p className="text-gray-600 mb-6">
          Monitor system performance, model metrics, and health status.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="bg-green-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-green-800">System Status</h3>
            <p className="text-2xl font-bold text-green-900">Healthy</p>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-blue-800">CPU Usage</h3>
            <p className="text-2xl font-bold text-blue-900">45%</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-purple-800">Memory Usage</h3>
            <p className="text-2xl font-bold text-purple-900">2.1GB</p>
          </div>
          <div className="bg-yellow-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-yellow-800">Active Models</h3>
            <p className="text-2xl font-bold text-yellow-900">3</p>
          </div>
        </div>

        <div className="text-center text-gray-500 py-8">
          <p>Detailed monitoring charts will appear here</p>
          <p className="text-sm">Prometheus and Grafana integration coming soon</p>
        </div>
      </div>
    </div>
  );
};

export default Monitoring; 
import React from 'react';
import { useParams } from 'react-router-dom';

const Analysis = () => {
  const { fileId } = useParams();

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Analysis Results</h2>
        <p className="text-gray-600 mb-6">
          File ID: {fileId}
        </p>

        <div className="text-center text-gray-500 py-8">
          <p>Analysis results will appear here</p>
          <p className="text-sm">This feature is under development</p>
        </div>
      </div>
    </div>
  );
};

export default Analysis; 
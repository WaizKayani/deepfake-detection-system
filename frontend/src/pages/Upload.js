import React, { useState } from 'react';
import axios from 'axios';

const Upload = () => {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [analysisResults, setAnalysisResults] = useState([]);
  const [error, setError] = useState(null);
  const [analysisStatus, setAnalysisStatus] = useState({});

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      setFiles(Array.from(e.target.files));
    }
  };

  const onButtonClick = () => {
    document.getElementById('file-input').click();
  };

  const analyzeFiles = async () => {
    if (files.length === 0) return;

    setUploading(true);
    setError(null);
    setAnalysisResults([]);
    setAnalysisStatus({}); // Clear previous status

    try {
      const results = [];

      for (const file of files) {
        // Upload file
        const formData = new FormData();
        formData.append('file', file);

        const uploadResponse = await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        // Get file ID from upload response
        const fileId = uploadResponse.data.file_id;

        // Poll for analysis result with exponential backoff
        let analysisResponse = null;
        let attempts = 0;
        const maxAttempts = 30; // 30 seconds max wait time
        const baseDelay = 1000; // Start with 1 second

        // Update status to show analysis is in progress
        setAnalysisStatus(prev => ({
          ...prev,
          [fileId]: { status: 'analyzing', message: 'Analysis in progress...' }
        }));

        while (attempts < maxAttempts) {
          try {
            analysisResponse = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/${fileId}`);
            
            // Update status to show completion
            setAnalysisStatus(prev => ({
              ...prev,
              [fileId]: { status: 'completed', message: 'Analysis completed!' }
            }));
            
            break; // Success, exit polling loop
          } catch (err) {
            if (err.response?.status === 404) {
              // Analysis not ready yet, wait and retry
              attempts++;
              const delay = Math.min(baseDelay * Math.pow(1.5, attempts - 1), 5000); // Max 5 second delay
              
              // Update status to show waiting
              setAnalysisStatus(prev => ({
                ...prev,
                [fileId]: { 
                  status: 'waiting', 
                  message: `Waiting for analysis... (attempt ${attempts}/${maxAttempts})` 
                }
              }));
              
              await new Promise(resolve => setTimeout(resolve, delay));
            } else {
              // Other error, throw it
              setAnalysisStatus(prev => ({
                ...prev,
                [fileId]: { status: 'error', message: 'Analysis failed' }
              }));
              throw err;
            }
          }
        }

        if (!analysisResponse) {
          throw new Error(`Analysis timed out for ${file.name} after ${maxAttempts} attempts`);
        }

        results.push({
          file: file,
          upload: uploadResponse.data,
          analysis: analysisResponse.data,
        });
      }

      setAnalysisResults(results);
      setFiles([]); // Clear files after successful analysis
    } catch (err) {
      console.error('Error analyzing files:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to analyze files. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Upload Media Files</h2>
        <p className="text-gray-600 mb-6">
          Upload images, videos, or audio files for deepfake detection analysis.
        </p>

        <div
          className={`border-2 border-dashed rounded-lg p-8 ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="text-center">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <div className="mt-4">
              <p className="text-lg font-medium text-gray-900">
                Drop files here or click to upload
              </p>
              <p className="text-sm text-gray-500">
                Supports: JPG, PNG, MP4, AVI, WAV, MP3 (Max 100MB)
              </p>
            </div>
            <button
              type="button"
              onClick={onButtonClick}
              className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Select Files
            </button>
            <input
              id="file-input"
              type="file"
              multiple
              accept=".jpg,.jpeg,.png,.bmp,.tiff,.mp4,.avi,.mov,.mkv,.webm,.wav,.mp3,.flac,.m4a,.aac"
              onChange={handleChange}
              className="hidden"
            />
          </div>
        </div>

        {files.length > 0 && (
          <div className="mt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Selected Files</h3>
            <div className="space-y-2">
              {files.map((file, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center">
                    <span className="text-sm font-medium text-gray-900">{file.name}</span>
                    <span className="ml-2 text-sm text-gray-500">
                      ({(file.size / 1024 / 1024).toFixed(2)} MB)
                    </span>
                  </div>
                  <button
                    onClick={() => setFiles(files.filter((_, i) => i !== index))}
                    className="text-red-600 hover:text-red-800"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
            <button 
              onClick={analyzeFiles}
              disabled={uploading}
              className="mt-4 w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {uploading ? 'Analyzing...' : 'Analyze Files'}
            </button>
          </div>
        )}

        {/* Analysis Status Indicators */}
        {Object.keys(analysisStatus).length > 0 && (
          <div className="mt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Analysis Status</h3>
            <div className="space-y-2">
              {Object.entries(analysisStatus).map(([fileId, status]) => (
                <div key={fileId} className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                  <div className="flex items-center">
                    <div className={`w-3 h-3 rounded-full mr-3 ${
                      status.status === 'completed' ? 'bg-green-500' :
                      status.status === 'error' ? 'bg-red-500' :
                      status.status === 'analyzing' ? 'bg-yellow-500' :
                      'bg-blue-500'
                    }`}></div>
                    <span className="text-sm font-medium text-gray-900">
                      {status.message}
                    </span>
                  </div>
                  {status.status === 'waiting' && (
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {analysisResults.length > 0 && (
          <div className="mt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Analysis Results</h3>
            <div className="space-y-4">
              {analysisResults.map((result, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-gray-900">{result.file.name}</h4>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      result.analysis.is_fake 
                        ? 'bg-red-100 text-red-800' 
                        : 'bg-green-100 text-green-800'
                    }`}>
                      {result.analysis.is_fake ? 'FAKE' : 'REAL'}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Confidence:</span>
                      <span className="ml-2 font-medium">
                        {(result.analysis.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Model:</span>
                      <span className="ml-2 font-medium">{result.analysis.model_used}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Processing Time:</span>
                      <span className="ml-2 font-medium">{result.analysis.processing_time}s</span>
                    </div>
                  </div>
                  {result.analysis.metadata?.visual_cues && (
                    <div className="mt-3">
                      <span className="text-gray-500 text-sm">Visual Cues:</span>
                      <ul className="mt-1 text-sm text-gray-700">
                        {result.analysis.metadata.visual_cues.map((cue, i) => (
                          <li key={i} className="ml-4">• {cue}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Upload; 
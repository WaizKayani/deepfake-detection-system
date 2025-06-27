import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';

import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import Analysis from './pages/Analysis';
import History from './pages/History';
import Monitoring from './pages/Monitoring';
import NotFound from './pages/NotFound';

function App() {
  return (
    <>
      <Helmet>
        <title>Media Authentication System</title>
        <meta name="description" content="AI-powered deepfake detection for images, videos, and audio" />
      </Helmet>
      
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/analysis/:fileId" element={<Analysis />} />
          <Route path="/history" element={<History />} />
          <Route path="/monitoring" element={<Monitoring />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Layout>
    </>
  );
}

export default App; 
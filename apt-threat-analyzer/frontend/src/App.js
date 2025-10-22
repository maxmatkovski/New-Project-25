import React, { useState } from 'react';
import { Shield, Activity, Target, FileText } from 'lucide-react';
import Dashboard from './components/Dashboard';
import Analyzer from './components/Analyzer';
import APTProfiles from './components/APTProfiles';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="bg-slate-900/50 backdrop-blur-sm border-b border-slate-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Shield className="w-8 h-8 text-cyan-400" />
              <div>
                <h1 className="text-2xl font-bold text-white">
                  <span className="text-cyan-400">DREAM</span> APT Threat Intelligence Analyzer
                </h1>
                <p className="text-xs text-slate-400">Nation-State Cyber Defense Platform</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <span className="px-3 py-1 bg-green-500/20 text-green-400 text-xs font-medium rounded-full">
                OPERATIONAL
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-1">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center space-x-2 px-6 py-4 text-sm font-medium transition-all ${
                activeTab === 'dashboard'
                  ? 'text-cyan-400 border-b-2 border-cyan-400 bg-slate-700/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/20'
              }`}
            >
              <Activity className="w-4 h-4" />
              <span>Dashboard</span>
            </button>
            <button
              onClick={() => setActiveTab('analyzer')}
              className={`flex items-center space-x-2 px-6 py-4 text-sm font-medium transition-all ${
                activeTab === 'analyzer'
                  ? 'text-cyan-400 border-b-2 border-cyan-400 bg-slate-700/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/20'
              }`}
            >
              <FileText className="w-4 h-4" />
              <span>Threat Analyzer</span>
            </button>
            <button
              onClick={() => setActiveTab('apt')}
              className={`flex items-center space-x-2 px-6 py-4 text-sm font-medium transition-all ${
                activeTab === 'apt'
                  ? 'text-cyan-400 border-b-2 border-cyan-400 bg-slate-700/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/20'
              }`}
            >
              <Target className="w-4 h-4" />
              <span>APT Profiles</span>
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'analyzer' && <Analyzer />}
        {activeTab === 'apt' && <APTProfiles />}
      </main>

      {/* Footer */}
      <footer className="bg-slate-900/50 backdrop-blur-sm border-t border-slate-700 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-slate-400 text-sm">
            <p>Built for Nation-State Cyber Defense | Powered by AI & MITRE ATT&CK</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
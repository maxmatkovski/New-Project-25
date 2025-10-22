import React from 'react';
import { Shield, Target, TrendingUp, AlertTriangle } from 'lucide-react';

function Dashboard() {
  // Mock data for demonstration
  const stats = [
    {
      label: 'Active APT Groups',
      value: '8',
      change: '+2 this month',
      icon: Target,
      color: 'cyan'
    },
    {
      label: 'Reports Analyzed',
      value: '2,847',
      change: '+342 this week',
      icon: Shield,
      color: 'green'
    },
    {
      label: 'Techniques Identified',
      value: '156',
      change: 'MITRE ATT&CK',
      icon: TrendingUp,
      color: 'blue'
    },
    {
      label: 'High Confidence Threats',
      value: '23',
      change: 'Requires attention',
      icon: AlertTriangle,
      color: 'red'
    }
  ];

  const recentThreats = [
    { apt: 'APT28', target: 'Government', confidence: 95, date: '2 hours ago' },
    { apt: 'Lazarus Group', target: 'Financial', confidence: 88, date: '5 hours ago' },
    { apt: 'APT29', target: 'Healthcare', confidence: 92, date: '1 day ago' },
    { apt: 'APT41', target: 'Technology', confidence: 85, date: '2 days ago' },
  ];

  const topTechniques = [
    { id: 'T1566', name: 'Phishing', count: 342 },
    { id: 'T1078', name: 'Valid Accounts', count: 287 },
    { id: 'T1071', name: 'Application Layer Protocol', count: 245 },
    { id: 'T1059', name: 'Command and Scripting Interpreter', count: 198 },
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div>
        <h2 className="text-3xl font-bold text-white mb-2">Threat Intelligence Overview</h2>
        <p className="text-slate-400">Real-time nation-state cyber threat monitoring and analysis</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, idx) => (
          <div key={idx} className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-lg p-6 hover:border-slate-600 transition-all">
            <div className="flex items-center justify-between mb-4">
              <stat.icon className={`w-8 h-8 text-${stat.color}-400`} />
              <span className={`text-2xl font-bold text-${stat.color}-400`}>{stat.value}</span>
            </div>
            <h3 className="text-slate-300 font-medium mb-1">{stat.label}</h3>
            <p className="text-slate-500 text-sm">{stat.change}</p>
          </div>
        ))}
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Threats */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-lg p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center">
            <AlertTriangle className="w-5 h-5 mr-2 text-red-400" />
            Recent High-Confidence Threats
          </h3>
          <div className="space-y-4">
            {recentThreats.map((threat, idx) => (
              <div key={idx} className="bg-slate-900/50 rounded-lg p-4 border border-slate-700">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-white font-semibold">{threat.apt}</span>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    threat.confidence >= 90 
                      ? 'bg-red-500/20 text-red-400'
                      : 'bg-yellow-500/20 text-yellow-400'
                  }`}>
                    {threat.confidence}% confidence
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-400">Target: {threat.target}</span>
                  <span className="text-slate-500">{threat.date}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Techniques */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-lg p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center">
            <TrendingUp className="w-5 h-5 mr-2 text-blue-400" />
            Most Common Attack Techniques
          </h3>
          <div className="space-y-4">
            {topTechniques.map((technique, idx) => (
              <div key={idx} className="bg-slate-900/50 rounded-lg p-4 border border-slate-700">
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <span className="text-cyan-400 font-mono text-sm">{technique.id}</span>
                    <h4 className="text-white font-medium">{technique.name}</h4>
                  </div>
                  <span className="text-2xl font-bold text-slate-400">{technique.count}</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div 
                    className="bg-cyan-400 h-2 rounded-full" 
                    style={{ width: `${(technique.count / 342) * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/20 rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-bold text-white mb-2">Ready to analyze a threat report?</h3>
            <p className="text-slate-400">Upload or paste threat intelligence for instant AI-powered analysis</p>
          </div>
          <button className="px-6 py-3 bg-cyan-500 hover:bg-cyan-600 text-white font-semibold rounded-lg transition-all">
            Start Analysis
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
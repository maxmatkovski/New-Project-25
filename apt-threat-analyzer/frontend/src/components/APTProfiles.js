import React, { useState, useEffect } from 'react';
import { Target, Globe, Zap, TrendingUp } from 'lucide-react';
import axios from 'axios';

function APTProfiles() {
  const [aptGroups, setAptGroups] = useState([]);
  const [selectedAPT, setSelectedAPT] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAPTGroups();
  }, []);

  const fetchAPTGroups = async () => {
    try {
      const response = await axios.get('http://localhost:5001/api/apt');
      setAptGroups(response.data.apt_groups);
    } catch (error) {
      console.error('Failed to fetch APT groups:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAPTProfile = async (aptName) => {
    try {
      const response = await axios.get(`http://localhost:5001/api/apt/${aptName}`);
      setSelectedAPT(response.data.profile);
    } catch (error) {
      console.error('Failed to fetch APT profile:', error);
    }
  };

  const getSophisticationColor = (level) => {
    switch(level) {
      case 'Extremely High': return 'text-red-400 bg-red-500/20';
      case 'Very High': return 'text-orange-400 bg-orange-500/20';
      case 'High': return 'text-yellow-400 bg-yellow-500/20';
      default: return 'text-blue-400 bg-blue-500/20';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-white mb-2">APT Group Profiles</h2>
        <p className="text-slate-400">Intelligence on known nation-state threat actors</p>
      </div>

      {/* APT Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
          <div className="col-span-full text-center text-slate-400 py-12">
            Loading APT profiles...
          </div>
        ) : (
          aptGroups.map((apt, idx) => (
            <div
              key={idx}
              onClick={() => fetchAPTProfile(apt.name)}
              className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-lg p-6 hover:border-cyan-400 hover:shadow-lg hover:shadow-cyan-400/20 transition-all cursor-pointer"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-white mb-2">{apt.name}</h3>
                  <div className="flex items-center space-x-2 text-sm">
                    <Globe className="w-4 h-4 text-slate-400" />
                    <span className="text-slate-400">{apt.origin}</span>
                  </div>
                </div>
                <Target className="w-8 h-8 text-red-400" />
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center space-x-2 text-sm">
                  <Zap className="w-4 h-4 text-cyan-400" />
                  <span className={`px-2 py-1 rounded text-xs font-medium ${getSophisticationColor(apt.sophistication)}`}>
                    {apt.sophistication} Sophistication
                  </span>
                </div>
                
                {apt.aliases && apt.aliases.length > 1 && (
                  <div className="text-xs text-slate-500">
                    Also known as: {apt.aliases.slice(1, 3).join(', ')}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Detailed Profile Modal */}
      {selectedAPT && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800 border border-slate-700 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-slate-800 border-b border-slate-700 p-6 flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-white mb-1">{selectedAPT.name}</h2>
                <p className="text-slate-400">{selectedAPT.origin} | {selectedAPT.sponsor}</p>
              </div>
              <button
                onClick={() => setSelectedAPT(null)}
                className="text-slate-400 hover:text-white text-2xl font-bold"
              >
                ×
              </button>
            </div>

            <div className="p-6 space-y-6">
              {/* Overview */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-3">Overview</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <p className="text-slate-400 text-sm mb-1">Active Since</p>
                    <p className="text-white font-semibold">{selectedAPT.active_since}</p>
                  </div>
                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <p className="text-slate-400 text-sm mb-1">Sophistication</p>
                    <span className={`px-3 py-1 rounded text-sm font-medium ${getSophisticationColor(selectedAPT.sophistication)}`}>
                      {selectedAPT.sophistication}
                    </span>
                  </div>
                  <div className="bg-slate-900/50 rounded-lg p-4 col-span-2">
                    <p className="text-slate-400 text-sm mb-1">Motivation</p>
                    <p className="text-white">{selectedAPT.motivation}</p>
                  </div>
                </div>
              </div>

              {/* Aliases */}
              {selectedAPT.names && selectedAPT.names.length > 1 && (
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">Known Aliases</h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedAPT.names.map((alias, idx) => (
                      <span key={idx} className="px-3 py-1 bg-slate-700 text-slate-300 rounded-full text-sm">
                        {alias}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Target Sectors */}
              {selectedAPT.targets && (
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">Target Sectors</h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedAPT.targets.map((target, idx) => (
                      <span key={idx} className="px-3 py-1 bg-red-500/20 text-red-400 rounded text-sm capitalize">
                        {target}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Known Tools */}
              {selectedAPT.tools && (
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">Known Tools & Malware</h3>
                  <div className="grid grid-cols-2 gap-2">
                    {selectedAPT.tools.map((tool, idx) => (
                      <div key={idx} className="bg-slate-900/50 rounded-lg p-3 border border-slate-700">
                        <p className="text-cyan-400 font-mono text-sm">{tool}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* TTPs */}
              {selectedAPT.ttps && (
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">Common TTPs</h3>
                  <div className="space-y-2">
                    {selectedAPT.ttps.map((ttp, idx) => (
                      <div key={idx} className="flex items-center space-x-2">
                        <TrendingUp className="w-4 h-4 text-cyan-400 flex-shrink-0" />
                        <span className="text-slate-300 capitalize">{ttp}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Threat Level Alert */}
              <div className="bg-gradient-to-r from-red-500/10 to-orange-500/10 border border-red-500/20 rounded-lg p-4">
                <div className="flex items-start space-x-3">
                  <Target className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-red-400 font-semibold mb-1">Active Threat</h4>
                    <p className="text-slate-300 text-sm">
                      This APT group is actively conducting operations. Organizations in targeted sectors should 
                      implement appropriate defensive measures and monitor for indicators of compromise.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default APTProfiles;
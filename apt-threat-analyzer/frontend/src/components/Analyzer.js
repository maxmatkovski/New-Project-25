import React, { useState } from 'react';
import { Send, Loader, AlertCircle, CheckCircle, Target, Shield } from 'lucide-react';
import axios from 'axios';

function Analyzer() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const analyzeReport = async () => {
    if (!text.trim()) {
      setError('Please enter threat intelligence text to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post('http://localhost:5001/api/analyze', {
        text: text
      });

      setResults(response.data.analysis);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze report. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const loadSampleReport = () => {
    setText(`A sophisticated APT28 campaign targeting NATO government agencies has been detected. The attackers used spear phishing emails with malicious attachments exploiting CVE-2024-1234 to gain initial access.

The X-Agent malware was deployed at IP 192.168.1.100, establishing persistence on compromised systems. The campaign focused on collecting intelligence from military and diplomatic targets, consistent with Russian GRU operations.

Credential harvesting techniques were observed using mimikatz, along with lateral movement via RDP to compromise email accounts of high-value targets in Ukraine and Eastern Europe.`);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-white mb-2">Threat Report Analyzer</h2>
        <p className="text-slate-400">AI-powered analysis of threat intelligence reports</p>
      </div>

      {/* Input Section */}
      <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <label className="text-white font-semibold">Threat Intelligence Report</label>
          <button
            onClick={loadSampleReport}
            className="text-cyan-400 hover:text-cyan-300 text-sm font-medium"
          >
            Load Sample Report
          </button>
        </div>
        
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste threat intelligence report here... (IOCs, malware names, attack descriptions, etc.)"
          className="w-full h-48 bg-slate-900 border border-slate-600 rounded-lg p-4 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400"
        />

        <div className="flex items-center justify-between mt-4">
          <span className="text-slate-400 text-sm">{text.length} characters</span>
          <button
            onClick={analyzeReport}
            disabled={loading || !text.trim()}
            className="flex items-center space-x-2 px-6 py-3 bg-cyan-500 hover:bg-cyan-600 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-all"
          >
            {loading ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                <span>Analyze Report</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-4 flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="text-red-400 font-semibold">Analysis Failed</h4>
            <p className="text-red-300 text-sm mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Results Section */}
      {results && (
        <div className="space-y-6">
          {/* Summary Card */}
          <div className="bg-gradient-to-r from-green-500/10 to-cyan-500/10 border border-green-500/20 rounded-lg p-6">
            <div className="flex items-center space-x-3 mb-4">
              <CheckCircle className="w-6 h-6 text-green-400" />
              <h3 className="text-xl font-bold text-white">Analysis Complete</h3>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-slate-400 text-sm">Entities Found</p>
                <p className="text-2xl font-bold text-white">{results.summary.entities_found}</p>
              </div>
              <div>
                <p className="text-slate-400 text-sm">MITRE Techniques</p>
                <p className="text-2xl font-bold text-white">{results.summary.techniques_identified}</p>
              </div>
              <div>
                <p className="text-slate-400 text-sm">Attribution</p>
                <p className="text-lg font-bold text-cyan-400">{results.summary.primary_attribution}</p>
              </div>
              <div>
                <p className="text-slate-400 text-sm">Confidence</p>
                <p className="text-2xl font-bold text-green-400">{results.summary.attribution_confidence}%</p>
              </div>
            </div>
          </div>

          {/* APT Attribution */}
          {results.apt_attribution?.primary && (
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-lg p-6">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center">
                <Target className="w-5 h-5 mr-2 text-red-400" />
                APT Attribution
              </h3>
              <div className="bg-slate-900/50 rounded-lg p-6 border border-slate-600">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h4 className="text-2xl font-bold text-white mb-2">
                      {results.apt_attribution.primary.apt_group}
                    </h4>
                    <div className="space-y-1 text-sm">
                      <p className="text-slate-300">
                        <span className="text-slate-400">Origin:</span> {results.apt_attribution.primary.origin}
                      </p>
                      <p className="text-slate-300">
                        <span className="text-slate-400">Sponsor:</span> {results.apt_attribution.primary.sponsor}
                      </p>
                      <p className="text-slate-300">
                        <span className="text-slate-400">Motivation:</span> {results.apt_attribution.primary.motivation}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-4xl font-bold text-green-400">
                      {results.apt_attribution.primary.confidence}%
                    </div>
                    <div className="text-slate-400 text-sm">Confidence</div>
                  </div>
                </div>
                <div>
                  <h5 className="text-white font-semibold mb-2">Evidence ({results.apt_attribution.primary.evidence_count} indicators):</h5>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {results.apt_attribution.primary.evidence.slice(0, 8).map((ev, idx) => (
                      <div key={idx} className="flex items-center space-x-2 text-sm">
                        <CheckCircle className="w-4 h-4 text-cyan-400 flex-shrink-0" />
                        <span className="text-slate-300">{ev}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* MITRE ATT&CK Techniques */}
          {results.mitre_attack?.techniques && results.mitre_attack.techniques.length > 0 && (
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-lg p-6">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center">
                <Shield className="w-5 h-5 mr-2 text-blue-400" />
                MITRE ATT&CK Techniques ({results.mitre_attack.techniques.length})
              </h3>
              <div className="space-y-3">
                {results.mitre_attack.techniques.map((tech, idx) => (
                  <div key={idx} className="bg-slate-900/50 rounded-lg p-4 border border-slate-600">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <span className="px-2 py-1 bg-cyan-500/20 text-cyan-400 text-xs font-mono rounded">
                            {tech.technique_id}
                          </span>
                          <h4 className="text-white font-semibold">{tech.name}</h4>
                        </div>
                        <p className="text-slate-400 text-sm mb-2">{tech.description}</p>
                        <div className="flex items-center space-x-2 text-xs">
                          <span className="px-2 py-1 bg-slate-700 text-slate-300 rounded">
                            {tech.tactic}
                          </span>
                          <span className="text-slate-500">
                            Matched: {tech.matched_keywords.join(', ')}
                          </span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="text-right">
                          <div className="text-2xl font-bold text-cyan-400">{tech.confidence}%</div>
                          <div className="text-slate-500 text-xs">confidence</div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Entities Extracted */}
          {results.entities && (
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-lg p-6">
              <h3 className="text-xl font-bold text-white mb-4">Extracted Entities</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {results.entities.ips?.length > 0 && (
                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <h4 className="text-cyan-400 font-semibold mb-2">IP Addresses ({results.entities.ips.length})</h4>
                    <div className="space-y-1">
                      {results.entities.ips.map((ip, idx) => (
                        <div key={idx} className="text-slate-300 font-mono text-sm">{ip}</div>
                      ))}
                    </div>
                  </div>
                )}
                {results.entities.cves?.length > 0 && (
                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <h4 className="text-cyan-400 font-semibold mb-2">CVEs ({results.entities.cves.length})</h4>
                    <div className="space-y-1">
                      {results.entities.cves.map((cve, idx) => (
                        <div key={idx} className="text-slate-300 font-mono text-sm">{cve}</div>
                      ))}
                    </div>
                  </div>
                )}
                {results.entities.malware_names?.length > 0 && (
                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <h4 className="text-cyan-400 font-semibold mb-2">Malware ({results.entities.malware_names.length})</h4>
                    <div className="space-y-1">
                      {results.entities.malware_names.map((malware, idx) => (
                        <div key={idx} className="text-slate-300 text-sm">{malware}</div>
                      ))}
                    </div>
                  </div>
                )}
                {results.entities.locations?.length > 0 && (
                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <h4 className="text-cyan-400 font-semibold mb-2">Locations ({results.entities.locations.length})</h4>
                    <div className="space-y-1">
                      {results.entities.locations.map((loc, idx) => (
                        <div key={idx} className="text-slate-300 text-sm">{loc}</div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Analyzer;
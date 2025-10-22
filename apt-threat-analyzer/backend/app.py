from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
from entity_extractor import ThreatEntityExtractor
from mitre_attack import MITREMapper
from apt_attribution import APTAttribution

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to talk to backend

# Load spaCy model for NLP
print("Loading NLP model...")
nlp = spacy.load("en_core_web_sm")
print("NLP model loaded!")

# Initialize all analysis modules
extractor = ThreatEntityExtractor(nlp)
mitre_mapper = MITREMapper()
apt_attributor = APTAttribution()
print("Entity extractor ready!")
print("MITRE ATT&CK mapper ready!")
print("APT attribution engine ready!")
print("\n🚀 All systems operational!\n")

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "APT Threat Analyzer API is running!",
        "version": "1.0.0"
    })

# Full threat intelligence analysis endpoint
@app.route('/api/analyze', methods=['POST'])
def analyze_report():
    try:
        # Get the text from the request
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        print(f"\n📊 Analyzing report ({len(text)} characters)...")
        
        # Step 1: Extract entities
        print("  → Extracting entities...")
        entities = extractor.extract_entities(text)
        
        # Step 2: Map to MITRE ATT&CK
        print("  → Mapping MITRE ATT&CK techniques...")
        mitre_techniques = mitre_mapper.map_text_to_techniques(text)
        tactic_summary = mitre_mapper.get_tactic_summary(mitre_techniques)
        attack_chain = mitre_mapper.generate_attack_chain(mitre_techniques)
        
        # Step 3: APT Attribution
        print("  → Performing APT attribution...")
        apt_attributions = apt_attributor.attribute_attack(text, entities, mitre_techniques)
        
        # Determine primary attribution
        primary_apt = apt_attributions[0] if apt_attributions else None
        
        print(f"✅ Analysis complete!")
        if primary_apt:
            print(f"   Primary attribution: {primary_apt['apt_group']} ({primary_apt['confidence']}% confidence)\n")
        
        # Return comprehensive analysis
        return jsonify({
            "status": "success",
            "timestamp": data.get('timestamp'),
            "analysis": {
                "summary": {
                    "text_length": len(text),
                    "entities_found": entities["total_count"],
                    "techniques_identified": len(mitre_techniques),
                    "primary_attribution": primary_apt['apt_group'] if primary_apt else "Unknown",
                    "attribution_confidence": primary_apt['confidence'] if primary_apt else 0
                },
                "entities": entities,
                "mitre_attack": {
                    "techniques_found": len(mitre_techniques),
                    "techniques": mitre_techniques,
                    "tactic_summary": tactic_summary,
                    "attack_chain": attack_chain
                },
                "apt_attribution": {
                    "primary": primary_apt,
                    "all_candidates": apt_attributions,
                    "total_candidates": len(apt_attributions)
                }
            },
            "message": "Full threat intelligence analysis complete!"
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        return jsonify({"error": str(e)}), 500

# Get APT group profile
@app.route('/api/apt/<apt_name>', methods=['GET'])
def get_apt_profile(apt_name):
    try:
        profile = apt_attributor.get_apt_profile(apt_name)
        
        if profile:
            return jsonify({
                "status": "success",
                "profile": profile
            })
        else:
            return jsonify({
                "status": "not_found",
                "message": f"APT group '{apt_name}' not found in database"
            }), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# List all APT groups
@app.route('/api/apt', methods=['GET'])
def list_apt_groups():
    try:
        groups = apt_attributor.get_all_apt_groups()
        
        return jsonify({
            "status": "success",
            "total_groups": len(groups),
            "apt_groups": groups
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("🛡️  APT THREAT INTELLIGENCE ANALYZER")
    print("="*60)
    print("Starting API server...")
    print("Server running on http://localhost:5001")
    print("="*60 + "\n")
    app.run(debug=True, port=5001)
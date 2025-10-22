from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
from entity_extractor import ThreatEntityExtractor

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to talk to backend

# Load spaCy model for NLP
print("Loading NLP model...")
nlp = spacy.load("en_core_web_sm")
print("NLP model loaded!")

# Initialize entity extractor
extractor = ThreatEntityExtractor(nlp)
print("Entity extractor ready!")

# Test endpoint to make sure server is working
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "APT Threat Analyzer API is running!"
    })

# Main analysis endpoint with entity extraction
@app.route('/api/analyze', methods=['POST'])
def analyze_report():
    try:
        # Get the text from the request
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Extract entities using AI
        entities = extractor.extract_entities(text)
        
        # Return the analysis results
        return jsonify({
            "status": "success",
            "text_length": len(text),
            "entities_found": entities["total_count"],
            "entities": entities,
            "message": "Analysis complete!"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting APT Threat Analyzer API...")
    print("Server running on http://localhost:5001")
    app.run(debug=True, port=5001)
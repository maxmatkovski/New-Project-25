import re
import spacy

class ThreatEntityExtractor:
    """
    Extracts cybersecurity entities from threat intelligence text.
    Finds: IPs, domains, malware names, CVEs, file hashes, and more.
    """
    
    def __init__(self, nlp_model):
        self.nlp = nlp_model
        
    def extract_entities(self, text):
        """
        Main method to extract all threat-related entities from text.
        Returns a dictionary with categorized entities.
        """
        entities = {
            "ips": self._extract_ips(text),
            "domains": self._extract_domains(text),
            "urls": self._extract_urls(text),
            "cves": self._extract_cves(text),
            "file_hashes": self._extract_hashes(text),
            "malware_names": self._extract_malware(text),
            "email_addresses": self._extract_emails(text),
            "organizations": self._extract_organizations(text),
            "locations": self._extract_locations(text)
        }
        
        # Count total entities found
        total_entities = sum(len(v) for v in entities.values())
        entities["total_count"] = total_entities
        
        return entities
    
    def _extract_ips(self, text):
        """Extract IPv4 addresses"""
        # Regex pattern for IPv4
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        ips = re.findall(ip_pattern, text)
        
        # Filter out invalid IPs (e.g., 999.999.999.999)
        valid_ips = []
        for ip in ips:
            parts = ip.split('.')
            if all(0 <= int(part) <= 255 for part in parts):
                valid_ips.append(ip)
        
        return list(set(valid_ips))  # Remove duplicates
    
    def _extract_domains(self, text):
        """Extract domain names"""
        # Pattern for domains (simplified)
        domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
        domains = re.findall(domain_pattern, text)
        
        # Filter out common false positives
        excluded = ['example.com', 'test.com', 'localhost.com']
        domains = [d for d in domains if d.lower() not in excluded]
        
        return list(set(domains))
    
    def _extract_urls(self, text):
        """Extract URLs"""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text)
        return list(set(urls))
    
    def _extract_cves(self, text):
        """Extract CVE identifiers (e.g., CVE-2024-1234)"""
        cve_pattern = r'CVE-\d{4}-\d{4,7}'
        cves = re.findall(cve_pattern, text, re.IGNORECASE)
        return list(set(cves))
    
    def _extract_hashes(self, text):
        """Extract file hashes (MD5, SHA1, SHA256)"""
        hashes = {
            "md5": [],
            "sha1": [],
            "sha256": []
        }
        
        # MD5: 32 hex chars
        md5_pattern = r'\b[a-fA-F0-9]{32}\b'
        hashes["md5"] = list(set(re.findall(md5_pattern, text)))
        
        # SHA1: 40 hex chars
        sha1_pattern = r'\b[a-fA-F0-9]{40}\b'
        hashes["sha1"] = list(set(re.findall(sha1_pattern, text)))
        
        # SHA256: 64 hex chars
        sha256_pattern = r'\b[a-fA-F0-9]{64}\b'
        hashes["sha256"] = list(set(re.findall(sha256_pattern, text)))
        
        return hashes
    
    def _extract_malware(self, text):
        """
        Extract potential malware names using NLP.
        Looks for suspicious capitalized terms and known patterns.
        """
        doc = self.nlp(text)
        
        malware_names = []
        
        # Common malware naming patterns
        malware_keywords = ['trojan', 'ransomware', 'backdoor', 'rootkit', 
                           'worm', 'rat', 'loader', 'stealer', 'botnet',
                           'apt', 'malware', 'virus']
        
        for token in doc:
            # Look for capitalized words near malware keywords
            if token.text[0].isupper() and len(token.text) > 3:
                # Check if near a malware keyword
                for keyword in malware_keywords:
                    if keyword in text.lower()[max(0, token.idx-50):token.idx+50]:
                        malware_names.append(token.text)
                        break
        
        return list(set(malware_names))
    
    def _extract_emails(self, text):
        """Extract email addresses"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))
    
    def _extract_organizations(self, text):
        """Extract organization names using spaCy NER"""
        doc = self.nlp(text)
        orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        return list(set(orgs))
    
    def _extract_locations(self, text):
        """Extract location names using spaCy NER"""
        doc = self.nlp(text)
        locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
        return list(set(locations))


def test_extractor():
    """Test function to demonstrate entity extraction"""
    
    # Sample threat report text
    sample_text = """
    A sophisticated APT28 campaign targeting energy sector organizations 
    has been detected. The attackers used CVE-2024-1234 to gain initial access.
    
    Malicious infrastructure includes:
    - C2 server: 192.168.1.100
    - Domain: malicious-domain.com
    - Malware hash: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
    
    The Emotet trojan was deployed via phishing emails from attacker@evil.com.
    Targets include organizations in United States and European Union.
    """
    
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")
    
    # Create extractor
    extractor = ThreatEntityExtractor(nlp)
    
    # Extract entities
    results = extractor.extract_entities(sample_text)
    
    print("\n=== ENTITY EXTRACTION TEST ===\n")
    print(f"Total entities found: {results['total_count']}\n")
    
    for category, items in results.items():
        if category != "total_count" and items:
            if isinstance(items, dict):
                print(f"{category.upper()}:")
                for sub_cat, sub_items in items.items():
                    if sub_items:
                        print(f"  {sub_cat}: {sub_items}")
            else:
                print(f"{category.upper()}: {items}")
    
    print("\n" + "="*40 + "\n")


if __name__ == "__main__":
    test_extractor()
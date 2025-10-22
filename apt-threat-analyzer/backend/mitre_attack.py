"""
MITRE ATT&CK Technique Mapper
Maps threat intelligence text to MITRE ATT&CK techniques
"""

class MITREMapper:
    """
    Maps cybersecurity text to MITRE ATT&CK techniques.
    Uses keyword matching and pattern recognition.
    """
    
    def __init__(self):
        # Simplified MITRE ATT&CK technique database
        # In production, this would be pulled from MITRE's official API
        self.techniques = {
            "T1566": {
                "name": "Phishing",
                "tactic": "Initial Access",
                "description": "Adversaries may send phishing messages to gain access",
                "keywords": ["phishing", "spear phishing", "email", "malicious attachment", "credential harvesting"]
            },
            "T1190": {
                "name": "Exploit Public-Facing Application",
                "tactic": "Initial Access",
                "description": "Adversaries may exploit vulnerabilities in public-facing applications",
                "keywords": ["exploit", "vulnerability", "CVE", "zero-day", "web application"]
            },
            "T1059": {
                "name": "Command and Scripting Interpreter",
                "tactic": "Execution",
                "description": "Adversaries may abuse command interpreters to execute commands",
                "keywords": ["powershell", "cmd", "bash", "script", "command line", "shell"]
            },
            "T1486": {
                "name": "Data Encrypted for Impact",
                "tactic": "Impact",
                "description": "Adversaries may encrypt data to disrupt availability",
                "keywords": ["ransomware", "encrypt", "encryption", "ransom", "locked files"]
            },
            "T1071": {
                "name": "Application Layer Protocol",
                "tactic": "Command and Control",
                "description": "Adversaries may use application layer protocols for C2",
                "keywords": ["C2", "command and control", "http", "https", "DNS tunneling", "beaconing"]
            },
            "T1078": {
                "name": "Valid Accounts",
                "tactic": "Defense Evasion",
                "description": "Adversaries may use valid credentials to maintain access",
                "keywords": ["credentials", "stolen password", "compromised account", "legitimate account"]
            },
            "T1087": {
                "name": "Account Discovery",
                "tactic": "Discovery",
                "description": "Adversaries may enumerate accounts to find targets",
                "keywords": ["reconnaissance", "account enumeration", "user discovery", "enumerate"]
            },
            "T1021": {
                "name": "Remote Services",
                "tactic": "Lateral Movement",
                "description": "Adversaries may use remote services to move laterally",
                "keywords": ["RDP", "SSH", "remote desktop", "lateral movement", "SMB"]
            },
            "T1005": {
                "name": "Data from Local System",
                "tactic": "Collection",
                "description": "Adversaries may search local systems for files of interest",
                "keywords": ["data theft", "exfiltration", "stolen data", "file collection", "harvesting"]
            },
            "T1567": {
                "name": "Exfiltration Over Web Service",
                "tactic": "Exfiltration",
                "description": "Adversaries may exfiltrate data to cloud storage services",
                "keywords": ["exfiltration", "data transfer", "upload", "cloud storage", "dropbox"]
            },
            "T1098": {
                "name": "Account Manipulation",
                "tactic": "Persistence",
                "description": "Adversaries may manipulate accounts to maintain access",
                "keywords": ["backdoor account", "persistence", "maintain access", "account creation"]
            },
            "T1055": {
                "name": "Process Injection",
                "tactic": "Defense Evasion",
                "description": "Adversaries may inject code into processes",
                "keywords": ["process injection", "DLL injection", "code injection", "memory manipulation"]
            },
            "T1003": {
                "name": "OS Credential Dumping",
                "tactic": "Credential Access",
                "description": "Adversaries may dump credentials from the OS",
                "keywords": ["mimikatz", "credential dump", "LSASS", "password hash", "SAM database"]
            },
            "T1068": {
                "name": "Exploitation for Privilege Escalation",
                "tactic": "Privilege Escalation",
                "description": "Adversaries may exploit vulnerabilities to escalate privileges",
                "keywords": ["privilege escalation", "elevation", "admin access", "root access", "exploit"]
            },
            "T1204": {
                "name": "User Execution",
                "tactic": "Execution",
                "description": "Adversaries may rely on user actions to execute malicious code",
                "keywords": ["malicious link", "user click", "social engineering", "macro", "user execution"]
            }
        }
    
    def map_text_to_techniques(self, text):
        """
        Analyze text and return matching MITRE ATT&CK techniques.
        Returns list of matched techniques with confidence scores.
        """
        text_lower = text.lower()
        matched_techniques = []
        
        for technique_id, technique_data in self.techniques.items():
            # Count keyword matches
            matches = 0
            matched_keywords = []
            
            for keyword in technique_data["keywords"]:
                if keyword.lower() in text_lower:
                    matches += 1
                    matched_keywords.append(keyword)
            
            # If we found matches, add to results
            if matches > 0:
                # Calculate confidence score (0-100)
                # More matches = higher confidence
                confidence = min(100, (matches / len(technique_data["keywords"])) * 100 + 20)
                
                matched_techniques.append({
                    "technique_id": technique_id,
                    "name": technique_data["name"],
                    "tactic": technique_data["tactic"],
                    "description": technique_data["description"],
                    "confidence": round(confidence, 1),
                    "matched_keywords": matched_keywords,
                    "match_count": matches
                })
        
        # Sort by confidence (highest first)
        matched_techniques.sort(key=lambda x: x["confidence"], reverse=True)
        
        return matched_techniques
    
    def get_tactic_summary(self, matched_techniques):
        """
        Summarize which MITRE ATT&CK tactics are present.
        Returns a count of techniques per tactic.
        """
        tactic_counts = {}
        
        for technique in matched_techniques:
            tactic = technique["tactic"]
            if tactic in tactic_counts:
                tactic_counts[tactic] += 1
            else:
                tactic_counts[tactic] = 1
        
        return tactic_counts
    
    def generate_attack_chain(self, matched_techniques):
        """
        Generate a likely attack chain based on matched techniques.
        Orders techniques by typical attack progression.
        """
        # MITRE ATT&CK tactic order (typical attack flow)
        tactic_order = [
            "Initial Access",
            "Execution",
            "Persistence",
            "Privilege Escalation",
            "Defense Evasion",
            "Credential Access",
            "Discovery",
            "Lateral Movement",
            "Collection",
            "Command and Control",
            "Exfiltration",
            "Impact"
        ]
        
        # Group techniques by tactic
        techniques_by_tactic = {}
        for technique in matched_techniques:
            tactic = technique["tactic"]
            if tactic not in techniques_by_tactic:
                techniques_by_tactic[tactic] = []
            techniques_by_tactic[tactic].append(technique)
        
        # Build attack chain in order
        attack_chain = []
        for tactic in tactic_order:
            if tactic in techniques_by_tactic:
                attack_chain.extend(techniques_by_tactic[tactic])
        
        return attack_chain


def test_mitre_mapper():
    """Test the MITRE ATT&CK mapper"""
    
    sample_text = """
    APT28 initiated the attack through a spear phishing campaign targeting 
    government officials. The malicious email contained a weaponized document 
    that exploited CVE-2024-1234. Upon execution, the malware established 
    a command and control channel using HTTPS protocol for beaconing.
    
    The attackers then performed lateral movement via RDP to access additional 
    systems. They dumped credentials using mimikatz and maintained persistence 
    through a backdoor account. Finally, sensitive data was exfiltrated to 
    cloud storage services. Ransomware was deployed to encrypt files across 
    the network.
    """
    
    mapper = MITREMapper()
    
    print("\n=== MITRE ATT&CK MAPPING TEST ===\n")
    print("Analyzing threat report...\n")
    
    # Map text to techniques
    techniques = mapper.map_text_to_techniques(sample_text)
    
    print(f"Found {len(techniques)} matching techniques:\n")
    
    for tech in techniques:
        print(f"[{tech['technique_id']}] {tech['name']}")
        print(f"  Tactic: {tech['tactic']}")
        print(f"  Confidence: {tech['confidence']}%")
        print(f"  Matched keywords: {', '.join(tech['matched_keywords'])}")
        print()
    
    # Show tactic summary
    tactic_summary = mapper.get_tactic_summary(techniques)
    print("\n--- Tactic Summary ---")
    for tactic, count in tactic_summary.items():
        print(f"{tactic}: {count} technique(s)")
    
    # Show attack chain
    print("\n--- Likely Attack Chain ---")
    attack_chain = mapper.generate_attack_chain(techniques)
    for i, tech in enumerate(attack_chain, 1):
        print(f"{i}. [{tech['tactic']}] {tech['name']} ({tech['technique_id']})")
    
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    test_mitre_mapper()
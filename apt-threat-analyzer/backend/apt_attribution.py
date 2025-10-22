"""
APT Attribution Engine
Identifies which nation-state threat actor is likely behind an attack
"""

class APTAttribution:
    """
    Attributes cyber attacks to specific APT groups based on TTPs,
    targets, tools, and infrastructure patterns.
    """
    
    def __init__(self):
        # Database of known APT groups with their characteristics
        self.apt_groups = {
            "APT28": {
                "names": ["APT28", "Fancy Bear", "Sofacy", "Pawn Storm"],
                "origin": "Russia",
                "sponsor": "GRU (Russian Military Intelligence)",
                "active_since": "2007",
                "targets": ["government", "military", "defense", "nato", "ukraine", "political"],
                "tools": ["X-Agent", "Sofacy", "LoJax", "Zebrocy"],
                "ttps": ["spear phishing", "credential harvesting", "exploit"],
                "motivation": "Espionage, Political Intelligence",
                "sophistication": "High"
            },
            "APT29": {
                "names": ["APT29", "Cozy Bear", "The Dukes", "Nobelium"],
                "origin": "Russia",
                "sponsor": "SVR (Foreign Intelligence Service)",
                "active_since": "2008",
                "targets": ["government", "diplomatic", "energy", "healthcare", "research"],
                "tools": ["SolarWinds", "Cobalt Strike", "WellMess", "WellMail"],
                "ttps": ["supply chain", "stealth", "persistence", "cloud"],
                "motivation": "Intelligence Collection, Long-term Espionage",
                "sophistication": "Very High"
            },
            "Lazarus Group": {
                "names": ["Lazarus Group", "Hidden Cobra", "APT38", "Guardians of Peace"],
                "origin": "North Korea",
                "sponsor": "Reconnaissance General Bureau",
                "active_since": "2009",
                "targets": ["financial", "cryptocurrency", "defense", "media", "entertainment"],
                "tools": ["WannaCry", "RATANKBA", "PowerRatankba", "AppleJeus"],
                "ttps": ["ransomware", "destructive attacks", "financial theft", "cryptocurrency"],
                "motivation": "Financial Gain, Sanctions Evasion, Disruption",
                "sophistication": "High"
            },
            "APT41": {
                "names": ["APT41", "Wicked Panda", "Double Dragon"],
                "origin": "China",
                "sponsor": "Ministry of State Security (suspected)",
                "active_since": "2012",
                "targets": ["healthcare", "telecom", "gaming", "technology", "manufacturing"],
                "tools": ["MESSAGETAP", "POISONPLUG", "HIGHNOON"],
                "ttps": ["supply chain", "ransomware", "data theft", "intellectual property"],
                "motivation": "Dual Purpose: Espionage and Financial",
                "sophistication": "Very High"
            },
            "APT33": {
                "names": ["APT33", "Elfin", "Refined Kitten"],
                "origin": "Iran",
                "sponsor": "Iranian Government",
                "active_since": "2013",
                "targets": ["aviation", "energy", "petrochemical", "government"],
                "tools": ["Shamoon", "SHAPESHIFT", "DROPSHOT"],
                "ttps": ["spear phishing", "destructive malware", "reconnaissance"],
                "motivation": "Espionage, Sabotage",
                "sophistication": "Medium-High"
            },
            "Turla": {
                "names": ["Turla", "Snake", "Uroburos", "Waterbug"],
                "origin": "Russia",
                "sponsor": "FSB (Federal Security Service)",
                "active_since": "1996",
                "targets": ["government", "diplomatic", "military", "research"],
                "tools": ["Snake", "Uroburos", "Epic Turla", "Neuron"],
                "ttps": ["watering hole", "hijacking", "satellite communications"],
                "motivation": "Espionage, Long-term Intelligence",
                "sophistication": "Very High"
            },
            "Equation Group": {
                "names": ["Equation Group", "EQUATION"],
                "origin": "United States",
                "sponsor": "NSA (suspected)",
                "active_since": "2001",
                "targets": ["telecommunications", "government", "military", "infrastructure"],
                "tools": ["EQUATION", "DoubleFantasy", "GrayFish", "Fanny"],
                "ttps": ["firmware implants", "advanced persistence", "supply chain"],
                "motivation": "Intelligence Collection, Cyber Warfare Capability",
                "sophistication": "Extremely High"
            },
            "APT10": {
                "names": ["APT10", "MenuPass", "Stone Panda", "Cloud Hopper"],
                "origin": "China",
                "sponsor": "Ministry of State Security",
                "active_since": "2009",
                "targets": ["managed service providers", "technology", "aerospace", "government"],
                "tools": ["PlugX", "Poison Ivy", "ChChes", "RedLeaves"],
                "ttps": ["spear phishing", "MSP compromise", "lateral movement"],
                "motivation": "Intellectual Property Theft, Espionage",
                "sophistication": "High"
            }
        }
    
    def attribute_attack(self, text, entities, mitre_techniques):
        """
        Attribute an attack to an APT group based on multiple signals.
        Returns ranked list of likely APT groups with confidence scores.
        """
        text_lower = text.lower()
        attributions = []
        
        for apt_name, apt_data in self.apt_groups.items():
            score = 0
            evidence = []
            
            # Check if APT group is explicitly mentioned
            for name_variant in apt_data["names"]:
                if name_variant.lower() in text_lower:
                    score += 50
                    evidence.append(f"Direct mention: {name_variant}")
            
            # Check for tool matches
            for tool in apt_data["tools"]:
                if tool.lower() in text_lower:
                    score += 15
                    evidence.append(f"Known tool: {tool}")
            
            # Check for target sector matches
            for target in apt_data["targets"]:
                if target.lower() in text_lower:
                    score += 5
                    evidence.append(f"Target sector: {target}")
            
            # Check for TTP matches
            for ttp in apt_data["ttps"]:
                if ttp.lower() in text_lower:
                    score += 8
                    evidence.append(f"TTP match: {ttp}")
            
            # Check MITRE techniques against known TTPs
            if mitre_techniques:
                for technique in mitre_techniques[:5]:  # Top 5 techniques
                    tech_name = technique['name'].lower()
                    for ttp in apt_data["ttps"]:
                        if ttp in tech_name or tech_name in ttp:
                            score += 3
                            evidence.append(f"MITRE technique alignment: {technique['technique_id']}")
            
            # Only include if we have some evidence
            if score > 0:
                # Normalize confidence to 0-100 scale
                confidence = min(100, score)
                
                attributions.append({
                    "apt_group": apt_name,
                    "confidence": round(confidence, 1),
                    "origin": apt_data["origin"],
                    "sponsor": apt_data["sponsor"],
                    "motivation": apt_data["motivation"],
                    "sophistication": apt_data["sophistication"],
                    "evidence": evidence,
                    "evidence_count": len(evidence)
                })
        
        # Sort by confidence (highest first)
        attributions.sort(key=lambda x: x["confidence"], reverse=True)
        
        return attributions
    
    def get_apt_profile(self, apt_name):
        """Get full profile for a specific APT group"""
        apt_name_upper = apt_name.upper()
        
        # Search by name or alias
        for group_name, group_data in self.apt_groups.items():
            if apt_name_upper in group_name.upper() or \
               any(apt_name_upper in alias.upper() for alias in group_data["names"]):
                return {
                    "name": group_name,
                    **group_data
                }
        
        return None
    
    def get_all_apt_groups(self):
        """Return list of all tracked APT groups"""
        return [
            {
                "name": name,
                "aliases": data["names"],
                "origin": data["origin"],
                "sophistication": data["sophistication"]
            }
            for name, data in self.apt_groups.items()
        ]


def test_apt_attribution():
    """Test APT attribution"""
    
    sample_text = """
    A sophisticated cyber espionage campaign targeting NATO government agencies
    has been attributed to APT28, also known as Fancy Bear. The attackers used
    spear phishing emails with malicious attachments to gain initial access.
    
    The X-Agent malware was deployed, establishing persistence on compromised
    systems. The campaign focused on collecting intelligence from military and
    diplomatic targets, consistent with Russian GRU operations.
    
    Credential harvesting techniques were observed, along with attempts to
    compromise email accounts of high-value targets in Ukraine and Eastern Europe.
    """
    
    # Simulate MITRE techniques (would come from mapper in real use)
    mitre_techniques = [
        {"technique_id": "T1566", "name": "Phishing"},
        {"technique_id": "T1078", "name": "Valid Accounts"}
    ]
    
    attributor = APTAttribution()
    
    print("\n=== APT ATTRIBUTION TEST ===\n")
    print("Analyzing threat intelligence...\n")
    
    # Attribute the attack
    attributions = attributor.attribute_attack(sample_text, {}, mitre_techniques)
    
    if attributions:
        print(f"Found {len(attributions)} potential APT group(s):\n")
        
        for i, attr in enumerate(attributions, 1):
            print(f"{i}. {attr['apt_group']}")
            print(f"   Confidence: {attr['confidence']}%")
            print(f"   Origin: {attr['origin']}")
            print(f"   Sponsor: {attr['sponsor']}")
            print(f"   Motivation: {attr['motivation']}")
            print(f"   Evidence ({attr['evidence_count']} indicators):")
            for evidence in attr['evidence'][:5]:  # Show top 5
                print(f"     • {evidence}")
            print()
    else:
        print("No APT attribution could be made with available indicators.\n")
    
    print("="*50 + "\n")


if __name__ == "__main__":
    test_apt_attribution()
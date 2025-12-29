#!/usr/bin/env python3
"""
USF-2 Domain Detector

Auto-detects task domains from keywords and context.
Maps domains to appropriate agent configurations.

Usage:
    detector = DomainDetector()
    domain = detector.detect("Analyze the authentication security")
    print(domain.name)  # "security"
    print(domain.archetypes)  # ["ARC-AD", "ARC-QA", ...]
"""

import re
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class DetectedDomain:
    """A detected domain with configuration"""
    name: str
    confidence: float
    keywords_matched: Set[str]
    archetypes: List[str]
    compute_type: str
    precision_level: int


class DomainDetector:
    """
    Domain Detector for USF-2

    Analyzes task descriptions to detect domain context
    and recommend appropriate configurations.
    """

    # Domain signatures: keywords -> config
    DOMAIN_SIGNATURES = {
        "security": {
            "keywords": [
                "security", "vulnerability", "exploit", "attack", "defense",
                "authentication", "authorization", "audit", "pentest", "threat",
                "malware", "injection", "xss", "sqli", "csrf", "ssrf", "rce",
            ],
            "archetypes": ["ARC-AD", "ARC-QA", "ARC-IM", "ARC-TH", "ARC-ST"],
            "compute_type": "hivemind",
            "precision_level": 5,
        },
        "crypto": {
            "keywords": [
                "cryptography", "encryption", "decryption", "cipher", "hash",
                "signature", "certificate", "key", "aes", "rsa", "elliptic",
                "post-quantum", "zkp", "commitment", "protocol",
            ],
            "archetypes": ["ARC-TH", "ARC-AD", "ARC-IM", "ARC-QA", "ARC-ST"],
            "compute_type": "hivemind",
            "precision_level": 5,
        },
        "systems": {
            "keywords": [
                "architecture", "design", "scalability", "performance",
                "distributed", "microservices", "infrastructure", "devops",
                "kubernetes", "docker", "cloud", "aws", "azure", "gcp",
            ],
            "archetypes": ["ARC-ST", "ARC-IM", "ARC-QA", "ARC-TH", "ARC-AD"],
            "compute_type": "parallel",
            "precision_level": 3,
        },
        "development": {
            "keywords": [
                "code", "programming", "function", "class", "module",
                "refactor", "test", "debug", "optimize", "implement",
                "api", "sdk", "library", "framework",
            ],
            "archetypes": ["ARC-IM", "ARC-QA", "ARC-TH", "ARC-ST", "ARC-AD"],
            "compute_type": "parallel",
            "precision_level": 3,
        },
        "research": {
            "keywords": [
                "research", "analyze", "investigate", "compare", "evaluate",
                "study", "survey", "literature", "state-of-art", "trend",
            ],
            "archetypes": ["ARC-TH", "ARC-ST", "ARC-IM", "ARC-QA", "ARC-AD"],
            "compute_type": "swarm",
            "precision_level": 4,
        },
        "legal": {
            "keywords": [
                "compliance", "regulation", "gdpr", "hipaa", "pci", "sox",
                "legal", "policy", "governance", "audit", "standard",
            ],
            "archetypes": ["ARC-QA", "ARC-TH", "ARC-ST", "ARC-IM", "ARC-AD"],
            "compute_type": "hivemind",
            "precision_level": 4,
        },
    }

    # Compute type keywords for override
    COMPUTE_KEYWORDS = {
        "quick": ("sequential", 1),
        "simple": ("sequential", 1),
        "fast": ("sequential", 2),
        "thorough": ("swarm", 5),
        "comprehensive": ("swarm", 5),
        "max": ("swarm", 5),
        "compare": ("tournament", 3),
        "evaluate": ("tournament", 3),
        "consensus": ("hivemind", 4),
        "vote": ("hivemind", 4),
    }

    def __init__(self):
        pass

    def detect(self, task: str) -> DetectedDomain:
        """
        Detect domain from task description.

        Args:
            task: Task description

        Returns:
            DetectedDomain with configuration recommendations
        """
        task_lower = task.lower()
        best_domain = None
        best_score = 0.0
        best_keywords = set()

        # Check each domain
        for domain_name, config in self.DOMAIN_SIGNATURES.items():
            matched = set()
            for keyword in config["keywords"]:
                if keyword in task_lower:
                    matched.add(keyword)

            if matched:
                # Score based on keyword match ratio
                score = len(matched) / len(config["keywords"])
                if score > best_score:
                    best_score = score
                    best_domain = domain_name
                    best_keywords = matched

        # Apply compute type overrides from task keywords
        compute_type = "parallel"
        precision_level = 3

        for keyword, (ct, pl) in self.COMPUTE_KEYWORDS.items():
            if keyword in task_lower:
                compute_type = ct
                precision_level = pl
                break

        # If domain detected, use its config as base
        if best_domain:
            config = self.DOMAIN_SIGNATURES[best_domain]
            # Only override compute/precision if not already set by keywords
            if compute_type == "parallel" and precision_level == 3:
                compute_type = config["compute_type"]
                precision_level = config["precision_level"]

            return DetectedDomain(
                name=best_domain,
                confidence=best_score,
                keywords_matched=best_keywords,
                archetypes=config["archetypes"],
                compute_type=compute_type,
                precision_level=precision_level,
            )

        # Default domain
        return DetectedDomain(
            name="general",
            confidence=0.0,
            keywords_matched=set(),
            archetypes=["ARC-TH", "ARC-AD", "ARC-IM", "ARC-ST", "ARC-QA"],
            compute_type=compute_type,
            precision_level=precision_level,
        )

    def detect_all(self, task: str) -> List[DetectedDomain]:
        """
        Detect all matching domains (not just the best).

        Args:
            task: Task description

        Returns:
            List of DetectedDomain sorted by confidence
        """
        task_lower = task.lower()
        domains = []

        for domain_name, config in self.DOMAIN_SIGNATURES.items():
            matched = set()
            for keyword in config["keywords"]:
                if keyword in task_lower:
                    matched.add(keyword)

            if matched:
                score = len(matched) / len(config["keywords"])
                domains.append(DetectedDomain(
                    name=domain_name,
                    confidence=score,
                    keywords_matched=matched,
                    archetypes=config["archetypes"],
                    compute_type=config["compute_type"],
                    precision_level=config["precision_level"],
                ))

        return sorted(domains, key=lambda d: d.confidence, reverse=True)

    def get_recommendations(self, task: str) -> Dict:
        """
        Get full configuration recommendations for a task.

        Args:
            task: Task description

        Returns:
            Dict with compute_type, precision, archetypes, domain
        """
        domain = self.detect(task)

        return {
            "domain": domain.name,
            "confidence": domain.confidence,
            "compute_type": domain.compute_type,
            "precision_level": domain.precision_level,
            "archetypes": domain.archetypes,
            "keywords_matched": list(domain.keywords_matched),
        }


def main():
    """CLI entry point"""
    import argparse
    import json

    parser = argparse.ArgumentParser(description='USF-2 Domain Detector')
    parser.add_argument('task', nargs='?', help='Task to analyze')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--all', action='store_true', help='Show all matching domains')

    args = parser.parse_args()

    if not args.task:
        # Interactive mode
        print("USF-2 Domain Detector")
        print("Enter tasks to analyze (Ctrl+C to exit)\n")
        detector = DomainDetector()

        while True:
            try:
                task = input("> ")
                if not task.strip():
                    continue

                rec = detector.get_recommendations(task)
                print(f"  Domain: {rec['domain']} ({rec['confidence']:.0%})")
                print(f"  Compute: {rec['compute_type']}")
                print(f"  Precision: PL{rec['precision_level']}")
                print(f"  Archetypes: {', '.join(rec['archetypes'][:3])}...")
                print()

            except KeyboardInterrupt:
                print("\nBye!")
                break
    else:
        detector = DomainDetector()

        if args.all:
            domains = detector.detect_all(args.task)
            if args.json:
                print(json.dumps([
                    {
                        "domain": d.name,
                        "confidence": d.confidence,
                        "keywords": list(d.keywords_matched),
                    }
                    for d in domains
                ], indent=2))
            else:
                print(f"Detected domains for: {args.task}\n")
                for d in domains:
                    print(f"  [{d.confidence:.0%}] {d.name}: {', '.join(list(d.keywords_matched)[:3])}")
        else:
            rec = detector.get_recommendations(args.task)
            if args.json:
                print(json.dumps(rec, indent=2))
            else:
                print(f"Domain: {rec['domain']} ({rec['confidence']:.0%} confidence)")
                print(f"Compute Type: {rec['compute_type']}")
                print(f"Precision Level: PL{rec['precision_level']}")
                print(f"Archetypes: {', '.join(rec['archetypes'])}")
                if rec['keywords_matched']:
                    print(f"Keywords: {', '.join(rec['keywords_matched'])}")


if __name__ == '__main__':
    main()

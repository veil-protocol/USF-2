"""
USF-2 Agents Module

Provides agent templates, spawning, and domain detection.

Usage:
    from agents import AgentSpawner, DomainDetector

    # Spawn a verification chain
    spawner = AgentSpawner()
    agent = spawner.spawn("chain-d", "Verify authentication claims")

    # Detect domain
    detector = DomainDetector()
    domain = detector.detect("Analyze cryptographic protocol")
"""

from .spawner import AgentSpawner, SpawnedAgent
from .domain_detector import DomainDetector, DetectedDomain

__all__ = [
    'AgentSpawner',
    'SpawnedAgent',
    'DomainDetector',
    'DetectedDomain',
]

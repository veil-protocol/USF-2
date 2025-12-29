#!/usr/bin/env python3
"""
USF-2 Agent Spawner

Spawns agents from registry with template interpolation.
Generates Task tool invocations ready for Claude Code.

Usage:
    spawner = AgentSpawner()
    agent = spawner.spawn("chain-d", task="Verify security claims")
    print(agent.to_task_dict())
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class SpawnedAgent:
    """A spawned agent ready for Task tool invocation"""
    agent_id: str
    name: str
    subagent_type: str
    prompt: str
    description: str
    tools: List[str] = field(default_factory=list)
    timeout_ms: int = 120000
    run_in_background: bool = True

    def to_task_dict(self) -> Dict[str, Any]:
        """Convert to Task tool invocation format"""
        return {
            "description": self.description,
            "prompt": self.prompt,
            "subagent_type": self.subagent_type,
            "run_in_background": self.run_in_background,
        }

    def to_yaml(self) -> str:
        """Convert to YAML for display"""
        return f"""description: "{self.description}"
subagent_type: "{self.subagent_type}"
run_in_background: {str(self.run_in_background).lower()}
prompt: |
{self._indent(self.prompt, 2)}"""

    def _indent(self, text: str, spaces: int) -> str:
        prefix = ' ' * spaces
        return '\n'.join(prefix + line for line in text.split('\n'))


class AgentSpawner:
    """
    Agent Spawner for USF-2

    Loads agent templates from registry.yaml and spawns
    configured agents with task interpolation.
    """

    def __init__(self, registry_path: Optional[str] = None):
        if registry_path:
            self.registry_path = Path(registry_path)
        else:
            self.registry_path = Path(__file__).parent / 'registry.yaml'

        self.registry = self._load_registry()
        self.agents = self._build_lookup()
        self.archetypes = self._build_archetype_lookup()

    def _load_registry(self) -> Dict:
        """Load agent registry from YAML"""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self.registry_path}")

        with open(self.registry_path) as f:
            return yaml.safe_load(f)

    def _build_lookup(self) -> Dict[str, Dict]:
        """Build flat lookup of agent_id -> agent_config"""
        lookup = {}

        for category, subcategories in self.registry.items():
            if category in ('version', 'last_updated', 'presets', 'archetypes'):
                continue
            if not isinstance(subcategories, dict):
                continue

            for subcategory, agents in subcategories.items():
                if not isinstance(agents, list):
                    continue

                for agent in agents:
                    if isinstance(agent, dict) and 'id' in agent:
                        lookup[agent['id']] = agent
                        agent['_category'] = category
                        agent['_subcategory'] = subcategory

        return lookup

    def _build_archetype_lookup(self) -> Dict[str, Dict]:
        """Build lookup for archetypes"""
        lookup = {}
        archetypes = self.registry.get('archetypes', [])

        for arch in archetypes:
            if isinstance(arch, dict) and 'id' in arch:
                lookup[arch['id']] = arch

        return lookup

    def list_agents(self, category: Optional[str] = None) -> List[Dict]:
        """List available agents"""
        agents = []

        for agent_id, agent in self.agents.items():
            if category and agent.get('_category') != category:
                continue
            agents.append({
                'id': agent_id,
                'name': agent.get('name', agent_id),
                'description': agent.get('description', ''),
                'category': agent.get('_category'),
            })

        return agents

    def list_archetypes(self) -> List[Dict]:
        """List available archetypes"""
        return [
            {
                'id': arch['id'],
                'name': arch.get('name', arch['id']),
                'mode': arch.get('mode', ''),
            }
            for arch in self.archetypes.values()
        ]

    def list_presets(self) -> List[Dict]:
        """List available presets"""
        presets = self.registry.get('presets', {})
        return [
            {
                'name': name,
                'description': config.get('description', ''),
                'agent_count': len(config.get('agents', [])),
            }
            for name, config in presets.items()
        ]

    def get_agent(self, agent_id: str) -> Optional[Dict]:
        """Get agent config by ID"""
        return self.agents.get(agent_id) or self.archetypes.get(agent_id)

    def spawn(
        self,
        agent_id: str,
        task: str,
        context: Optional[str] = None,
        run_in_background: bool = True,
    ) -> SpawnedAgent:
        """
        Spawn an agent with task interpolation.

        Args:
            agent_id: Agent ID from registry
            task: Task description to interpolate
            context: Optional additional context
            run_in_background: Whether to run in background

        Returns:
            SpawnedAgent ready for Task tool invocation
        """
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Unknown agent: {agent_id}")

        # Get template and interpolate
        template = agent.get('prompt_template', 'Task: {task}')
        prompt = template.format(task=task)

        # Add context if provided
        if context:
            prompt += f"\n\n## Additional Context\n{context}"

        return SpawnedAgent(
            agent_id=agent_id,
            name=agent.get('name', agent_id),
            description=f"{agent.get('name', agent_id)}",
            subagent_type=agent.get('subagent_type', 'general-purpose'),
            prompt=prompt.strip(),
            tools=agent.get('tools', []),
            timeout_ms=agent.get('timeout_ms', 120000),
            run_in_background=run_in_background,
        )

    def spawn_archetype(
        self,
        archetype_id: str,
        task: str,
        domain: str = "default",
        run_in_background: bool = True,
    ) -> SpawnedAgent:
        """
        Spawn an archetype with domain synthesis.

        Args:
            archetype_id: Archetype ID (ARC-TH, ARC-AD, etc.)
            task: Task description
            domain: Domain for persona synthesis
            run_in_background: Whether to run in background

        Returns:
            SpawnedAgent with synthesized persona
        """
        archetype = self.archetypes.get(archetype_id)
        if not archetype:
            raise ValueError(f"Unknown archetype: {archetype_id}")

        # Get synthesized persona name
        synthesis = archetype.get('domain_synthesis', {})
        persona = synthesis.get(domain, synthesis.get('default', archetype_id))

        # Build prompt
        template = archetype.get('prompt_template', 'Task: {task}')
        prompt = template.format(task=task)

        return SpawnedAgent(
            agent_id=archetype_id,
            name=persona,
            description=f"{persona} ({archetype_id})",
            subagent_type="general-purpose",
            prompt=prompt.strip(),
            run_in_background=run_in_background,
        )

    def spawn_preset(
        self,
        preset_name: str,
        task: str,
        run_in_background: bool = True,
    ) -> List[SpawnedAgent]:
        """
        Spawn all agents in a preset.

        Args:
            preset_name: Preset name from registry
            task: Task description
            run_in_background: Whether to run in background

        Returns:
            List of SpawnedAgent ready for parallel execution
        """
        presets = self.registry.get('presets', {})
        preset = presets.get(preset_name)

        if not preset:
            raise ValueError(f"Unknown preset: {preset_name}")

        agents = []
        for agent_id in preset.get('agents', []):
            if agent_id.startswith('ARC-'):
                agents.append(self.spawn_archetype(agent_id, task, run_in_background=run_in_background))
            else:
                agents.append(self.spawn(agent_id, task, run_in_background=run_in_background))

        return agents

    def spawn_verification_chain(
        self,
        chain_id: str,
        task: str,
        run_in_background: bool = True,
    ) -> SpawnedAgent:
        """Convenience method for spawning verification chains"""
        return self.spawn(chain_id, task, run_in_background=run_in_background)

    def spawn_panel(
        self,
        task: str,
        domain: str = "default",
        panel_size: int = 5,
        required_archetypes: Optional[List[str]] = None,
    ) -> List[SpawnedAgent]:
        """
        Spawn an expert panel.

        Args:
            task: Task description
            domain: Domain for persona synthesis
            panel_size: Number of experts (max 5)
            required_archetypes: Archetypes that must be included

        Returns:
            List of SpawnedAgent experts
        """
        all_archetypes = list(self.archetypes.keys())

        # Start with required
        selected = list(required_archetypes) if required_archetypes else []

        # Fill remaining slots
        for arch_id in all_archetypes:
            if len(selected) >= panel_size:
                break
            if arch_id not in selected:
                selected.append(arch_id)

        return [
            self.spawn_archetype(arch_id, task, domain=domain)
            for arch_id in selected[:panel_size]
        ]


def main():
    """CLI entry point"""
    import argparse
    import json

    parser = argparse.ArgumentParser(description='USF-2 Agent Spawner')
    parser.add_argument('--list', action='store_true', help='List available agents')
    parser.add_argument('--archetypes', action='store_true', help='List archetypes')
    parser.add_argument('--presets', action='store_true', help='List presets')
    parser.add_argument('--spawn', help='Agent ID to spawn')
    parser.add_argument('--preset', help='Preset to spawn')
    parser.add_argument('--task', help='Task description')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    spawner = AgentSpawner()

    if args.list:
        agents = spawner.list_agents()
        print(f"Available agents: {len(agents)}\n")
        for agent in agents:
            print(f"  {agent['id']}: {agent['description']}")

    elif args.archetypes:
        archetypes = spawner.list_archetypes()
        print(f"Available archetypes: {len(archetypes)}\n")
        for arch in archetypes:
            print(f"  {arch['id']}: {arch['name']} - {arch['mode']}")

    elif args.presets:
        presets = spawner.list_presets()
        print(f"Available presets: {len(presets)}\n")
        for preset in presets:
            print(f"  {preset['name']}: {preset['description']} ({preset['agent_count']} agents)")

    elif args.spawn and args.task:
        agent = spawner.spawn(args.spawn, args.task)
        if args.json:
            print(json.dumps(agent.to_task_dict(), indent=2))
        else:
            print(agent.to_yaml())

    elif args.preset and args.task:
        agents = spawner.spawn_preset(args.preset, args.task)
        if args.json:
            print(json.dumps([a.to_task_dict() for a in agents], indent=2))
        else:
            for agent in agents:
                print(f"--- {agent.name} ---")
                print(agent.to_yaml())
                print()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()

"""
USF-2: Unified Superintelligence Framework
Runner Class for Automated Execution

Provides a simple interface for preparing and executing USF tasks.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .usf_executor import (
    USFExecutor,
    auto_detect_compute,
    auto_detect_precision
)


@dataclass
class USFPreparedPlan:
    """A prepared USF execution plan with helper properties"""
    task: str
    plan_dict: Dict[str, Any]
    executor: 'USFExecutor'

    @property
    def total_agents(self) -> int:
        """Total number of agents to spawn"""
        return self.plan_dict.get("total_agents", 0)

    @property
    def chain_count(self) -> int:
        """Number of verification chain agents"""
        return len(self.plan_dict.get("chain_commands", []))

    @property
    def archetype_count(self) -> int:
        """Number of archetype expert agents"""
        return len(self.plan_dict.get("archetype_commands", []))

    @property
    def spawn_commands(self) -> str:
        """Copy-paste ready Task invocations"""
        lines = ["# USF-2 Agent Spawn Commands", ""]
        lines.append("# Verification Chains")

        for i, cmd in enumerate(self.plan_dict.get("chain_commands", [])):
            lines.append(f"""
Task(
    description="{cmd['description']}",
    prompt=\"\"\"{cmd['prompt'][:200]}...\"\"\",
    subagent_type="{cmd['subagent_type']}",
    run_in_background={cmd['run_in_background']}
)""")

        if self.plan_dict.get("archetype_commands"):
            lines.append("\n# Expert Panel")
            for cmd in self.plan_dict.get("archetype_commands", []):
                lines.append(f"""
Task(
    description="{cmd['description']}",
    prompt=\"\"\"{cmd['prompt'][:200]}...\"\"\",
    subagent_type="{cmd['subagent_type']}",
    run_in_background={cmd['run_in_background']}
)""")

        return "\n".join(lines)

    @property
    def collection_code(self) -> str:
        """Code to collect TaskOutput results"""
        return f"""
# Collect results from all {self.total_agents} agents
outputs = []

# For each spawned agent, collect its output:
# result = TaskOutput(task_id=agent_id, block=True, timeout=60000)
# outputs.append({{"task_id": agent_id, "output": result, "description": description}})

# Example pattern:
for agent_id in spawned_agent_ids:
    result = TaskOutput(task_id=agent_id, block=True, timeout=60000)
    outputs.append({{
        "task_id": agent_id,
        "output": result,
        "description": agent_descriptions[agent_id]
    }})
"""

    @property
    def aggregation_code(self) -> str:
        """Code to aggregate results"""
        return f"""
from usf_executor import USFExecutor

executor = USFExecutor()
plan = {repr(self.plan_dict)}

aggregated = executor.aggregate_from_json(outputs, plan)

print(f"Overall Confidence: {{aggregated['confidence']:.0%}}")
print(f"Chain Results: {{aggregated['chain_count']}}")
print(f"Archetype Results: {{aggregated['archetype_count']}}")
print(f"Aggregation Method: {{aggregated['aggregation_method']}}")
print(f"Status: {{aggregated['status']}}")
"""


class USFRunner:
    """
    High-level runner for USF execution.

    Usage:
        runner = USFRunner()
        plan = runner.prepare("Analyze this code for security issues")
        print(plan.spawn_commands)
        # ... spawn agents ...
        result = runner.aggregate(outputs, plan.plan_dict)
    """

    def __init__(self):
        self.executor = USFExecutor()

    def prepare(
        self,
        task: str,
        compute_type: Optional[str] = None,
        precision_level: Optional[int] = None,
        use_archetypes: bool = True,
        auto: bool = False
    ) -> USFPreparedPlan:
        """
        Prepare an execution plan for a task.

        Args:
            task: The task to analyze
            compute_type: Override compute type (or auto-detect if None)
            precision_level: Override precision (or auto-detect if None)
            use_archetypes: Include expert archetype panel
            auto: Auto-detect compute and precision from task

        Returns:
            USFPreparedPlan with spawn commands and helpers
        """

        if auto or (compute_type is None and precision_level is None):
            compute_type = compute_type or auto_detect_compute(task)
            precision_level = precision_level or auto_detect_precision(task)
        else:
            compute_type = compute_type or "parallel"
            precision_level = precision_level or 3

        plan_dict = self.executor.create_smart_execution_plan(
            task=task,
            precision_level=precision_level,
            use_archetypes=use_archetypes
        )

        # Override compute type if specified
        if compute_type != plan_dict.get("compute_type"):
            plan_dict["compute_type"] = compute_type
            internal_plan = self.executor.create_execution_plan(
                task,
                compute_type=compute_type,
                precision_level=precision_level
            )
            plan_dict["chain_commands"] = self.executor.get_task_commands(internal_plan)

        return USFPreparedPlan(
            task=task,
            plan_dict=plan_dict,
            executor=self.executor
        )

    def aggregate(
        self,
        outputs: List[Dict[str, Any]],
        plan_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Aggregate results from spawned agents.

        Args:
            outputs: List of {task_id, output, description} dicts
            plan_dict: The plan dict from prepare()

        Returns:
            Aggregated results with confidence, status, etc.
        """
        return self.executor.aggregate_from_json(outputs, plan_dict)

    def get_quick_start_guide(self) -> str:
        """Get a quick start guide for using USFRunner"""
        return """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         USF-2 QUICK START GUIDE                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝

1. PREPARE A PLAN
─────────────────
from usf_runner import USFRunner

runner = USFRunner()
plan = runner.prepare("Your task here", auto=True)

print(f"Total agents: {plan.total_agents}")
print(f"Chains: {plan.chain_count}")
print(f"Experts: {plan.archetype_count}")

2. SPAWN AGENTS
───────────────
# View spawn commands:
print(plan.spawn_commands)

# Or iterate manually:
agent_ids = []
for cmd in plan.plan_dict['chain_commands']:
    # agent = Task(description=cmd['description'], ...)
    # agent_ids.append(agent.id)
    pass

for cmd in plan.plan_dict['archetype_commands']:
    # agent = Task(description=cmd['description'], ...)
    # agent_ids.append(agent.id)
    pass

3. COLLECT RESULTS
──────────────────
outputs = []
for agent_id in agent_ids:
    # result = TaskOutput(task_id=agent_id, block=True)
    # outputs.append({"task_id": agent_id, "output": result, "description": "..."})
    pass

4. AGGREGATE
────────────
result = runner.aggregate(outputs, plan.plan_dict)

print(f"Confidence: {result['confidence']:.0%}")
print(f"Status: {result['status']}")
print(f"Method: {result['aggregation_method']}")

═══════════════════════════════════════════════════════════════════════════════
"""

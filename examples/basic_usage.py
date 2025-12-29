#!/usr/bin/env python3
"""
USF-2 Basic Usage Examples

This file demonstrates the core usage patterns for USF-2.
"""

import sys
sys.path.insert(0, '../src')

from usf_executor import USFExecutor, auto_detect_parameters
from usf_runner import USFRunner


def example_1_simple_plan():
    """Create a simple execution plan"""
    print("=" * 60)
    print("Example 1: Simple Execution Plan")
    print("=" * 60)

    executor = USFExecutor()

    # Create plan with defaults
    plan = executor.create_smart_execution_plan(
        task="Analyze this code for potential bugs",
        precision_level=3,
        use_archetypes=True
    )

    print(f"Task: {plan['task']}")
    print(f"Domain: {plan['domain_detected']}")
    print(f"Precision: PL{plan['precision_level']}")
    print(f"Compute: {plan['compute_type']}")
    print(f"Total Agents: {plan['total_agents']}")
    print(f"  - Chains: {len(plan['chain_commands'])}")
    print(f"  - Experts: {len(plan['archetype_commands'])}")
    print()


def example_2_auto_detection():
    """Demonstrate auto-detection of parameters"""
    print("=" * 60)
    print("Example 2: Auto-Detection")
    print("=" * 60)

    tasks = [
        "security audit of authentication system",
        "quick check of this variable",
        "comprehensive analysis of the architecture",
        "compare these two implementations",
        "research the best approach for caching"
    ]

    for task in tasks:
        params = auto_detect_parameters(task)
        print(f"Task: {task[:40]}...")
        print(f"  Compute: {params['compute_type']}")
        print(f"  Precision: PL{params['precision_level']}")
        print()


def example_3_runner():
    """Use the high-level runner"""
    print("=" * 60)
    print("Example 3: USFRunner")
    print("=" * 60)

    runner = USFRunner()

    # Prepare with auto-detection
    plan = runner.prepare(
        "Analyze the security of the login endpoint",
        auto=True
    )

    print(f"Prepared plan:")
    print(f"  Task: {plan.task}")
    print(f"  Total Agents: {plan.total_agents}")
    print(f"  Chains: {plan.chain_count}")
    print(f"  Experts: {plan.archetype_count}")
    print()

    # Show spawn commands (abbreviated)
    print("Spawn commands preview:")
    for cmd in plan.plan_dict['chain_commands'][:2]:
        print(f"  - {cmd['description']}")
    print("  ...")
    print()


def example_4_aggregation():
    """Demonstrate result aggregation"""
    print("=" * 60)
    print("Example 4: Result Aggregation")
    print("=" * 60)

    executor = USFExecutor()

    # Simulate outputs from agents
    outputs = [
        {
            "task_id": "agent1",
            "description": "Chain-A verify",
            "output": '{"chain": "A", "confidence": 0.85, "result": "No issues found"}'
        },
        {
            "task_id": "agent2",
            "description": "Chain-B verify",
            "output": '{"chain": "B", "confidence": 0.78, "result": "Minor concerns"}'
        },
        {
            "task_id": "agent3",
            "description": "Security Auditor (ARC-QA)",
            "output": '{"confidence": 0.92, "result": "Passes audit"}'
        }
    ]

    plan = {
        "compute_type": "parallel",
        "precision_level": 3
    }

    result = executor.aggregate_from_json(outputs, plan)

    print(f"Aggregation Result:")
    print(f"  Confidence: {result['confidence']:.0%}")
    print(f"  Method: {result['aggregation_method']}")
    print(f"  Chain Results: {result['chain_count']}")
    print(f"  Archetype Results: {result['archetype_count']}")
    print(f"  Status: {result['status']}")
    print()


def example_5_compute_types():
    """Show different compute types"""
    print("=" * 60)
    print("Example 5: Compute Types")
    print("=" * 60)

    executor = USFExecutor()
    task = "analyze security"

    compute_types = ["parallel", "hivemind", "swarm", "tournament", "map_reduce"]

    for ct in compute_types:
        plan = executor.create_execution_plan(
            task=task,
            compute_type=ct,
            precision_level=3
        )
        commands = executor.get_task_commands(plan)
        print(f"{ct:20} → {len(commands)} commands")

    print()


if __name__ == "__main__":
    example_1_simple_plan()
    example_2_auto_detection()
    example_3_runner()
    example_4_aggregation()
    example_5_compute_types()

    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)

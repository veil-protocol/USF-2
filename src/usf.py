#!/usr/bin/env python3
"""
USF-2: Unified Superintelligence Framework
Command Line Interface

Usage:
    python usf.py "your task" --json
    python usf.py "your task" --auto
    python usf.py "your task" --compute hivemind --precision 5 --json
"""

import argparse
import json
import sys
from typing import Optional

from usf_executor import (
    USFExecutor,
    ComputeType,
    auto_detect_compute,
    auto_detect_precision,
    auto_detect_parameters
)


def show_interface():
    """Display the full USF interface specification"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    USF-2: Unified Superintelligence Framework                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝

USAGE
═════
  python usf.py "your task"                    # Human-readable output
  python usf.py "your task" --json             # JSON for Claude Task tool
  python usf.py "your task" --auto --json      # Auto-detect parameters

COMPUTE TYPES (--compute)
═════════════════════════
  sequential       │ Chains run one after another
  parallel         │ All chains run simultaneously (default)
  swarm            │ Many agents, best answer wins
  hivemind         │ Consensus voting across agents
  pipeline         │ Output of one feeds into next
  supervisor_worker│ Coordinator + workers
  hybrid           │ Parallel exploration + sequential refinement
  map_reduce       │ Split, parallel process, combine
  tournament       │ Agents compete, best wins
  critic_loop      │ Generate then critique
  ensemble         │ Multiple approaches combined
  mesh_distributed │ Spread across nodes
  mesh_offensive   │ Security-focused execution

PRECISION LEVELS (--precision)
══════════════════════════════
  PL1 │ Quick check (1 chain, 80% confidence target)
  PL2 │ Standard analysis (2 chains, 90% target)
  PL3 │ Important work (3 chains, 95% target) [DEFAULT]
  PL4 │ High stakes (4-6 chains, 99% target)
  PL5 │ Maximum rigor (9 chains, 99.9%+ target)

VERIFICATION CHAINS
═══════════════════
  Chain A │ Single Source Verification
  Chain B │ Dual Source Cross-Reference
  Chain C │ Triple Source Consensus
  Chain D │ Adversarial Verification
  Chain E │ Formal/Mathematical Verification
  Chain F │ Domain Expert Analysis
  Chain G │ Temporal Validity Check
  Chain H │ Multi-Agent Consensus
  Chain I │ Streaming Early-Exit

EXPERT ARCHETYPES
═════════════════
  ARC-TH │ Theoretical (research, proofs, invariants)
  ARC-AD │ Adversarial (attack surface, red team)
  ARC-IM │ Implementation (engineering, optimization)
  ARC-ST │ Strategic (holistic synthesis, trade-offs)
  ARC-QA │ Quality Assurance (testing, compliance)

AUTO-DETECTION RULES
════════════════════
  Keywords                    │ Compute    │ Precision
  ────────────────────────────┼────────────┼───────────
  security, audit, attack     │ hivemind   │ PL5
  max, comprehensive          │ swarm      │ PL5
  compare, evaluate, test     │ tournament │ PL3
  quick, simple, basic        │ sequential │ PL1
  analyze, research           │ parallel   │ PL3

EXAMPLES
════════
  # Security audit with maximum rigor
  python usf.py "security audit of authentication" --compute hivemind --precision 5 --json

  # Quick code review
  python usf.py "quick review of this function" --auto --json

  # Research task
  python usf.py "analyze the VEIL protocol design" --json

OUTPUT FORMAT (--json)
══════════════════════
  {
    "task": "your task",
    "domain_detected": "security|crypto|software|legal|default",
    "precision_level": 1-5,
    "compute_type": "parallel|hivemind|...",
    "chain_commands": [...],       # Verification chain Task invocations
    "archetype_commands": [...],   # Expert panel Task invocations
    "execution_mode": "parallel|sequential",
    "aggregation": {"method": "...", "chain_weight": 0.6, "archetype_weight": 0.4},
    "total_agents": N
  }
""")


def format_human_readable(plan: dict) -> str:
    """Format execution plan for human reading"""
    output = []
    output.append(f"\n{'═' * 60}")
    output.append(f"USF-2 EXECUTION PLAN")
    output.append(f"{'═' * 60}\n")

    output.append(f"Task: {plan['task']}")
    output.append(f"Domain: {plan['domain_detected']}")
    output.append(f"Precision: PL{plan['precision_level']}")
    output.append(f"Compute: {plan['compute_type']}")
    output.append(f"Total Agents: {plan['total_agents']}")

    output.append(f"\n{'─' * 60}")
    output.append("VERIFICATION CHAINS")
    output.append(f"{'─' * 60}")
    for cmd in plan['chain_commands']:
        bg = "(background)" if cmd.get('run_in_background') else "(sequential)"
        output.append(f"  • {cmd['description']} {bg}")

    if plan['archetype_commands']:
        output.append(f"\n{'─' * 60}")
        output.append("EXPERT PANEL")
        output.append(f"{'─' * 60}")
        for cmd in plan['archetype_commands']:
            output.append(f"  • {cmd['description']}")

    output.append(f"\n{'─' * 60}")
    output.append("AGGREGATION")
    output.append(f"{'─' * 60}")
    output.append(f"  Method: {plan['aggregation']['method']}")
    output.append(f"  Chain Weight: {plan['aggregation']['chain_weight']}")
    output.append(f"  Archetype Weight: {plan['aggregation']['archetype_weight']}")

    output.append(f"\n{'═' * 60}")
    output.append("To execute, use: python usf.py \"task\" --json")
    output.append("Then spawn agents using Claude's Task tool.")
    output.append(f"{'═' * 60}\n")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="USF-2: Unified Superintelligence Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "task",
        nargs="?",
        help="Task to analyze"
    )

    parser.add_argument(
        "--compute",
        choices=[ct.value for ct in ComputeType],
        default="parallel",
        help="Compute type (default: parallel)"
    )

    parser.add_argument(
        "--precision",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=3,
        help="Precision level 1-5 (default: 3)"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON for Claude Task tool"
    )

    parser.add_argument(
        "--auto",
        action="store_true",
        help="Auto-detect compute type and precision from task"
    )

    parser.add_argument(
        "--no-archetypes",
        action="store_true",
        help="Disable expert archetype panel"
    )

    parser.add_argument(
        "--show-interface",
        action="store_true",
        help="Display full interface specification"
    )

    args = parser.parse_args()

    if args.show_interface:
        show_interface()
        return 0

    if not args.task:
        parser.print_help()
        return 1

    # Auto-detect parameters if requested
    compute_type = args.compute
    precision = args.precision

    if args.auto:
        params = auto_detect_parameters(args.task)
        compute_type = params["compute_type"]
        precision = params["precision_level"]

    # Create executor and plan
    executor = USFExecutor()

    # Create execution plan
    plan = executor.create_smart_execution_plan(
        task=args.task,
        precision_level=precision,
        use_archetypes=not args.no_archetypes
    )

    # Override compute type if specified
    if args.compute != "parallel" or not args.auto:
        plan["compute_type"] = compute_type
        # Regenerate commands with new compute type
        internal_plan = executor.create_execution_plan(
            args.task,
            compute_type=compute_type,
            precision_level=precision
        )
        plan["chain_commands"] = executor.get_task_commands(internal_plan)

    # Output
    if args.json:
        # Convert to JSON-serializable format for Task tool
        output = {
            "task": plan["task"],
            "domain_detected": plan["domain_detected"],
            "precision_level": plan["precision_level"],
            "compute_type": plan["compute_type"],
            "task_invocations": plan["chain_commands"],
            "archetype_invocations": plan["archetype_commands"],
            "execution_mode": plan["execution_mode"],
            "aggregation": plan["aggregation"],
            "total_agents": plan["total_agents"],
            "spawn_instructions": f"""
# USF-2 Spawn Instructions
# Spawn all agents in parallel using Claude's Task tool:

from usf_executor import USFExecutor
import json

# Store agent IDs as you spawn
agent_ids = []

# 1. Spawn verification chains
for inv in plan['task_invocations']:
    # Use Task tool:
    # Task(description=inv['description'], prompt=inv['prompt'],
    #      subagent_type=inv['subagent_type'], run_in_background=inv['run_in_background'])
    pass

# 2. Spawn archetype panel
for inv in plan['archetype_invocations']:
    # Use Task tool with same pattern
    pass

# 3. Collect results
outputs = []
for agent_id in agent_ids:
    # result = TaskOutput(task_id=agent_id, block=True, timeout=60000)
    # outputs.append({{"task_id": agent_id, "output": result, "description": "..."}})
    pass

# 4. Aggregate
executor = USFExecutor()
aggregated = executor.aggregate_from_json(outputs, plan)
print(f"Confidence: {{aggregated['confidence']:.0%}}")
"""
        }
        print(json.dumps(output, indent=2))
    else:
        print(format_human_readable(plan))

    return 0


if __name__ == "__main__":
    sys.exit(main())

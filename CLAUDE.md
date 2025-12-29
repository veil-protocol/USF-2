# USF-2: Unified Superintelligence Framework

> **Claude Code Memory File** - This file tells Claude how to use USF-2

---

## QUICK START

When user says **"use USF"**, **"invoke USF"**, or needs multi-agent analysis:

```python
# 1. Generate plan
import subprocess, json
result = subprocess.run(
    ["python3", "src/usf.py", "TASK", "--auto", "--json"],
    capture_output=True, text=True
)
plan = json.loads(result.stdout)

# 2. Spawn ALL agents in ONE message (parallel)
for inv in plan['task_invocations'] + plan['archetype_invocations']:
    Task(
        description=inv['description'],
        prompt=inv['prompt'],
        subagent_type=inv['subagent_type'],
        run_in_background=True
    )

# 3. Collect results
outputs = []
for agent_id in spawned_ids:
    result = TaskOutput(task_id=agent_id, block=True, timeout=60000)
    outputs.append({"task_id": agent_id, "output": result, "description": desc})

# 4. Aggregate
from src.usf_executor import USFExecutor
executor = USFExecutor()
final = executor.aggregate_from_json(outputs, plan)
print(f"Confidence: {final['confidence']:.0%}")
```

---

## ZERO-PROMPT INVOCATION (Default Mode)

When user invokes USF without details, **infer everything from context**:

### Trigger Phrases
- "use USF" / "invoke USF" / "USF this"
- "use USF max" → swarm + PL5
- "use USF quick" → sequential + PL1
- "analyze with USF" / "USF security audit"

### Auto-Detection Rules

| Task Keywords | Compute Type | Precision |
|---------------|--------------|-----------|
| security, audit, vulnerability, attack | hivemind | PL5 |
| max, comprehensive, thorough, exhaustive | swarm | PL5 |
| compare, evaluate, test, benchmark | tournament | PL3 |
| quick, simple, check, basic, fast | sequential | PL1 |
| analyze, research, review | parallel | PL3 |
| **default** | parallel | PL3 |

### Zero-Prompt Workflow

```
1. Extract task from user message or conversation context
2. Auto-detect compute type and precision from keywords
3. Generate plan: python3 src/usf.py "TASK" --auto --json
4. Spawn ALL agents immediately (no confirmation needed)
5. Collect results
6. Aggregate and present to user
```

**CRITICAL**: In zero-prompt mode, NEVER ask for confirmation. Spawn agents immediately.

---

## COMPUTE TYPES

| Type | Agents | Use When |
|------|--------|----------|
| `sequential` | 1-3 | Steps must happen in order |
| `parallel` | 3-5 | Independent verification (default) |
| `swarm` | 5-9 | Need many perspectives |
| `hivemind` | 5-7 | Need consensus voting |
| `pipeline` | 3-5 | Each step builds on previous |
| `tournament` | 5-9 | Want competitive best answer |
| `critic_loop` | 2 | Generate + critique |
| `ensemble` | 3 | Multiple analytical approaches |
| `supervisor_worker` | 4+ | Coordinator + parallel workers |
| `map_reduce` | 4+ | Split, process, combine |
| `hybrid` | 4+ | Parallel explore + synthesize |
| `mesh_distributed` | 3+ | Spread across compute nodes |
| `mesh_offensive` | 3+ | Security-focused execution |

---

## PRECISION LEVELS

| Level | Chains | Confidence Target | Use When |
|-------|--------|-------------------|----------|
| PL1 | 1 | 80% | Quick checks, low stakes |
| PL2 | 2 | 90% | Standard analysis |
| PL3 | 3 | 95% | Important work (default) |
| PL4 | 6 | 99% | High stakes |
| PL5 | 9 | 99.9%+ | Maximum rigor, security |

---

## VERIFICATION CHAINS (9 Total)

| Chain | Purpose | When It Helps |
|-------|---------|---------------|
| A | Single source verification | Quick baseline |
| B | Dual source cross-reference | Conflict detection |
| C | Triple source consensus | High-confidence claims |
| D | Adversarial verification | Attack surface, weaknesses |
| E | Formal/mathematical proof | Logic, invariants |
| F | Domain expert analysis | Specialized knowledge |
| G | Temporal validity | Freshness, deprecation |
| H | Multi-agent consensus | Synthesis |
| I | Streaming early-exit | Speed optimization |

---

## EXPERT ARCHETYPES (5 Universal)

| ID | Name | Primary Mode | Domain Examples |
|----|------|--------------|-----------------|
| ARC-TH | Theoretical | Research, proofs | Security Researcher, Cryptographer |
| ARC-AD | Adversarial | Attack, red team | Red Team Operator, Cryptanalyst |
| ARC-IM | Implementation | Engineering | Security Engineer, Developer |
| ARC-ST | Strategic | Big picture | Security Strategist, Tech Lead |
| ARC-QA | Quality Assurance | Validation | Security Auditor, QA Engineer |

Archetypes synthesize into domain-specific personas automatically.

---

## MANUAL MODE

When user says **"use USF manual"** or **"USF step by step"**:

### Step 1: Show Options
```bash
python3 src/usf.py --show-interface
```

### Step 2: Ask User
```
What task should USF analyze?
Which compute type? (parallel/swarm/hivemind/tournament)
Precision level? (PL1-PL5)
```

### Step 3: Confirm Before Spawning
```
Ready to spawn N agents:
- Task: [task]
- Compute: [type]
- Precision: [level]
Proceed? (y/n)
```

### Step 4: Execute with Visibility
- Show each agent as spawned
- Display progress
- Present results step by step

---

## AGGREGATION

### Result Weighting
- **60%** verification chains
- **40%** archetype panel

### Aggregation Methods by Compute Type
| Compute | Method |
|---------|--------|
| parallel | confidence_weighted_average |
| hivemind | majority_vote (60% quorum) |
| swarm | best_of_n |
| tournament | elimination |
| sequential | last_result |
| pipeline | chain_refinement |
| ensemble | weighted_combination |

### Aggregation Code
```python
from src.usf_executor import USFExecutor

executor = USFExecutor()
result = executor.aggregate_from_json(outputs, plan)

# Result contains:
# - confidence: 0.0-1.0
# - result: final synthesized answer
# - chain_count: number of chain results
# - archetype_count: number of archetype results
# - aggregation_method: method used
# - status: success/no_consensus/etc
```

---

## EXAMPLE INVOCATIONS

### Security Audit (High Rigor)
```python
# User: "use USF to audit the authentication system"
# Auto-detects: hivemind, PL5

plan = generate_plan("audit authentication system security", "hivemind", 5)
# Spawns: 9 chains + 7 experts = 16 agents
# Aggregation: majority_vote
```

### Quick Code Review
```python
# User: "use USF quick review of this function"
# Auto-detects: sequential, PL1

plan = generate_plan("review this function", "sequential", 1)
# Spawns: 1 chain + 3 experts = 4 agents
# Aggregation: last_result
```

### Research Task
```python
# User: "use USF to analyze the protocol design"
# Auto-detects: parallel, PL3

plan = generate_plan("analyze protocol design", "parallel", 3)
# Spawns: 3 chains + 5 experts = 8 agents
# Aggregation: confidence_weighted_average
```

### Maximum Analysis
```python
# User: "use USF max on this codebase"
# Auto-detects: swarm, PL5

plan = generate_plan("comprehensive codebase analysis", "swarm", 5)
# Spawns: 9 chains + 7 experts = 16 agents
# Aggregation: best_of_n
```

---

## CLI REFERENCE

```bash
# Show full interface
python3 src/usf.py --show-interface

# Human-readable plan
python3 src/usf.py "your task"

# JSON for Task tool
python3 src/usf.py "your task" --json

# Auto-detect parameters
python3 src/usf.py "your task" --auto --json

# Override compute and precision
python3 src/usf.py "your task" --compute hivemind --precision 5 --json

# No archetype panel
python3 src/usf.py "your task" --no-archetypes --json
```

---

## SUBAGENT TYPE MAPPING

USF-2 uses appropriate subagent types for diversity:

| Context | Subagent Type |
|---------|---------------|
| Research, exploration | `Explore` |
| Coordination, planning | `Plan` |
| Execution, analysis | `general-purpose` |

---

## FILE STRUCTURE

```
USF-2/
├── CLAUDE.md           # This file (memory/invocation guide)
├── README.md           # User documentation
├── src/
│   ├── usf.py          # CLI interface
│   ├── usf_executor.py # Core engine
│   └── usf_runner.py   # Runner class
├── tests/
│   └── test_usf.py     # Test suite
├── examples/
│   └── *.py            # Usage examples
└── docs/
    └── *.md            # Additional documentation
```

---

## KEY PRINCIPLES

1. **Zero-friction**: "use USF" should just work
2. **Auto-detect**: Infer parameters from task context
3. **Parallel first**: Spawn all agents simultaneously
4. **Aggregate always**: Never skip result synthesis
5. **Confidence scores**: Every result has 0-1 confidence
6. **Archetype diversity**: Expert panel adds perspectives

---

## TROUBLESHOOTING

### No agents spawning
- Check `python3 src/usf.py --show-interface` works
- Verify `--json` flag produces valid JSON

### Low confidence results
- Increase precision level (PL4 or PL5)
- Use hivemind for consensus
- Check task clarity

### Timeout issues
- Use `run_in_background=True` for parallel
- Set appropriate `timeout` in TaskOutput

---

**Version**: USF-2.0.0
**License**: MIT
**Repository**: https://github.com/veil-protocol/USF-2
